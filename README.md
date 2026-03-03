# AutoConfig Backup System

AutoConfig Backup System is a Python-based network automation tool
designed to automatically back up configurations from multiple Cisco
devices.

This project demonstrates network automation, structured inventory
management, and secure credential handling using environment variables.

The system supports both real lab devices and simulated mock
configurations for safe public demonstrations.

------------------------------------------------------------------------

## Problem Statement

In enterprise networks, configuration changes happen frequently.

Without centralized automated backups:

-   Configuration loss can occur during device failure
-   Manual errors may go unnoticed
-   Recovery during outages becomes slow
-   Compliance auditing becomes difficult

This project solves that by automating secure configuration backups in a
structured and reliable way.

------------------------------------------------------------------------

## Features

-   Multi-device support via YAML inventory
-   SSH-based device connection using Netmiko
-   Timestamped configuration backups
-   Device-wise organized backup folders
-   Secure credential handling using environment variables
-   Mock fallback mode for demo and privacy-safe usage
-   Clean, modular, and production-style code structure

------------------------------------------------------------------------

## Installation

Install required dependencies:

pip install netmiko pyyaml python-dotenv

------------------------------------------------------------------------

## Configuration

### 1. Edit `devices.yaml`

Add your lab devices:

devices: - name: R1 device_type: cisco_ios host: 192.168.100.10

### 2. Create `.env` file (Recommended)

NET_USERNAME=labuser\
NET_PASSWORD=labpassword\
NET_SECRET=labsecret

Add `.env` to `.gitignore`.

------------------------------------------------------------------------

## Usage

Run the script:

python backup.py

Backups will be stored in:

backups/`<device_name>`{=html}/

------------------------------------------------------------------------

## Privacy & Security

-   No production IPs are included
-   Credentials are managed using environment variables
-   Supports mock configuration fallback for public demo environments
-   Designed for safe GitHub sharing

------------------------------------------------------------------------

## Technologies Used

-   Python
-   Netmiko
-   PyYAML
-   python-dotenv
-   SSH Automation

------------------------------------------------------------------------

## Future Enhancements

-   Configuration change detection (diff engine)
-   Email alert notifications
-   Logging system
-   Scheduled automated backups
-   Web-based dashboard interface

------------------------------------------------------------------------

