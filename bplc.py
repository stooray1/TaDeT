import socket
import time 
import threading
import hashlib
from Crypto.Cipher import ChaCha20
from base64 import b64encode
from base64 import b64decode
from Crypto.Util.Padding import pad


from Crypto.Random import get_random_bytes
from codecs import utf_16_be_decode
from Crypto.Util.Padding import  unpad

# Define the buffer size for incoming data
BUFFER_SIZE = 1024


#PLC_IP = '192.168.178.86'
PLC_IP = '192.168.0.101'
#PLC_IP = '127.0.0.1'
PLC_PORT = 12345

#Ip address of BPLC 
#BPLC_IP = '127.0.0.1'
BPLC_IP = '192.168.0.100'
BPLC_PORT = 50015
#sensors 
input_table = [50]
temp_idx = 0 
#actuator
output_table = [1, 0]
v1_idx  = 0
v2_idx  = 1

NO_DATA_IDX = -1
# Encription key 

key = b'Sixteen byte keySixteen byte key'
# encrypted data and nonce separator 
sep =" "

#Comparision Module 
#-----------------For hashing ------------
def compare_bytes(val1, val2):
    if len(val1) != len(val2):
        return False
    for i in range(len(val1)):
        print(val1[i],"--", val2[i])
        if val1[i] != val2[i]:
            return False
    return True

#only considered v1 for experiment to make it work for any
#any actuator change  for each case study 
#this is for write experiment 
def check_tamper_hased_value(val):      
    idx = v1_idx      
    if(len(val)==2):
        res = str(output_table[idx])   
        res = hashSha256(res)
    else:
        #write request 
        #print ("v1 value ",output_table[idx])
        t_val = hashSha256(output_table[idx])
        #change t_val to binary for comparison 
        t_val = t_val.encode('utf-8')       
        if (val == t_val ):            
            res = "No Tampered"
        else:
            res = "TAMPERED "     
    return res

def print_tables():
    print( "PLC Input table  : ", input_table)            
    print( "PLC Output table : ", output_table)        
    

def decode_table(data):
    command = data[0]
    table = input_table if command == 'i' else output_table
    table_index = 0
    value = ''  # Variable to store multi-character value
    for char in data[2:]:  # Start from index 2 to skip the command character and space
        if char.isdigit():
            value += char  # Accumulate digits to form the complete value
        else:
            if value:  # If there's accumulated value, convert and assign to the table
                table[table_index] = int(value)
                table_index += 1
                value = ''  # Reset value for next iteration
    # If there's a remaining value after the loop, convert and assign it to the table
    if value:
        table[table_index] = int(value)


#Hash value 
def hashSha256(data):
    ms = hashlib.sha256()
    ms.update(str(data).encode('utf-8'))
    h = ms.hexdigest()            
    return h

#Process data using hashing 
def process_hashed_data(data):
     
     res = check_tamper_hased_value(data)
     return res

# Define a function to handle incoming client connections
def handle_client(client_socket, client_address):
    print(f"New connection from scada {client_address}")
    while True:
        # Receive incoming data from the client scada
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        # Process the data however you need to here
        #print(f"Received from Scada {data.decode()} from {client_address}")
        start_time = time.time()
        res = process_hashed_data(data)
        time_taken = (time.time() - start_time)
        print("BPLC time  (b_t2) in seconds :", time_taken)     
        print(">>> ",res)   
        client_socket.sendall(res.encode('utf-8'))
        
    # Close the socket when the client disconnects
    print(f"Connection closed from {client_address}")
    client_socket.close()

# Create a TCP socket and bind it to the server's IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((BPLC_IP, BPLC_PORT))
server_socket.listen()

# Create a thread function to accept incoming client connections and spawn a new thread to handle each one
def accept_connections():
    while True:
        # Accept incoming client connections
        client_socket, client_address = server_socket.accept()
        # Spawn a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def plc_connect():
    plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    plc_socket.connect((PLC_IP, PLC_PORT))
    data = plc_socket.recv(BUFFER_SIZE)
    print(f"Received {data.decode()} from the PLC")
    while True:        
        # Receive the response from the server and print it
        data = plc_socket.recv(BUFFER_SIZE)
        if not data:
           break
        #print(f"Received {data.decode()} from the PLC")
        start_time2 = time.time()
        data = data.decode('utf-8')
        decode_table(data)
        time_taken2 = (time.time() - start_time2)        
        print("BPLC time  (b_t1) in seconds :", time_taken2)     
        #print_tables()

def bplc_program():
    print("This is Backup PLC (BPLC)")  

    # Create a thread to to Connect to PLC
    plc_thread = threading.Thread(target=plc_connect)
    plc_thread.start()

    # Create a thread to accept incoming client connections from Scada
    server_thread = threading.Thread(target=accept_connections)
    server_thread.start()

if __name__ == '__main__':
    bplc_program()



   

   
