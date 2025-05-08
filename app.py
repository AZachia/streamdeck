from flask import Flask, render_template, url_for, request, jsonify
from flask_socketio import SocketIO, emit
import os
import json

from plugin_manager import plugin_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load configuration from JSON file
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
else:
    config = {
        "title": "Mon Stream Deck Custom",
        "background": "/static/fond1.jpg",
        "keys": [],
    }
    

print("Configuration loaded:", config)


@app.route('/')
def index():
    
    
    styles = plugin_manager.generate_styles()
    
    
    html = ""
    for componant in config.get("components", []):
        if componant["plugin"] in plugin_manager.plugins:
            html += plugin_manager.generate_component(
                componant.get("plugin"),
                componant.get("component"),
                componant.get("args", {})
            )
            
            
    return render_template('index.html', styles=styles, html=html)

@app.route('/config')
def config_page():
    return render_template('config.html')

@app.route('/static/<path:filename>')
def send_static(filename):
    return app.send_static_file(filename)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'data': 'Connected to server'})
    
@socketio.on('command')
def handle_command(data):
    print('Received command:', data)
    plugin, command, args = data
    plugin_manager.execute_plugin_action(plugin, command, args)
    
    
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    
@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('response', {'data': 'Message received: ' + data['data']})
    

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)