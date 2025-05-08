import json
from plugin import Plugin
from plugin_manager import plugin_manager


class CorePlugin(Plugin):
    def __init__(self):
        super().__init__("core", "1.0.0")

        
        self.register_component(
            "keys",
            {
                "handler": self.keys,
                "description": "Contener of keys",
                "parameters": []
            },
            
        )
        
        
        self.register_component(
            "key",
            {
                "handler": self.key,
                "description": "A key widget",
                "parameters": []
            },   
        )
        
        self.register_component(
            "background",
            {
                "handler": self.background,
                "description": "Background image",
                "parameters": [
                    {
                        "name": "image",
                        "type": "string",
                        "description": "URL of the background image",
                    }
                ]
            },
        )
        
        self.register_script(
            "switchScreen",
            {
                "code": self.switchScreen(),
                "description": "Switch to another screen",
                "parameters": [
                    {
                        "name": "screen",
                        "type": "string",
                        "description": "Name of the screen to switch to",
                    }
                ]
            },
        )
        
        self.register_style(
            """
            .keys {
                flex: 1;
                display: grid;
                gap: 20px;
                padding: 20px;
                box-sizing: border-box;
                justify-items: center;
                align-items: center;
                height: 100vh;
                width: 100vw;
                grid-auto-rows: 1fr;
            }
            
            .key {
                background-color: #007BFF;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 10px;
                cursor: pointer;
                font-size: 16px;
                display: flex;
                justify-content: center;
                align-items: center;
                witdh: 100%;
                height: 100%;
                min-width: 10px;
                min-height: 10px;
                aspect-ratio: 1 / 1;
            }
            
            .key .icon {
                max-width: 80%;
                max-height: 80%;
                object-fit: contain;
            }

            """
        )
    
    
    def switchScreen(self):
        """
        Switch to another screen.
        """
        code = """
        function switchScreen(screen) {
            document.querySelectorAll('.screen').forEach((el) => {
                el.style.display = 'none';
            });
            document.querySelector(`#{screen}`).style.display = 'block';
        }
        """
        return code
    
    def keys(self, args):
        html = f"""
        <div class="keys" style="grid-template-columns: repeat({args.get("col", 4)}, 1fr); grid-template-rows: repeat({args.get("row", 4)}, 1fr);">
        """
        for component in args.get('components', []):
            print(component.get("plugin"))
            if component.get("plugin") in plugin_manager.plugins:
                html += plugin_manager.generate_component(
                    component.get('plugin'),
                    component.get('component'),
                    component.get('args', {})
                )
        html += """
        </div>
        """
        
        return html
        
    
    def key(self, args):
        html = f"""
        <button onclick='sendCommand("{args.get("plugin")}", "{args.get("command")}", {json.dumps(args.get("args"))})'
            class="key" style="background-color: {args.get("color", "#007BFF")}; color: {args.get("text_color", "#FFFFFF")};
            grid-column-start: {args.get("position", {}).get("col")}; grid-row-start: {args.get("position", {}).get("row")};">"""

        if args.get("icon"):
            html += f"""
                <img src="{ args.get('icon') }" alt="{ args.get("label") }" class="icon">"""
        # html += f"""
        #     <span class="label">{ args.get("label") }</span>
        # </button>
        # """

        return html
    
    
    def background(self, args):
        return f"""
        <div class="background" style="position: fixed; z-index:-1; background-image: url({ args.get("image") }); background-size: cover; background-position: center; width: 100%; height: 100%;"></div>
        """ 

