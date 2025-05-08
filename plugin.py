from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.actions = {}
        self.components = {}


    def register_action(self, name: str, action: dict):
        """
        name = nom de l'action
        valeur = dict
        """
        if name in self.actions:
            raise ValueError(f"L'action '{name}' est déjà enregistrée.")
        self.actions[name] = action
        
    
    def register_component(self, name: str, component: dict):
        """
        name = nom du composant
        valeur = dict
        """
        if name in self.components:
            raise ValueError(f"Le composant '{name}' est déjà enregistré.")
        self.components[name] = component
        
        
    
    def execute_action(self, action_name, *args, **kwargs):
        """
        Exécute l'action spécifiée par action_name avec les arguments fournis.
        """
        action = self.actions.get(action_name)
        if action:
            if callable(action['handler']):
                return action['handler'](*args, **kwargs)
            else:
                raise ValueError(f"L'action '{action_name}' n'est pas callable.")
        else:
            raise ValueError(f"L'action '{action_name}' n'est pas enregistrée.")
            

    def get_metadata(self):
        return {
            "name": self.name,
            "version": self.version,
            "actions": self.actions
        }

    def get_action_info(self, action_name):
        return self.actions.get(action_name)
