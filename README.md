
# Tamper Detection Framework

This repository contains the code for the Tamper Detection Framework, which includes components such as Programmable Logic Controller (PLC), backup PLC (BPLC), Supervisory Control and Data Acquisition (SCADA), and an attacker or Man In The Middle (MITM).

The PLC is responsible for controlling industrial processes. It communicates with the SCADA system and performs various operations based on the commands and data it receives. In our simulation, we focus on the I/O Tables and utilize a supervising layer.

The role of the MITM is to tamper with the communication between the SCADA system and the PLC. Our objective is to identify tampering attempts by utilizing the BPLC, which acts as an intermediary between the SCADA system and the PLC and utilizes an encrypted channel for communication.

## Brief Desctiption of Each File

 ### plc.py:
  This file contains the main logic for the PLC server. It establishes a TCP socket and listens for incoming client connections from the SCADA system and BPLC. It handles client requests, processes data, and sends responses back to the SCADA system and update I/O tables on BPLC. 

### bplc.py:
 This file represents the backup PLC server. It connects to the primary PLC server and receives data updates from it. 

### scada.py:
 This file contains the main logic for the SCADA system. It establishes TCP connections with the PLC and BPLC servers, sends commands and data, and receives responses. It also includes functions for data hashing using Sha256 algorithm to communicate with BPLC.


### attacker.py: 
The attacker program intercepts the communication between the SCADA system and the PLC. It listens for incoming connections from the SCADA system, establishes a connection with the PLC, and forwards the data between them while modifying the data in transit.


## Prerequisites
To run this code, you need the following:

- Python 3.x installed on your system.
- The following Python packages: socket, threading, and time.
- hashlib 

## Usage
Modify the IP addresses of Each device. 

- Run the plc.py file to start the PLC server.
- Run the bplc.py file to start the backup PLC.
- Run the attacker program (if applicable) to simulate attacks on the system.
- Run the scada.py file to start the SCADA system.

Note: Make sure to follow the given sequence of steps to ensure proper communication between the components.
