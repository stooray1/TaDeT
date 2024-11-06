import socket
import threading
import time 
'''
First run plc.py then bplc.py (backup PLC) followed by attacker and lastly scada.py
'''

#Use the IP address of your PLC device 
# For communication with SCADA and BPLC 

#PLC_IP = '192.00.00.00'
PLC_IP = '127.0.0.1'
PLC_PORT = 12345

# Define the buffer size for incoming data
BUFFER_SIZE = 1024

#listed of connected clients 
#First one must be BPLC
con_lst = []

#=========================================================================
#sensors 
input_table = [50]
temp_idx = 0 
#actuator
output_table = [10, 0]
v1_idx  = 0
v2_idx  = 1

# to read alll values/symbols from input/output table 
READ_ALL = -1

#Change the following two functions for each case study 

#this logic need update 
def run_plc_logic():
    if input_table[temp_idx] >= 120 : 
        output_table[v1_idx] = 1
    else:
        output_table[v1_idx] = 0


def decode_data(data):
    print(data)
    lst = str(data).split(",")
    size = len(lst)  
    run_logic = True  
    response = "Invalid request"
    #print ("Decode executed ")
    #print(lst)
    

    if(len(lst)==2):
        #write request 
        if lst[0]== "temp" : 
            input_table[temp_idx] = int(lst[1])
            response = "Write successful :"+ data                     
        if lst[0]== "v1" : 
            output_table[v1_idx] = int(lst[1])
            run_logic = False                 
            response = "Write successful (Output table): "+ data                
        if lst[0]== "v2" : 
            output_table[v2_idx] = int(lst[1])
            run_logic = False                 
            response = "Write successful (Output table): "+ data                
        if(run_logic):
            run_plc_logic()
    elif(len(lst)==1):
        #read request 
        
        if lst[0] == "temp" : 
            response = make_read_data("i", temp_idx)                                             
        if lst[0] == "v1" : 
            response = make_read_data("o", v1_idx)
        if lst[0] == "v2" : 
            response = make_read_data("o", v2_idx)
        if lst[0] == "i_table":
            response = make_read_data("i", READ_ALL)
        if lst[0]== "o_table":
            response = make_read_data("o", READ_ALL)

    return response    

#==========================================================================
'''
Print PLC input and output tables 

'''
def print_tables():
    print( "PLC Input table  : ", input_table)            
    print( "PLC Output table : ", output_table)        
    

def make_read_data(tbl, symbol_idx):
    r_data =""
    if(tbl=="i"):
        if(symbol_idx == READ_ALL):
            r_data ="i"
            for x in input_table:             
                r_data +=' '+ str(x)
        elif(symbol_idx>=0 and symbol_idx< len(input_table)):
            r_data=str(input_table[symbol_idx])
    elif (tbl=="o"):
        if(symbol_idx == READ_ALL):
            r_data ="o"
            for x in output_table:             
                r_data +=' '+ str(x)
        elif(symbol_idx>=0 and symbol_idx< len(output_table)):
            r_data=str(output_table[symbol_idx])
    
    return r_data

def encode_table(tbl, symbol_idx):
    r_data =""
    if(tbl=="i"):
        if(symbol_idx == READ_ALL):
            r_data ="i "
            r_data += ' '.join(map(str, input_table))           
        elif(symbol_idx>=0 and symbol_idx< len(input_table)):
            r_data=str(input_table[symbol_idx])
    elif (tbl=="o"):
        if(symbol_idx == READ_ALL):
            r_data ="o "
            r_data += ' '.join(map(str, output_table))  
        elif(symbol_idx>=0 and symbol_idx< len(output_table)):
            r_data=str(output_table[symbol_idx])  
    return r_data

def update_bplc():
    #con_lst is for connection list mean that BPLC is connected 
    if(len(con_lst)> 1): 
        #tbl = make_read_data("i", READ_ALL)
        #con_lst[0].sendall(str.encode(tbl))
        #print(tbl)
        tbl = encode_table("o", READ_ALL)
        con_lst[0].sendall(str.encode(tbl))
        
        
        

def handle_client(client_socket, client_address):
    #client_socket.sendall(str.encode('PLC Connected'))  
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
           break     
        print(f"Received {data.decode()} from {client_address}")
        #start timmer and Process data 
        start_time = time.time()        
        data = data.decode('utf-8')                     
        print("from connected Scada: " + str(data))        
        res = decode_data(str(data))
        time_taken = (time.time() - start_time)
        print("PLC time  (p_t1) in seconds :", time_taken )
        update_bplc() 
        print("...updated BPLC...")                   
        print_tables()  
        client_socket.sendall(str.encode(res))
    client_socket.close()


plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    plc_socket.bind((PLC_IP, PLC_PORT))
except socket.error as e:
    print(str(e))

plc_socket.listen()

# Create a thread function to accept incoming client connections and spawn a new thread to handle each one
def accept_connections():
    print("PLC is listening")
    while True:
        # Accept incoming client connections
        # First connection is from SCADA 
        client_socket, client_address = plc_socket.accept()
        con_lst.append(client_socket)
        client_socket.sendall(str.encode('PLC Connected'))
        if(len(con_lst)>1):
            # Spawn a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()

def plc_server_program():        
    print("This is PLC ")
    print("PLC IP Address :", PLC_IP, " Port #", PLC_PORT)    
    run_plc_logic()
    print_tables()        
    print("=======================================")
    
    # Create a thread to accept incoming client connections
    plc_thread = threading.Thread(target=accept_connections)
    plc_thread.start()
    
    
if __name__ == '__main__':
    plc_server_program()

