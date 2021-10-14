# Drone Programming
# PlanetBravo

# Import the necessary modules
import threading 
import socket
import time
import subprocess

# Stores the IP and port that the drone transmits video to.
droneEye = 'udp://0.0.0.0:11111'

# Stores the ffmpeg command that captures and processes incoming video from the drone.
command = ['ffmpeg',
           '-i', droneEye,
           '-y',
           'output.mp4']

# Stores the subprocess call which can be used anywhere in the program to start capturing video.
# subprocess.Popen is used to run other apps or commands outside of the Python program.
# In this case we are executing a terminal command that runs ffmpeg in the Termux command line app.
seeMe = subprocess.Popen(command)

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
        print("Sending message: " + message)
    except Exception as e:
        print("Error sending: " + str(e))

# The seeMe process is added inside this function and will be ran when this function in called.
def recvVideo():
    try:
        seeMe
    except Exception as e:
        print('Error: ' + str(e))

# Create thread that receives video that runs in the background
# Notice the instead of calling the recv function, it instead calls the recvVideo function.
recvThread = threading.Thread(target=recvVideo)
recvThread.daemon = True
recvThread.start()

# Give your drone commands by placing code below.
send("command")
time.sleep(5)

send ("takeoff")
time.sleep(5)

#pre-video movement

for i in range(4):
    send ("forward " + str(500))
    time.sleep(10)
send ("forward " + str(450))
time.sleep(10)

# Turns drones video stream on.
send("streamon")
time.sleep(15)

# drone  commands here. 

send ("cw " + str(360))
time.sleep (4)

# Terminates the ffmpeg process that is capturing video.
seeMe.terminate()
time.sleep(6)

# Turns drone's video stream off.
send("streamoff")
time.sleep(5)

for i in range(4):
    send ("back " + str(500))
    time.sleep(10)
send ("back " + str(450))
time.sleep(10)

send ("land") 

# Report mission status
print("Mission completed successfully!")
                   
# Clean-up your open connections by closing them.                 
sock.close()