from plugin import Plugin


class HelloWorldPlugin(Plugin):
    def __init__(self):
        super().__init__("helloworld", "1.0.0")

        self.register_action(
            "hello",
            {
                "handler": self.hello,
                "description": "Say hello to the world",
                "parameters": {
                    "name": {
                        "type": "string",
                        "description": "Name of the person to greet",
                    }
                },
            },
        )
        
    def hello(self):
        """
        Greet the world with a hello message.
        """
        print("Hello, world!")