import json
from plugin import Plugin
from plugin_manager import plugin_manager
import os


class CorePlugin(Plugin):
    def __init__(self):
        super().__init__("core", "1.0.0")
        
        
        self.register_component(
            "screen",
            {
                "handler": self.screen,
                "description": "Screen widget",
            },
        )

        
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
        
        self.register_component(
            "website",
            {
                "handler": self.website,
                "description": "Website widget",
            },
        )
        
        self.register_component(
            "scale",
            {
                "handler": self.scale,
                "description": "Scale widget",
            },
        )
        
        self.register_script(self.switchScreen())
        
        self.register_style(
            """
            
            
            .screen {
                display: none;
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1;
            }
            
            
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
                border-radius: 15px;
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
            
            .website {
                width: 100%;
                height: 100%;
                border: none;
                border-radius: 15px;
                overflow: hidden;
            }
            
            
            .range {
                -webkit-appearance: none;
                top: 50%;
                left: 50%;
                margin: 0;
                padding: 0;
                width: 20rem;
                height: 3.5rem;
                border-radius: 1rem;
                overflow: hidden;
                
            }
            
            input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 0;
            box-shadow: -20rem 0 0 20rem rgb(0, 0, 0, 0.4);
            }

            input[type="range"]::-moz-range-thumb {
            border: none;
            width: 0;
            box-shadow: -20rem 0 0 20rem rgb(0, 0, 0, 0.4);
            }

            """
        )
        
        self.register_action(
            "execute",
            {
                "handler": self.execute,
                "description": "Execute a command on the machine"
            },
        )
    
    
    def switchScreen(self):
        """
        Switch to another screen.
        """
        code = """
        function switchScreen(args) {
            console.log(args);
            document.querySelectorAll('.screen').forEach((el) => {
                el.style.display = 'none';
            });
            if (typeof args === 'string') {
                document.getElementById(args).style.display = 'block';
            } else if (typeof args === 'object') {
                document.getElementById(args.screen).style.display = 'block';
            }
        }
        """
        return code
    
    
    def screen(self, args):
        """
        Generate the screens.
        """
        html = f"""
        <div class="screen" id="{args.get("id")}">
        """
        for component in args.get('components', []):
            if component.get("plugin") in plugin_manager.plugins:
                html += plugin_manager.generate_component(
                    component.get('plugin'),
                    component.get('component'),
                    component.get('args', {})
                )
        html += """
        </div>
        """
        
        if args.get("default", False):
            self.register_script(
                f"""
                    switchScreen("{args.get("id")}");
                """
            )
        
        return html
    
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
        <button onclick='sendCommand("{args.get("plugin")}", "{args.get("command", {})}", {json.dumps(args.get("args"))})'
            class="key" style="background-color: {args.get("color", "#007BFF")}; color: {args.get("text_color", "#FFFFFF")};
            grid-column-start: {args.get("position", {}).get("col")}; grid-row-start: {args.get("position", {}).get("row")};">"""

        if args.get("icon"):
            html += f"""
                <img src="{ args.get('icon') }" alt="{ args.get("label") }" class="icon">"""
        # html += f"""
        #     <span class="label">{ args.get("label") }</span>
        # </button>
        # """
        
        html += """
        </button>
        """

        return html
    
    
    def background(self, args):
        return f"""
        <div class="background" style="position: fixed; z-index:-1; background-image: url({ args.get("image") }); background-size: cover; background-position: center; width: 100%; height: 100%;"></div>
        """
        
    def website(self, args):
        return f"""
        <iframe src="{args.get("url")}" style="grid-column-start: {args.get("position", {}).get("col", 1)}; grid-row-start: {args.get("position", {}).get("row", 1)}; grid-column: span {args.get("position", {}).get("width", 1)}; grid-row: span {args.get("position", {}).get("height", 1)};" class="website"></iframe>
        """
        
    def scale(self, args):
        html = f"""
        <input type="range" min="{args.get("min", 0)}" max="{args.get("max", 100)}" value="{args.get("value", 50)}" style="grid-column-start: {args.get("position", {}).get("col")}; grid-row-start: {args.get("position", {}).get("row")}; grid-column: span {args.get("position", {}).get("width")}; grid-row: span {args.get("position", {}).get("height")}; width: 100%; height: 100%;" oninput="sendCommand('{args.get('plugin')}', '{args.get('command', {})}', """ + """{value: this.value})" class="range" />"""
        return html
    
    
    def execute(self, args):
        """
        Execute a command on the machine.
        """
        print(args)
        os.system(args.get("cmd", ""))
        

