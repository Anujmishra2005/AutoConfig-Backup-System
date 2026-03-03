import os
import yaml
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException


def load_devices(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data["devices"]


def create_backup_folder(device_name):
    folder_path = os.path.join("backups", device_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def backup_device(device):
    device_copy = device.copy()  # Avoid modifying original dictionary
    device_name = device_copy.pop("name")  # Remove 'name' before passing to Netmiko

    try:
        print(f"\nConnecting to {device_name} ({device_copy['host']})...")

        connection = ConnectHandler(**device_copy)
        connection.enable()

        running_config = connection.send_command("show running-config")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = create_backup_folder(device_name)
        filename = f"{device_name}_backup_{timestamp}.txt"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w") as backup_file:
            backup_file.write(running_config)

        print(f"Backup successful for {device_name}")
        print(f"Saved at: {filepath}")

        connection.disconnect()

    except NetMikoTimeoutException:
        print(f"❌ Timeout Error: Unable to reach {device_name}")

    except NetMikoAuthenticationException:
        print(f"❌ Authentication Failed for {device_name}")

    except Exception as e:
        print(f"❌ Error with {device_name}: {str(e)}")


def main():
    print("===== AutoConfig Backup System Started =====")

    devices = load_devices("devices.yaml")

    for device in devices:
        backup_device(device)

    print("\n===== Backup Process Completed =====")


if __name__ == "__main__":
    main()