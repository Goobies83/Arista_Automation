import pyeapi
import yaml
import re

def load_config(config_file):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

def configure_svi_and_interfaces(switch):
    connection = pyeapi.connect(host=switch['host'], username=switch['username'], password=switch['password'])
    node = pyeapi.client.Node(connection)

    # Get the current configuration using run_commands
    commands = ["show running-config"]
    output = node.run_commands(commands)
    
    # Extract the running-config from the response
    current_config = output[0].get('output', '')  # Use .get() to avoid KeyError

    commands = []

    # Ask for VLANs to create
    num_vlans = int(input("How many VLANs would you like to create? "))
    vlan_info = {}
    
    # Ask for VLAN IDs and names
    for i in range(num_vlans):
        vlan_id = input(f"Enter VLAN ID for VLAN {i+1}: ")
        vlan_name = input(f"Enter name for VLAN {vlan_id}: ")
        vlan_info[vlan_id] = vlan_name
        commands.append(f"vlan {vlan_id}")
        commands.append(f"name {vlan_name}")

    # Ask for SVI configurations
    svi_info = {}
    for vlan_id in vlan_info:
        ip_address = input(f"Enter the IP address for SVI {vlan_id} (e.g., 10.0.10.1/24): ")
        svi_info[vlan_id] = ip_address
        # Add SVI configuration commands
        commands.extend([
            f"interface Vlan{vlan_id}",
            f"ip address {ip_address}",
            "no shutdown"
        ])

    # Ask how many Ethernet interfaces need to be configured
    num_interfaces = int(input("How many Ethernet interfaces would you like to configure? "))
    
    # Loop through each interface and prompt for the necessary information
    for i in range(num_interfaces):
        # Ask for the Ethernet number (e.g., 1, 2, 3, etc.)
        ethernet_number = input(f"Enter the Ethernet number (e.g., 1, 2, 3, etc.) for interface {i+1}: ")
        ethernet_interface = f"Ethernet{ethernet_number}"
        new_ip_address = input(f"Enter the new IP address for {ethernet_interface} (e.g., 10.0.5.1/31): ")

        # Check if the interface already exists in the configuration
        interface_found = False
        ip_found = False

        # Use regex to match interface and IP address
        interface_pattern = re.compile(rf"interface {ethernet_interface}")
        ip_pattern = re.compile(rf"ip address (\S+)")

        # Check if interface is in the config
        if interface_pattern.search(current_config):
            interface_found = True

            # Check if an IP address is already configured for this interface
            ip_match = ip_pattern.findall(current_config)
            for ip in ip_match:
                if ip == new_ip_address:
                    ip_found = True
                    print(f"IP address {new_ip_address} is already configured on {ethernet_interface}, skipping update.")
                    break
                else:
                    # Warning message: Show existing and new IP address
                    print(f"WARNING: {ethernet_interface} already has IP address {ip}. Overriding with {new_ip_address}.")
                    commands.extend([
                        f"interface {ethernet_interface}",
                        f"no ip address",  # Remove the existing IP address first
                        f"ip address {new_ip_address}"
                    ])
                    break

        if not interface_found:
            # Add the interface configuration if not found
            commands.extend([
                f"interface {ethernet_interface}",
                "description Spine1",
                "mtu 9214",
                "no switchport",
                f"ip address {new_ip_address}"
            ])
    
    # Apply the configuration
    if commands:
        try:
            node.config(commands)
            print(f"VLANs, SVIs, and {num_interfaces} Ethernet interfaces configured on {switch['host']}")
        except pyeapi.eapilib.CommandError as e:
            print(f"Error applying configuration: {e}")

if __name__ == "__main__":
    config = load_config("svi_config.yaml")
    
    configure_svi_and_interfaces(config['BLS-001'])
