
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


# plc.py: PLC Script

This file contains a Python script simulating a **Programmable Logic Controller (PLC)** that communicates with a **SCADA** system and a **Backup PLC (BPLC)**. The PLC processes input sensor data, runs control logic, and communicates with external systems over a network.

## Introduction

This script simulates a **PLC** that:
1. Receives input data (e.g., temperature) from a SCADA system or other clients.
2. Processes the input data using basic control logic.
3. Updates a Backup PLC (BPLC) with the latest output data.
4. Supports both read and write operations on its input/output tables. 
5. For our experiments we used only write operation

## How It Works

- The PLC listens on a specified IP and port, waiting for connections from SCADA and the BPLC.
- The PLC processes incoming write requests to update sensor values or actuator states.
- For read requests, the PLC returns current sensor values or actuator states.
- The PLC runs its control logic based on input values and updates the output table.
- The PLC also synchronizes its output table with the connected BPLC to ensure redundancy.

### Modify IP and Port
Update the IP addresses in the plc.py script based on your network configuration:

PLC_IP: The IP address where the PLC will listen.
PLC_PORT: The port number for PLC communication.

### Example Flow:
1. **SCADA** sends a temperature value to the PLC.
2. The PLC updates its internal input table with the new temperature.
3. Based on the temperature, the PLC logic decides whether to open/close a valve (update the output table).
4. The PLC sends the updated output table to the BPLC.
5. The SCADA can read the PLC's current input or output tables at any time.
6. The attacker can tamper the communcation between SCADA and PLC 


# bplcy.py: Backup PLC (BPLC) Script

This repository contains a Python script that simulates a **Backup Programmable Logic Controller (BPLC)**. The BPLC is designed to ensure redundancy by mirroring the output data of the main PLC and verifying the integrity of the received data using hashing techniques.


## Introduction

The **BPLC** (Backup PLC) works as a fail-safe system, receiving output data from the main PLC and providing backup support in case of failure. Additionally, it ensures the integrity of the communication by verifying the hash of the output values received from the main PLC.

The BPLC:
1. Listens for connections from SCADA.
2. Connects to the main PLC and receives output table updates.
3. Uses cryptographic hashing to verify the integrity of the received data.
4. Responds to SCADA's queries to confirm whether the data is tampered or intact.

## How It Works

1. **PLC Connection**: The BPLC connects to the main PLC and listens for updates to the PLC's output table.
2. **Data Verification**: It processes the received data, applies SHA-256 hashing, and compares the hash values to detect any tampering.
3. **SCADA Communication**: The BPLC also listens for incoming connections from SCADA, responding to requests with tamper-detection results (i.e., whether the data is valid or tampered).

### Hashing Mechanism
- The BPLC uses the SHA-256 hashing algorithm to ensure data integrity.
- When a client (such as SCADA) sends a request, the BPLC compares the hash of the received data with the expected hash to detect any tampering.