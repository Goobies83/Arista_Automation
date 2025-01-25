import pyeapi
import yaml

def load_config(config_file):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

def configure_svi(switch):
    connection = pyeapi.connect(host=switch['host'], username=switch['username'], password=switch['password'])
    node = pyeapi.client.Node(connection)
    
    commands = []
    for vlan, ip in switch['svi'].items():
        commands.extend([
            f"vlan {vlan}",
            f"interface Vlan{vlan}",
            f"ip address virtual {ip}",
            "no shutdown"
        ])
    
    node.config(commands)
    print(f"SVI interfaces configured on {switch['host']}")

if __name__ == "__main__":
    config = load_config("svi_config.yaml")
    
    configure_svi(config['BLS-001'])
