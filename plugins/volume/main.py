from plugin import Plugin
import platform
import subprocess
import os

class VolumePlugin(Plugin):
    def __init__(self):
        super().__init__("volume", "1.0.0")
        
        
        # self.register_script("sendCommand('volume', 'test_all', {})" )
        
        
        self.register_action(
            "toggle",
            {
                "handler": self.toggle_mute,
                "description": "Toggle mute/unmute",
            },
        )
        
        self.register_action(
            "set",
            {
                "handler": self.set_volume,
                "description": "Set the system volume",
                "parameters": [
                    {
                        "name": "volume",
                        "type": "integer",
                        "description": "Volume level (0-100)",
                    }
                ],
            },
        )
        
        self.register_action(
            "get",
            {
                "handler": self.get_volume,
                "description": "Get the current system volume",
            },
        )
        
        self.register_action(
            "is_muted",
            {
                "handler": self.is_muted,
                "description": "Check if the system is muted",
            },
        )
        
        self.register_action(
            "plus",
            {
                "handler": self.volume_plus,
                "description": "Increase the system volume"
            },
        )
        
        self.register_action(
            "minus",
            {
                "handler": self.volume_minus,
                "description": "Decrease the system volume"
            },
        )
        
        
        
        
        self.register_action(
            "media",
            {
                "handler": self.media,
                "description": "Get the current system volume",
            },
        )
        
        self.register_action(
            "play",
            {
                "handler": self.play,
                "description": "Play the current audio",
            },
        )
        
        self.register_action(
            "pause",
            {
                "handler": self.pause,
                "description": "Pause the current audio",
            },
        )
        
        self.register_action(
            "next",
            {
                "handler": self.next,
                "description": "Play the next track",
            },
        )
        
        self.register_action(
            "previous",
            {
                "handler": self.previous,
                "description": "Play the previous track",
            },
        )
        
        self.register_action(
            "play-pause",
            {
                "handler": self.play_pause,
                "description": "Toggle play/pause",
            },
        )
        
        
    
    def media(self, args):
        {"play": self.play, "pause": self.pause, "next": self.next, "previous": self.previous, "play-pause": self.play_pause}.get(args.get("action"), lambda x: None)(args)
    
    
    
    
    def pause(self, args):
        """
        Pause the current audio.
        """
        if platform.system() == "Linux":
            subprocess.run(["playerctl", "pause"])
    
    def play(self, args):
        """
        Play the current audio.
        """
        if platform.system() == "Linux":
            subprocess.run(["playerctl", "play"])
    
    def next(self, args):
        """
        Play the next track.
        """
        if platform.system() == "Linux":
            subprocess.run(["playerctl", "next"])
    
    def previous(self, args):
        """
        Play the previous track.
        """
        if platform.system() == "Linux":
            subprocess.run(["playerctl", "previous"])
    
    def play_pause(self, args):
        """
        Toggle play/pause.
        """
        if platform.system() == "Linux":            
            os.system("playerctl play-pause")
            
    
    
    def get_volume(self):
        """
        Get the current system volume.
        """
        if platform.system() == "Linux":
            result = subprocess.run(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], capture_output=True, text=True)
            if result.returncode == 0:
                volume = result.stdout.split()[4]
                return int(volume[:-1])
    
    def set_volume(self, args):
        """
        Set the system volume.
        """
        if platform.system() == "Linux":
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{args.get("value", 50)}%"])
    
    def toggle_mute(self, args):
        """
        Toggle mute/unmute.
        """
        if platform.system() == "Linux":
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
    
    def is_muted(self):
        """
        Check if the system is muted.
        """
        if platform.system() == "Linux":
            result = subprocess.run(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip() == "yes"
    
    
    def volume_plus(self, args):
        """
        Increase the system volume.
        """
        if platform.system() == "Linux":
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"+{args.get("value", 5)}%"])
        
    
    def volume_minus(self, args):
        """
        Decrease the system volume.
        """
        if platform.system() == "Linux":
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"-{args.get("value", 5)}%"])
        
