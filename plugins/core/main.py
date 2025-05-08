import json
from plugin import Plugin

class CorePlugin(Plugin):
    def __init__(self):
        super().__init__("core", "1.0.0")
        
    
        self.register_component(
            "key",
            {
                "handler": self.key,
                "description": "A key widget",
                "parameters": []
            },
            
        )
        
    
    def key(self, key):
        html = f"""
        <button onclick='sendCommand("{ key.plugin }", "{ key.command }", { json.dumps(key.args) })'
            class="key" style="background-color: { key.color }; color: { key.get('text_color', '#FFFFFF') };
            grid-column-start: { key.position.col }; grid-row-start: { key.position.row };'>"""
            
        if key.get('icon'):
            html += f"""
                <img src="{ key.icon }" alt="{ key.label }" class="icon">"""
        html += f"""
            <span class="label">{ key.label }</span>
        </button>
        """
        return html

