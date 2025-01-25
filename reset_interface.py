import pyeapi
import yaml

def load_config(config_file):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

def delete_vlan_and_interfaces(switch):
    connection = pyeapi.connect(host=switch['host'], username=switch['username'], password=switch['password'])
    node = pyeapi.client.Node(connection)

    while True:
        # Ask for VLANs to delete
        num_vlans = int(input("How many VLANs would you like to delete? "))
        vlan_ids = []

        # Ask for VLAN IDs to delete
        for i in range(num_vlans):
            vlan_id = input(f"Enter VLAN ID to delete (e.g., 100): ")
            vlan_ids.append(vlan_id)

            # Delete VLAN command
            delete_vlan_command = f"no vlan {vlan_id}"
            commands = [delete_vlan_command]
            try:
                node.config(commands)
                print(f"VLAN {vlan_id} deleted.")
            except pyeapi.eapilib.CommandError as e:
                print(f"Error deleting VLAN {vlan_id}: {e}")

        print(f"VLANs {', '.join(vlan_ids)} deleted.")

        # Ask if the user wants to delete more VLANs
        delete_more = input("Do you want to delete more VLANs? (yes/no): ").strip().lower()
        if delete_more != 'yes':
            break

    # Ask how many Ethernet interfaces to reset
    num_interfaces = int(input("How many Ethernet interfaces would you like to reset to default? "))

    # Loop through each interface and prompt for the necessary information
    for i in range(num_interfaces):
        ethernet_number = input(f"Enter the Ethernet number (e.g., 1, 2, 3, etc.) for interface {i+1}: ")
        ethernet_interface = f"Ethernet{ethernet_number}"

        # Reset the Ethernet interface configuration
        commands = [
            f"interface {ethernet_interface}",
            "no ip address",
            "no description",
            "no mtu",
            "no switchport"
        ]
        try:
            node.config(commands)
            print(f"Interface {ethernet_interface} has been reset to default configuration.")
        except pyeapi.eapilib.CommandError as e:
            print(f"Error applying configuration: {e}")

if __name__ == "__main__":
    config = load_config("svi_config.yaml")
    
    delete_vlan_and_interfaces(config['BLS-001'])
