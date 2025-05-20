import os
import importlib.util
from plugin import Plugin


class PluginManager:
    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        self.plugins = {}  # {plugin_name: plugin_instance}

    def load_plugins(self):
        for plugin_name in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, plugin_name, "main.py")
            if not os.path.isfile(plugin_path):
                continue

            module_name = f"{plugin_name}_plugin"
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                print(f"Erreur de chargement du plugin {plugin_name}: {e}")
                continue

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Plugin)
                    and attr is not Plugin
                ):
                    try:
                        instance = attr()
                        self.plugins[instance.name] = instance
                        print(f"✅ Plugin chargé : {instance.name}")
                    except Exception as e:
                        print(
                            f"❌ Erreur lors de l'instanciation du plugin {plugin_name}: {e}"
                        )
    
    def execute_plugin_action(self, plugin_name, action_name, args):
        """
        Exécute l'action spécifiée par action_name du plugin spécifié.
        """
        plugin = self.plugins.get(plugin_name)
        if plugin:
            try:
                return plugin.execute_action(action_name, args)
            except Exception as e:
                print(f"Erreur lors de l'exécution de l'action '{action_name}' du plugin '{plugin_name}': {e}")
        else:
            print(f"Plugin '{plugin_name}' non trouvé.")
            return None
        
    
    def generate_component(self, plugin_name, component_name, args):
        """
        Génère le composant spécifié par component_name du plugin spécifié.
        """
        
        print(plugin_name, component_name, args)
        plugin = self.plugins.get(plugin_name)
        if plugin:
            try:
                return plugin.generate_component(component_name, args)
            except Exception as e:
                print(f"Erreur lors de la génération du composant '{component_name}' du plugin '{plugin_name}': {e}")
        else:
            print(f"Plugin '{plugin_name}' non trouvé.")
            return None
    
    def generate_styles(self):
        """
        Génère les styles de tous les plugins.
        """
        styles = ""
        for plugin in self.plugins.values():
            styles += plugin.get_styles()
        return styles

    
    def get_scripts(self):
        """
        Renvoie la liste des scripts de tous les plugins.
        """
        scripts = ""
        for plugin in self.plugins.values():
            scripts += plugin.get_scripts()
        return scripts

    def get_plugin(self, name):
        return self.plugins.get(name)

    def all_plugins(self):
        return self.plugins


plugin_manager = PluginManager()
plugin_manager.load_plugins()