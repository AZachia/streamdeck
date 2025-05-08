from abc import ABC, abstractmethod


class Plugin(ABC):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.actions = {}
        self.components = {}
        self.scripts = {}
        self.styles = []


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
        

    def register_script(self, name: str, script: dict):
        """
        name = nom du script
        valeur = dict
        """
        if name in self.scripts:
            raise ValueError(f"Le script '{name}' est déjà enregistré.")
        self.scripts[name] = script
        
    def register_style(self, style: str):
        """
        style = nom du style
        valeur = str
        """
        if style in self.styles:
            raise ValueError(f"Le style '{style}' est déjà enregistré.")
        self.styles.append(style)
    
    
    def get_styles(self):
        """
        Renvoie la liste des styles enregistrés.
        """
        return "\n".join(self.styles)
        
        
    
    def execute_action(self, action_name, args):
        """
        Exécute l'action spécifiée par action_name avec les arguments fournis.
        """
        action = self.actions.get(action_name)
        if action:
            if callable(action['handler']):
                return action['handler'](args)
            else:
                raise ValueError(f"L'action '{action_name}' n'est pas callable.")
        else:
            raise ValueError(f"L'action '{action_name}' n'est pas enregistrée.")
        
    def generate_component(self, component_name, args):
        """
        Génère le composant spécifié par component_name avec les arguments fournis.
        """
        component = self.components.get(component_name)
        if component:
            if callable(component['handler']):
                return component['handler'](args)
            else:
                raise ValueError(f"Le composant '{component_name}' n'est pas callable.")
        else:
            raise ValueError(f"Le composant '{component_name}' n'est pas enregistré.")
            

    def get_metadata(self):
        return {
            "name": self.name,
            "version": self.version,
            "actions": self.actions
        }

    def get_action_info(self, action_name):
        return self.actions.get(action_name)
