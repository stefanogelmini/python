#!/usr/bin/python

import minimalmodbus
import time
import subprocess
import datetime
import paho.mqtt.client as mqtt 
import os.path
import socket


rs485 = minimalmodbus.Instrument('/dev/ttyUSB1', 1)
rs485.serial.baudrate = 9600
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
rs485.serial.stopbits = 1
rs485.serial.timeout = 1
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU
#print rs485

MQTT_SERVER= "192.168.1.216"
MQTT_TOPIC_ROOT="/SDM120C/"

try:
    client= mqtt.Client("SDM120C-001")

    print("Connecting to MQTT server... ",MQTT_SERVER)

    if client.connect(MQTT_SERVER)==0:#connect
        

        while True:
            Volts = rs485.read_float(0, functioncode=4, numberOfRegisters=2)
            Current = rs485.read_float(6, functioncode=4, numberOfRegisters=2)
            Active_Power = rs485.read_float(12, functioncode=4, numberOfRegisters=2)
            Apparent_Power = rs485.read_float(18, functioncode=4, numberOfRegisters=2)
            Reactive_Power = rs485.read_float(24, functioncode=4, numberOfRegisters=2)
            Power_Factor = rs485.read_float(30, functioncode=4, numberOfRegisters=2)
            Phase_Angle = rs485.read_float(36, functioncode=4, numberOfRegisters=2)
            Frequency = rs485.read_float(70, functioncode=4, numberOfRegisters=2)
            Import_Active_Energy = rs485.read_float(72, functioncode=4, numberOfRegisters=2) 
            Export_Active_Energy = rs485.read_float(74, functioncode=4, numberOfRegisters=2)
            Import_Reactive_Energy = rs485.read_float(76, functioncode=4, numberOfRegisters=2)
            Export_Reactive_Energy = rs485.read_float(78, functioncode=4, numberOfRegisters=2)
            Total_Active_Energy = rs485.read_float(342, functioncode=4, numberOfRegisters=2)
            Total_Reactive_Energy = rs485.read_float(344, functioncode=4, numberOfRegisters=2)

            print("Publishing... ")
            
                
                
            client.publish(MQTT_TOPIC_ROOT+"Volts",Volts)#publish
            client.publish(MQTT_TOPIC_ROOT+"Current",Current)#publish
            client.publish(MQTT_TOPIC_ROOT+"Active_Power",Active_Power)#publish
            client.publish(MQTT_TOPIC_ROOT+"Reactive_Power",Reactive_Power)#publish
            client.publish(MQTT_TOPIC_ROOT+"Power_Factor",Power_Factor)#publish
            client.publish(MQTT_TOPIC_ROOT+"Phase_Angle",Phase_Angle)#publish
            client.publish(MQTT_TOPIC_ROOT+"Frequency",Frequency)#publish
            client.publish(MQTT_TOPIC_ROOT+"Apparent_Power",Apparent_Power)#publish
            client.publish(MQTT_TOPIC_ROOT+"Import_Active_Energy",Import_Active_Energy)#publish
            client.publish(MQTT_TOPIC_ROOT+"Export_Active_Energy",Export_Active_Energy)#publish
            client.publish(MQTT_TOPIC_ROOT+"Import_Reactive_Energy",Import_Reactive_Energy)#publish
            client.publish(MQTT_TOPIC_ROOT+"Export_Reactive_Energy",Export_Reactive_Energy)#publish
            client.publish(MQTT_TOPIC_ROOT+"Total_Active_Energy",Total_Active_Energy)#publish
            client.publish(MQTT_TOPIC_ROOT+"Apparent_Power",Apparent_Power)#publish
            client.publish(MQTT_TOPIC_ROOT+"Current_Yield",Volts * Current)#publish
            print 'Voltage: {0:.1f} Volts'.format(Volts)
            print 'Current: {0:.1f} Amps'.format(Current)
            print 'Active power: {0:.1f} Watts'.format(Active_Power)
            print 'Apparent power: {0:.1f} VoltAmps'.format(Apparent_Power)
            print 'Reactive power: {0:.1f} VAr'.format(Reactive_Power)
            print 'Power factor: {0:.1f}'.format(Power_Factor)
            print 'Phase angle: {0:.1f} Degree'.format(Phase_Angle)
            print 'Frequency: {0:.1f} Hz'.format(Frequency)
            print 'Import active energy: {0:.3f} Kwh'.format(Import_Active_Energy)
            print 'Export active energy: {0:.3f} kwh'.format(Export_Active_Energy)
            print 'Import reactive energy: {0:.3f} kvarh'.format(Import_Reactive_Energy)
            print 'Export reactive energy: {0:.3f} kvarh'.format(Export_Reactive_Energy)
            print 'Total active energy: {0:.3f} kwh'.format(Total_Active_Energy)
            print 'Total reactive energy: {0:.3f} kvarh'.format(Total_Reactive_Energy)
            print 'Current Yield (V*A): {0:.1f} Watt'.format(Volts * Current)
            time.sleep(5)
        client.disconnect() #disconnect
       

except KeyboardInterrupt:
    print('\n\n Keyboard exception received. Exiting.')
    exit()





