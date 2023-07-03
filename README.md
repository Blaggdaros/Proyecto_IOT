# Proyecto_IOT
Ejercicio consistente en  montar un sistema de domótica con 2 sensores temperatura/humedad y sensor de ultrasonidos, el cual envié los datos recogidos mediante protocolo MQTT.

Más concretamente:
- Para el sensor de temeperatura y humedad, enviar la información usando el protocolo MQTT.
- Por otro lado, para el caso del sensor de ultrasonidos, medir la distancia y envie una señal usando el protocolo MQTT cuando esta sea inferior a 10cm.
- Por otra parte, conectar el microcontrolador a los eventos enviados por MQTT para alertar del movimiento encendiendo un LED durante 5 segundos.. Además 
  mostrar usando print los valores de humedad y temperatura.
