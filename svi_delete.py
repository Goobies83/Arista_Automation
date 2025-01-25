import pyeapi
import yaml

def load_config(config_file):
    """Load YAML configuration file."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

def delete_svi(switch):
    """Delete SVI interfaces from the Arista switch."""
    connection = pyeapi.connect(
        host=switch['host'],
        username=switch['username'],
        password=switch['password'],
        transport="https"
    )
    node = pyeapi.client.Node(connection)

    while True:
        # Ask how many SVIs to delete
        num_svis = int(input("How many SVIs would you like to delete? "))

        for _ in range(num_svis):
            svi_id = input("Enter SVI ID to delete (e.g., 100): ")

            try:
                # Check if the SVI exists
                show_command = f"show interfaces Vlan{svi_id}"
                output = node.run_commands([show_command])

                if 'interfaceStatuses' in output[0] and f"Vlan{svi_id}" in output[0]['interfaceStatuses']:
                    # Delete the SVI if it exists
                    node.config([f"no interface Vlan{svi_id}"])
                    print(f"SVI for VLAN {svi_id} deleted.")
                else:
                    print(f"SVI for VLAN {svi_id} does not exist, skipping deletion.")

            except pyeapi.eapilib.CommandError as e:
                print(f"Error checking or deleting SVI for VLAN {svi_id}: {e}")

        # Ask if the user wants to delete more SVIs
        delete_more = input("Do you want to delete more SVIs? (yes/no): ").strip().lower()
        if delete_more != 'yes':
            break

if __name__ == "__main__":
    config = load_config("switch_config.yaml")
    delete_svi(config['BLS-001'])
