
# Tamper DeTection Framework (TaDeT)

This repository contains the code for TaDeT Framework, which includes components such as Programmable Logic Controller (PLC), backup PLC (BPLC), Supervisory Control and Data Acquisition (SCADA), and a Man-in-the-Middle (MitM) adversary.

PLC is responsible for controlling industrial processes through field devices such as sensors and actuators over the "control layer". 
PLC communicates with SCADA system over the "supervision layer" for advanced monitoring and control of the physical processes based on the control commands it receives from SCADA.

Our threat model incorporates an MitM adversary who has access to the supervision layer and aims to perform "control data tampering" (overriding control values leading to unpredictable and unstable responses in the control applications).

Our objective is to detect control data tampering attempts of an MitM adversary by leveraging customary BPLCs that act as fail-over devices for the purpose of availability and resilience. 
Towards this, we add a network module between BPLC and SCADA that act as a parallel computing environment supporting cryptographic hashing operations. 

## Brief Desctiption of Each File

 ### plc.py:
This file contains the main control logic for the PLC server. It establishes a TCP socket and listens for incoming client connections from the SCADA system and BPLC. It handles client requests, processes data, and sends responses back to the SCADA system and updates the process image tables on BPLC. 

### bplc.py:
This file represents the BPLC server. It connects to the primary PLC server and receives data updates from it. 

### scada.py:
This file contains the main logic for the SCADA system. It establishes TCP connections with the PLC and BPLC servers, sends control commands, and receives responses. It also includes functions for data hashing using SHA-256 algorithm to communicate with BPLC.


### attacker.py: 
The attacker program intercepts the communication between the SCADA system and the PLC. It listens for incoming connections from the SCADA system, establishes a connection with the PLC, and forwards the data between them while modifying the control data in transit.


## Prerequisites
To run this code, you need the following:

- Python 3.x
- Basic understanding of networking and socket programming.
- hashlib 

## Usage
Modify the IP addresses of each device. 

- Run the plc.py file to start the PLC server.
- Run the bplc.py file to start the BPLC server.
- Run the attacker program (if applicable) to simulate attacks on the system.
- Run the scada.py file to start the SCADA server.

Note: Make sure to follow the given sequence of steps to ensure proper communication between the components.


# plc.py: PLC Script

This file contains a Python script simulating a **Programmable Logic Controller (PLC)** that communicates with a **SCADA** system and a **Backup PLC (BPLC)**. The PLC processes input sensor data, runs control logic, and communicates with external systems over a network.

## Introduction

This script simulates a **PLC** that:
1. Receives input data (e.g., temperature) from a SCADA system or other clients.
2. Processes the input data using basic control logic.
3. Updates a BPLC with the latest output data.
4. Supports both read and write operations on its process image tables. 
5. For our experiments we used the write operation only

## How It Works

- PLC listens on a specified IP and port, waiting for connections from SCADA and the BPLC.
- PLC processes incoming write requests to updates sensor values or actuator states.
- For read requests, PLC returns current sensor values or actuator states.
- PLC runs the control logic based on input values and updates the output table.
- PLC also synchronizes its output table with the connected BPLC to ensure redundancy.

### Modify IP and Port
Update the IP addresses in the plc.py script based on your network configuration:

PLC_IP: The IP address where PLC will listen.
PLC_PORT: The port number for PLC communication.

### Example Flow:
1. **SCADA** sends a temperature value to PLC.
2. PLC updates its process image table with the new temperature value.
3. PLC sends the updated process image table to BPLC.
5. SCADA can read PLC's process image table at any time.
6. The attacker can tamper the communcation between SCADA and PLC 


# bplcy.py: Backup PLC (BPLC) Script

This file contains a Python script that simulates a **Backup Programmable Logic Controller (BPLC)**. The BPLC is designed to ensure redundancy by mirroring the output data of the primary PLC and verifying the integrity of the received data using hash functions.


## Introduction

The **BPLC** (Backup PLC) works as a fail-safe system, receiving output data from the main PLC and providing backup support in case of failure. Additionally, it ensures the integrity of the communication by verifying the hash of the output values received from the main PLC.

The BPLC:
1. Listens for connections from SCADA.
2. Connects to the main PLC and receives process image table updates.
3. Uses cryptographic hash functions to verify the integrity of the received data.
4. Responds to SCADA's queries to confirm whether the data is tampered or intact.

## How It Works

1. **PLC Connection**: The BPLC connects to the main PLC and listens for updates to the PLC's process image table.
2. **Data Verification**: It processes the received data, executes SHA-256 hash function, and compares the hash values to detect control data tampering.
3. **SCADA Communication**: The BPLC also listens for incoming connections from SCADA, responding to requests with tamper-detection results (i.e., whether the data is valid or tampered).

### Hashing Mechanism
- The BPLC uses the SHA-256 hash function to ensure data integrity.
- When a client (such as SCADA) sends a request, the BPLC compares the hash of the received data with the expected hash to detect any tampering.

# scada.py: SCADA Program

This file contains a Python script that simulates a **Supervisory Control and Data Acquisition (SCADA)** system. The SCADA system communicates with both a **Primary PLC** and a **Backup PLC (BPLC)** to send control commands and verify the integrity of the data using hash functions. It also supports testing in a simulated **Man-in-the-Middle (MitM)** attack environment.

## Introduction

The **SCADA** program allows the control of actuators (such as `v1`) in the PLC system by sending values to the PLC and verifying the data integrity via a hash-based comparison with the Backup PLC (BPLC). It can simulate a MitM attack scenario by modifying the network communication paths.

## How It Works

1. **PLC Communication**: SCADA connects to both the primary PLC and the backup PLC (BPLC). It sends actuator control values (e.g., for `v1`) to the primary PLC.
   
2. **Hashing and Integrity Check**: SCADA generates an SHA-256 hash of the sent data and transmits it to the BPLC for integrity verification. The BPLC compares the received hash with the expected value and reports if the data is tampered.

3. **MitM Simulation**: If MitM simulation is enabled (`SIMULATE_MITM`), SCADA connects to an attacker-controlled intermediary rather than the real PLC.

# attacker.py: Attacker MITM Program

This repository contains a Python script that simulates a **Man-in-the-Middle (MitM)** attack between a **Programmable Logic Controller (PLC)** and a **client** (e.g., SCADA). The adversary intercepts, modifies, and forwards the communication, allowing tampering with the data exchanged between the two parties.

## Introduction

In a **Man-in-the-Middle (MitM)** attack, an adversary intercepts the communication between two parties (in this case, a client and a PLC) to modify or tamper with the exchanged data. This script demonstrates how an adversary can manipulate control data or read responses by acting as an intermediary between the SCADA and PLC.

## How It Works

1. **Interception**: The adversary listens for connections from a client (e.g., SCADA) and establishes a connection with the PLC.
2. **Tampering**: The adversary modifies the data before forwarding it to the intended recipient.
   - **Write requests**: The adversary modifies the data being sent to the PLC, altering actuator control or sensor data.
   - **Read responses**: The adversary modifies the PLC's response before sending it to the client.
3. **Forwarding**: After modification, the tampered data is forwarded to the respective party (either the PLC or the client).

### Example Scenario:
- SCADA sends a write request to PLC to update an actuator value.
- The adversary intercepts this request and modifies the value before forwarding it to PLC.
- When PLC responds with a read request, the adversary intercepts the response, modifies the control data, and sends it to SCADA.


# Disclaimer
This code is for educational and research purposes only. It is coded for specific case studies only. This code does not cover all aspects of a complete PLC system we have implemented only supervision layer. Control layer is not implemented. It may not be suitable for production environments and may require additional security measures and error handling. Use it at your own risk.

