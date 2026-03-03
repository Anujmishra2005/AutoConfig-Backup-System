import os
import yaml
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException


def load_devices(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)["devices"]


def create_backup_folder(device_name):
    folder_path = os.path.join("backups", device_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def backup_device(device):
    try:
        print(f"\nConnecting to {device['name']} ({device['host']})...")

        connection = ConnectHandler(**device)
        connection.enable()

        running_config = connection.send_command("show running-config")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = create_backup_folder(device["name"])
        filename = f"{device['name']}_backup_{timestamp}.txt"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w") as backup_file:
            backup_file.write(running_config)

        print(f"Backup successful for {device['name']} -> {filepath}")

        connection.disconnect()

    except NetMikoTimeoutException:
        print(f"Timeout Error: Unable to reach {device['name']}")

    except NetMikoAuthenticationException:
        print(f"Authentication Failed for {device['name']}")

    except Exception as e:
        print(f"Error with {device['name']}: {str(e)}")


def main():
    devices = load_devices("devices.yaml")

    for device in devices:
        backup_device(device)


if __name__ == "__main__":
    main()