import paramiko
import yaml

def load_hosts(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def delete_svi(host, username, password, vlan_id):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, look_for_keys=False, allow_agent=False)
        
        shell = client.invoke_shell()
        shell.send("enable\n")
        shell.send("Goobies83\n")  # Enter enable password
        shell.send("show ip interface brief | include Vlan{}\n".format(vlan_id))
        shell.recv(5000)  # Read initial output
        
        shell.send("\n")  # Ensure command execution
        output = shell.recv(5000).decode('utf-8')
        
        if f"Vlan{vlan_id}" not in output:
            print(f"SVI VLAN {vlan_id} is not present on {host}. Skipping...")
        else:
            shell.send("configure terminal\n")
            shell.send(f"no interface vlan {vlan_id}\n")
            shell.send("end\n")
            shell.send("write memory\n")
            print(f"SVI VLAN {vlan_id} deleted successfully on {host}.")
        
        client.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    hosts = load_hosts("delete_SVI.yaml")
    host_info = hosts.get("hosts", {}).get("BLS-001")
    
    if not host_info:
        print("Host information not found.")
        exit()
    
    host = host_info["ip"]
    username = host_info["username"]
    password = host_info["password"]
    
    num_svis = int(input("Enter number of SVI interfaces to delete: "))
    vlan_ids = [input(f"Enter VLAN ID {i+1}: ") for i in range(num_svis)]
    
    for vlan_id in vlan_ids:
        delete_svi(host, username, password, vlan_id)
