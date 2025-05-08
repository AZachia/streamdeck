from plugin import Plugin
import webbrowser


class WebOpenerPlugin(Plugin):
    def __init__(self):
        super().__init__("webopener", "1.0.0")

        self.register_action(
            "open",
            {
                "handler": self.open,
                "description": "Open a web page in the default browser",
                "parameters": [
                    {
                        "name": "url",
                        "type": "string",
                        "description": "URL to open",
                    }
                ]
            },
        )

    def open(self, url):
        """
        Open a web page in the default browser.
        """

        webbrowser.open(url)
