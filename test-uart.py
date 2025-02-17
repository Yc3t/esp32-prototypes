import serial
import time

# Configurar el puerto serie
ser = serial.Serial(
    port='COM11',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def send_and_receive(message):
    # Enviar mensaje
    ser.write(message.encode())
    time.sleep(0.1)  # Pequeña pausa para asegurar la recepción
    
    # Leer respuesta
    if ser.in_waiting:
        response = ser.read(ser.in_waiting)
        return response.decode()
    return None

try:
    while True:
        # Enviar mensaje de prueba
        message = "Hola ESP32!\n"
        print(f"Enviando: {message}")
        
        response = send_and_receive(message)
        if response:
            print(f"Recibido: {response}")
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Programa terminado por el usuario")
    ser.close()
