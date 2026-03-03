import os
import yaml
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()


def load_devices(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data["devices"]


def create_backup_folder(device_name):
    folder_path = os.path.join("backups", device_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def get_mock_config(device_name):
    """Fallback mock configuration if device is unreachable."""
    return f"""
hostname {device_name}
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
line vty 0 4
 login local
 transport input ssh
"""


def backup_device(device):
    device_copy = device.copy()
    device_name = device_copy.pop("name")

    # Add credentials from environment variables
    device_copy["username"] = os.getenv("NET_USERNAME", "labuser")
    device_copy["password"] = os.getenv("NET_PASSWORD", "labpassword")
    device_copy["secret"] = os.getenv("NET_SECRET", "labsecret")

    print(f"\nConnecting to {device_name} ({device_copy['host']})...")

    try:
        connection = ConnectHandler(**device_copy)
        connection.enable()
        running_config = connection.send_command("show running-config")
        connection.disconnect()
        print(f"Connected successfully to {device_name}")

    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        print(f"⚠ Could not connect to {device_name}. Using mock configuration.")
        running_config = get_mock_config(device_name)

    except Exception as e:
        print(f"⚠ Error with {device_name}: {str(e)}")
        running_config = get_mock_config(device_name)

    # Save backup file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder = create_backup_folder(device_name)
    filename = f"{device_name}_backup_{timestamp}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as backup_file:
        backup_file.write(running_config)

    print(f"Backup saved at: {filepath}")


def main():
    print("===== AutoConfig Backup System Started =====")
    devices = load_devices("devices.yaml")

    for device in devices:
        backup_device(device)

    print("\n===== Backup Process Completed =====")


if __name__ == "__main__":
    main()