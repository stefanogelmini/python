import paho.mqtt.client as mqtt
import time

import pymodbus
import serial
from pymodbus.pdu import ModbusRequest
# initialize a serial RTU client instance
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import logging
logging.basicConfig(level="INFO")
log = logging.getLogger()
log.setLevel(logging.INFO)

MQTT_SERVER = "192.168.1.216"
MQTT_TOPIC_ROOT = "/MIRAI/"


# count= the number of registers to read
# unit= the slave unit this request is targeting
# address= the starting address to read from
try:
    client_ModBus = ModbusClient(
        method="rtu",
        port="/dev/ttyUSB0",
        stopbits=1,
        bytesize=8,
        parity='E',
        baudrate=9600)

    client_Mqtt = mqtt.Client("MIRAI-001")

    print("Connecting to MQTT server... ", MQTT_SERVER)

    if client_Mqtt.connect(MQTT_SERVER) == 0:  # connect
	while True:
            # Connect to the serial modbus server
	    connection = client_ModBus.connect()
            # print (connection)
            if connection:
	        result1_start = 8970
		result1_lenght = 62
		result1 = client_ModBus.read_holding_registers(
		result1_start, result1_lenght, unit=0x1)
		result2_start = 9032
		result2_lenght = 62
		result2 = client_ModBus.read_holding_registers(
		result2_start, result1_lenght, unit=0x1)
		result3_start = 16438
		result3_lenght = 62
		result3 = client_ModBus.read_holding_registers(
		result3_start, result1_lenght, unit=0x1)

		result_lenghT = result1_lenght + result2_lenght + result3_lenght
		#print("result_lenghT " + str(result_lenghT))
		Matrix = {}
		Indice = 0
		if result1:

			x = 0
			result1_counter = result1_start
			while (x < len(result1.registers)):
				result1_counter = result1_counter + 1
				topic = MQTT_TOPIC_ROOT + str(result1_counter)
				Matrix[Indice, 1] = topic
				Matrix[Indice, 2] = result1.registers[x]
				Indice = Indice + 1
				# print(topic + "=" + str(result1.registers[x]))
				x = x + 1

		if result2:
			x = 0
			result2_counter = result2_start
			while (x < len(result2.registers)):
				result2_counter = result2_counter + 1
				topic = MQTT_TOPIC_ROOT + str(result2_counter)
				Matrix[Indice, 1] = topic
				Matrix[Indice, 2] = result2.registers[x]
				Indice = Indice + 1
				# print(topic + "=" + str(result2.registers[x]))
				x = x + 1
		if result3:
			x = 0
			result3_counter = result3_start
			while (x < len(result3.registers)):
				result3_counter = result3_counter + 1
				topic = MQTT_TOPIC_ROOT + str(result3_counter)
				Matrix[Indice, 1] = topic
				Matrix[Indice, 2] = result3.registers[x]
				Indice = Indice + 1
				# print(topic + "=" + str(result3.registers[x]))
				x = x + 1

		while (x < len(Matrix) / 2):
		    logging.debug(Matrix[x,1]+"="+str(Matrix[x, 2]))
			#print(Matrix[x,1]+"="+str(Matrix[x, 2]))
		    client_Mqtt.publish(Matrix[x, 1], Matrix[x, 2])
		    x = x + 1
            time.sleep(5)
            client_ModBus.close()
	client_Mqtt.disconnect()


except KeyboardInterrupt:
    print('\n\n Keyboard exception received. Exiting.')
    exit()
