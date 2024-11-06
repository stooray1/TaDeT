import socket
import time
import hashlib
from base64 import b64encode
from base64 import b64decode
from pprint import pprint as pp

#To simulate MITM/attacker  use this 
SIMULATE_MITM = True

PLC_IP   = '127.0.0.1'
PLC_PORT = 0

#Update IP address for your devices 
if(SIMULATE_MITM):
    print("Simulating MITM/attacker ")
    #Attacker(MITM) target address and port 
    #PLC_IP = '192.00.00.00'    
    PLC_IP   = '127.0.0.1'
    PLC_PORT = 23456
else:
    print("NO MITM/attacker ")
    #PLC target address and port 
    #PLC_IP = '192.168.178.86'
    PLC_IP = '127.0.0.1'       
    PLC_PORT = 12345

#BPLC target address and port 
#BPLC_IP = "192.00.00.00"
BPLC_IP = "127.0.0.1"
BPLC_PORT = 50015

# Define the buffer size for incoming data
BUFFER_SIZE = 1024

# d time (in Sec) between sending data to PLC and BPLC
d_time=0.011


def hashSha256(data):
    ms = hashlib.sha256()
    ms.update(str(data).encode('utf-8'))
    h = ms.hexdigest()            
    return h

def scada_client_program():
    

    PLCClient = socket.socket()
    print("This is SCADA")
    print('Waiting for connection response')
    try:
        PLCClient.connect((PLC_IP, PLC_PORT))
    except socket.error as e:
        print(str(e))
    res = PLCClient.recv(1024)
    print(res.decode('utf-8')) 

    BPLCClient = socket.socket()
    try:
        BPLCClient.connect((BPLC_IP, BPLC_PORT))
    except socket.error as e:
        print(str(e))

       
    print("d (in sec)", d_time)
    #this  loop is to n time change actuator value 


    '''
    w_tbl=["v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50",
           "v1,10","v1,20","v1,30","v1,40", "v1,50"]
    '''
    #values for v1 using hash 
    w_tbl=["10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50",
           "10","20","30","40", "50"]
    

    delay = 2.0
    print("---Write Experiment ---")
    print(w_tbl)
    #Write Experiment 
    for data in w_tbl:
        print(data)                
        PLCClient.send(str.encode("v1,"+data))
        time.sleep(d_time)
        start_time = time.time()
        #data_en = encrypt(data)        
        hash_data = hashSha256(data)
        #print("hash data" + hash_data)
        #BPLCClient.sendall(str.encode(hash_data),)
        BPLCClient.sendall(str.encode(hash_data),)
        time_taken = (time.time() - start_time)
        print("Scada time  (s_t1) in seconds :", time_taken ) 
        res = PLCClient.recv(BUFFER_SIZE)              
        print("PLC rs: "+res.decode('utf-8'))
        res = BPLCClient.recv(BUFFER_SIZE)
        print("BPLC rs: "+res.decode('utf-8'))
       
        time.sleep(delay)
    
    
    print("=========Experiment run Successfully============")        
    PLCClient.close()
    BPLCClient.close()


if __name__ == '__main__':
    scada_client_program()