from machine import Pin
from dht import DHT11
import ujson
from umqtt.simple import MQTTClient
from utime import sleep_ms
from hcsr04 import HCSR04

# Configuración de MQTT
mqtt_server = "broker.hivemq.com"
mqtt_topic = "EOI: Temperatura y Humedad"

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
    print(f"Mensaje recibido de {topic}: ", msg)
    if topic == "EOI: Movimiento":
        # Encender la bombilla cuando se recibe un mensaje MQTT en el topic "EOI: Movimiento"
        led.on()
        sleep_ms(2000)
        led.off()

# Conexión y configuración del cliente MQTT
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(mqtt_topic)
client.subscribe("EOI: Movimiento")

while True:
    client.check_msg()
    sleep_ms(500)
    sensorDHT.measure()
    temp = sensorDHT.temperature()
    hum = sensorDHT.humidity()
    print(f"T={temp:.2f} ºC, {hum:.2f}")

    # Publicar datos de temperatura y humedad en MQTT
    client.publish(mqtt_topic, f"Temperatura: {temp:.2f}, Humedad: {hum:.2f}")

    distance = sensorhcsr04.distance_cm()
    print(f"Distancia: {distance:.2f} cm")

    if distance < 10:
        # Enviar señal MQTT cuando la distancia es inferior a 10 cm
        client.publish("EOI: Movimiento", f"Movimiento detectado: {distance:.2f}")

    sleep_ms(500)