import network
import time
from machine import Pin
from dht import DHT11
import ujson
from umqtt.simple import MQTTClient
from utime import sleep_ms
from hcsr04 import HCSR04

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# Configuración de MQTT
mqtt_server = "broker.hivemq.com"
mqtt_topic = "EOI: Movimiento"

# Configuración de los pines
led = Pin(15, Pin.OUT)
sensorDHT = DHT11(Pin(16, pull=Pin.PULL_UP))
sensorhcsr04 = HCSR04(trigger_pin=17, echo_pin=18, echo_timeout_us=10000)

# Conexión MQTT
client = MQTTClient("Blaggdaros", mqtt_server)

def mqtt_callback(topic, msg):
    # Callback para manejar los mensajes MQTT recibidos
    msg = msg.decode()
    topic = topic.decode() 
    if topic == mqtt_topic and float(msg.split()[0]) < 10:
        print(f"Mensaje recibido de {topic}:\n{msg[1::]}")
        # Encender la bombilla cuando se recibe un mensaje MQTT en el topic "EOI: Movimiento"
        led.on()
        sleep_ms(5000)
        led.off()

# Conexión y configuración del cliente MQTT
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(mqtt_topic)

while True:
    client.check_msg()
    sleep_ms(500)
    sensorDHT.measure()
    temp = sensorDHT.temperature()
    hum = sensorDHT.humidity()
    distance = sensorhcsr04.distance_cm()

    # Publicar datos en MQTT
    message = f"{int(distance)} Temperatura: {temp:.2f}, Humedad: {hum:.2f}\nMovimiento detectado: {distance:.2f} cm"
    client.publish(mqtt_topic, message)

    sleep_ms(500)

