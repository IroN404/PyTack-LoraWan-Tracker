import socket, machine, math, os, utime, time, gc, pycom, ubinascii
from L76GNSS import L76GNSS
from network import LoRa
from machine import RTC, SD
from pycoproc_2 import Pycoproc
import binascii

# Initialise LoRa in LORAWAN mode.
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('D765F100FAF4D640C20D6B29FAEF69F0')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
print('Joined')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# Initialize L76GNSS
py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYTRACK:
    raise Exception('Not a Pytrack')

time.sleep(1)
l76 = L76GNSS(py, timeout=30, buffer=512)

pybytes_enabled = False
if 'pybytes' in globals():
    if(pybytes.isconnected()):
        print('Pybytes is connected, sending signals to Pybytes')
        pybytes_enabled = True

while True:
    current_time = utime.localtime()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5])
    coord = l76.coordinates()
    # Extract the GPS data
    latitude = coord[0]
    longitude = coord[1]
    if latitude is not None and longitude is not None:
        # Scale the latitude and longitude values to fit into 3 bytes each
        scaled_latitude = int((latitude + 90) * 10000)  # Scale to fit between 0 and 180
        scaled_longitude = int((longitude + 180) * 10000)  # Scale to fit between 0 and 360
        # Encode the scaled values into bytes
        encoded_data = scaled_latitude.to_bytes(3, 'big') + scaled_longitude.to_bytes(3, 'big')
        print(formatted_time + " : " + "Latitude: {}, Longitude: {}".format(latitude, longitude))
        # Send the encoded data via LoRa
        s.send(encoded_data)
        # 16777216.0
    else:
        print(formatted_time + " : " + "No coordinates have been found, sending sample coordinates")
        latitude = 48.858844
        longitude = 2.2945
        
        latitude_int = int((latitude + 90.0) / 180.0 * 16777215)
        longitude_int = int((longitude + 180.0) / 360.0 * 16777215)
    
        hex_latitude = '{:06X}'.format(latitude_int)
        hex_longitude = '{:06X}'.format(longitude_int)
        print("Latitude: {}, Longitude: {}".format(hex_latitude, hex_longitude))

        pkt = binascii.unhexlify(hex_latitude + hex_longitude)



        s.send(pkt)

        # wait for an incoming packet
        print('Waiting for a packet')
        data = s.recv(64)
        print(data)

    # Wait for some time before getting the next GPS fix
    time.sleep(10)  # Adjust this value based on your desired frequency
