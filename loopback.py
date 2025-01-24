import pyeapi
import yaml
import requests

# Disable SSL certificate verification globally (For self-signed certs)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Load hosts from YAML
with open("hosts.yaml", "r") as file:
    hosts = yaml.safe_load(file)

for host in hosts["hosts"]:
    print(f"Connecting to {host['name']} ({host['ip']})...")

    # Connect to EOS switch (Force HTTPS with ignored SSL warnings)
    conn = pyeapi.connect(
        transport="https",
        host=host["ip"],
        username=host["username"],
        password=host["password"],
        timeout=10,
        verify=False  # This disables SSL verification
    )
    
    try:
        # Execute the command using the 'execute' method
        response = conn.execute("show interfaces")
        
        # Print the entire response to inspect the structure
        print(f"Response from {host['name']}:\n", response)

        # Check for loopback interfaces
        for interface, details in response["result"].items():
            if "Loopback" in interface:
                print(f"{interface}: {details['interfaceStatus']}")

    except Exception as e:
        print(f"Failed to retrieve loopbacks: {e}")
