# PyPortScanner

A simple and efficient port scanner written in Python.

## Description

PyPortScanner is a command-line tool that allows you to scan open ports on a single host or across an entire network range. It uses multithreading to speed up the scanning process and provides colorful output to easily identify open and closed ports.

## Features

- Scan ports on a single host or an IP range (CIDR notation supported)
- Multithreaded scanning for faster results
- Clear, color-coded terminal output for better readability
- Detects open ports and reports progress in real-time
- Handles keyboard interruptions gracefully

## Requirements

- Python 3.x
- No external libraries required (only built-in Python modules)

## Usage

1. Clone or download this repository:
   git clone https://github.com/BitNox01/PyPortScanner.git
   cd PyPortScanner
2. Run the scanner script:
     python main.py

3. Follow the on-screen prompts to:
   -Choose whether to scan a network range or localhost
   -Enter the network range in CIDR notation (if applicable)
   -Enter the port range to scan

## Example
 Choose an option:
 [1] Scan a network range
 [2] Scan localhost
 Enter 1 or 2: 2
 Local IP detected: 192.168.1.10
 Enter start port (1-65535): 1
 Enter end port (>= start port): 1024
 Scanning localhost 192.168.1.10...
 [+] Port 22 is open on 192.168.1.10
 ...

## License
 This project is licensed under the MIT License.

# Created by BitNox



