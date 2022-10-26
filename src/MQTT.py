#Librerias
import time
import ubinascii
from umqtt.simple import MQTTClient
from machine import unique_id,Pin
import micropython
import network
#Configuración inicial de WiFi
ssid = 'INFINITUMC180_2.4'  #Nombre de la Red
password = 'drFHcKemY4' #Contraseña de la red
wlan = network.WLAN(network.STA_IF)
wlan.active(True) #Activa el Wifi
wlan.connect(ssid, password) #Hace la conexión
while wlan.isconnected() == False: #Espera a que se conecte a la red
    pass
print('Conexion con el WiFi %s establecida' % ssid)
print(wlan.ifconfig()) #Muestra la IP y otros datos del Wi-Fi
#Entradas y salidas
