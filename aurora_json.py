import time
import subprocess
import datetime
import paho.mqtt.client as mqtt 
import os.path
import socket
import json
global_STR1P = 0
global_STR2P = 0
global_STRTP = 0
global_DateTimeInverter = ""
global_InverterStatus= ""
MQTT_SERVER= "localhost"
MQTT_TOPIC_WattRealTime = "/Inverter/WattProdottiRealTime"
MQTT_TOPIC_DateTimeStatus = "/Inverter/DateTimeStatus"
MQTT_TOPIC_InverterStatus = "/Inverter/Status"

filename = "/tmp/aurora.out"
args ='/usr/bin/aurora -T -3 -s -c -Y10 -d 0 -a 2 /dev/ttyUSB0 -o ' + filename 

def readData():
    if os.path.exists(filename):
        os.remove(filename) 
    cmd = subprocess.call(args, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(filename):
        arr=[]
        with open(filename,'r') as f:
		for line in f:
			
			fields = map(lambda s: s.strip(), line.split())
                     	
			arr.append({"checkOK": fields[len(fields)-1],"global_DateTimeInverter": fields[0],"global_STR1P": float(fields[3]),"global_STR2P": float(fields[6]),"global_STRTP": float(fields[3])+float(fields[6]),})
			print(arr)
			print(json.dumps(arr, indent=2))
#os.remove(filename) 
#       global global_STR1P
#       global global_STR2P
#       global global_STRTP
#       global global_DateTimeInverter
#       global global_InverterStatus

#       if checkOK == "OK":
#               global_InverterStatus= "Running..."
#               global_DateTimeInverter = data_list[0]
#               global_STR1P = float(data_list[3])
#               global_STR2P = float(data_list[6])
#               global_STRTP = global_STR1P + global_STR2P
#       else:
#               global_InverterStatus= "Sleeping..."
#               global_DateTimeInverter = ""
#               global_STR1P = 0
#               global_STR2P = 0
#               global_STRTP = 0
#try:
#        client= mqtt.Client(socket.gethostname() + "-001")
 
#        while True:
#                readData()
#                print("Connecting to MQTT server... ",MQTT_SERVER)
       
#               if client.connect(MQTT_SERVER)==0:#connect
#                     print("Publishing... ")
#                     client.publish(MQTT_TOPIC_WattRealTime,global_STRTP)#publish
#                     client.publish(MQTT_TOPIC_InverterStatus,global_InverterStatus)#publish
#                     client.disconnect() #disconnect
        #print(global_InverterStatus)
        #print(global_DateTimeInverter)
        #print(global_STRTP)
#        time.sleep(5)
#except KeyboardInterrupt:
#        print('\n\n Keyboard exception received. Exiting.')
#        exit()
try:

	readData()
except:
	exit()
