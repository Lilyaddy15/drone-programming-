# Drone Programming
# PlanetBravo
# Lily Stone

# Import the necessary modules
import threading 
import socket
import time 


# IP and port of Tello
tello_address = ('192.168.10.1', 8889)

# IP and port of local computer
phone = ''
port = 9000
localaddress = (phone,port)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the local address and port
sock.bind(localaddress)


# Send the message to Tello
def send(message):
    try:
        sock.sendto(message.encode(), tello_address)
        print ("Sending message: " + message)
    except Exception as e:
        print ("Error sending, Drone says: " + str(e))
    


# Receive the message from Tello
def recv():
    # Continuously loop and listen for incoming messages
    while True:
        # Try to receive the message. If there is a problem print the exception.
        try:
            response, drone = sock.recvfrom(1518)
            print("Drone says: " + response.decode(encoding="utf-8"))
        except Exception as e:
            sock.close()
            print ("Error receiving, Drone says: " + str(e))
            break

# Create and start a listening thread that runs in the background
# This utilizes our receive functions and will continuously monitor for incoming
recvThread = threading.Thread(target=recv)
recvThread.daemon = True
recvThread.start()

# Give your drone commands by placing code below.
send ("command")
time.sleep(8)

send ("takeoff")
time.sleep(8)

send ("up " + str(50))
time.sleep(8)

send ("forward " + str(100))
time.sleep(8)

send ("back " + str(50))
time.sleep(8)

send ("down " + str(50))
time.sleep(8)

send ("cw " + str(360))
time.sleep(8)

for i in range(2):
    send ("flip f ")
    time.sleep(8)
    
    send ("forward " + str(30))
    time.sleep(8)
    
    send ("flip r ")
    time.sleep(8)
    
    send ("right " + str(30))
    time.sleep(8)
    
    send ("flip b ")
    time.sleep(8)
    
    send ("back " + str(30))
    time.sleep(8)
    
    send ("flip l ")
    time.sleep(8)
    
send ("ccw " + str(360))
time.sleep(8)

send ("land") 


# Report mission status
print("Mission completed successfully!")
                   
#Clean-up your open connections by closing them.                 
sock.close()