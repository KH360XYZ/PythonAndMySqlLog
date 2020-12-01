import serial							#Import libraries
import time
from datetime import datetime
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
import mysql.connector

ADAFRUIT_IO_USERNAME = "Kasper_Holen"
ADAFRUIT_IO_KEY = "aio_IIVQ43BNwYsRdgLdUyqp5VZXO0RD"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
board = pyfirmata.Arduino('COM7')
it = pyfirmata.util.Iterator(board)
it.start()
digital_output = board.get_pin('d:13:o')
analog_input = board.get_pin('a:1:i')
analog_read = analog_input.read()
s = 1

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root",
	database="t"
)
mycursor = mydb.cursor(buffered=True)
print ("Connected..")

try:
	digital = aio.feeds('digital')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)
run_count = 0	
while True:
	print (analog_read)
	sql = "INSERT INTO temp(temp,time) VALUES (%s,%s)"
	tid = datetime.now()
	print (tid)
	val = (analog_input.read(), tid)
	print (val)
	print(mycursor.rowcount, "Record inserted in log table")
	mycursor.execute(sql, val)
	mycursor.execute("SHOW DATABASES;")
	print (digital_output.read())
	#potmeter1 = board.get_pin('a:5:i')
	print('Sending count:', run_count)
	run_count += 1
	time.sleep(10)
	aio.send_data('counter', run_count)
	print(analog_input.read())
	aio.send_data('potmeter', analog_input.read())
	#aio.send_data('xpotmeter1', potmeter1)
	data = aio.receive(digital.key)
	print('Data: ', data.value)
	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

time.sleep(3)
