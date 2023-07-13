import network
import utime
from credentials import password, ssid
from machine import Pin

# Configurar hardware
led = Pin("LED", Pin.OUT)  # Pin Placa
boton = Pin(0, Pin.IN)

# Conectando a la wifi
led.value(
    0
)  # led inicialmente encendido para indicar que nos estamos intentando conectar a la wifi
print("\nConectando a {} ...".format(ssid), end="")
red = network.WLAN(network.STA_IF)
red.active(True)
# red.scan()  # Escanea y te muestra redes disponibles
red.connect(ssid, password)
# while not red.isconnected():  # Espera hasta que este conectado
# utime.sleep(0.1)
print("conectado!")
print(red.ifconfig())  # ver la ip que se nos ha asignado por DHCP
led.value(1)  # apagamos led para indicar que ya estamos conectados
utime.sleep(1)
led.value(0)
