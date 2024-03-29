# Embedded System Homework 3

This repository, `embedded_system_hw3`, contains a Python script designed for use on a Raspberry Pi to demonstrate interaction with BLE (Bluetooth Low Energy) devices. The script scans for BLE devices, connects to a selected device, and listens for notifications from the device.

#### Author

電機三B10502139 許禎勻

## Prerequisites

Before running the script, ensure your Raspberry Pi is set up with an internet connection and has Python 3 installed. This project also requires the `bluepy` library for BLE communication.

## Setup and Installation

Follow these steps to set up and run the project on your Raspberry Pi:

1. **Clone the Repository**

    Clone the repository to your Raspberry Pi:

    ```bash
    git clone https://github.com/ianhsu0203/embedded_system_hw3.git

2. **Install Dependencies**

    Update your package list and install Python 3 pip and the required BLE libraries:

    ```bash
    sudo apt update
    sudo apt install python3-pip
    sudo apt install libglib2.0-dev
    sudo pip3 install bluepy
    ```

3. **Run the Script**

    Change to the project directory and run the script:

    ```bash
    cd embedded_system_hw3
    sudo python3 ble_scan_connect.py
    ```

    Note: The `sudo` command is required for `bluepy` to access the BLE hardware.

4. **Select a BLE Device**

    With the BLE advertising tool active on your smartphone, follow the on-screen instructions to select your device from the list of scanned BLE devices.

5. **Receive Notifications**

    Once connected, you can use your smartphone to send notifications to the Raspberry Pi via the BLE connection.

## Acknowledgments

- This project uses the `bluepy` library for communicating with BLE devices.
- Created for the Embedded System course as homework assignment 3.
