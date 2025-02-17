import serial
import time

def test_uart_echo():
    # Configurar la conexión serial
    ser = serial.Serial(
        port='COM19',  
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    print(f"Puerto serial abierto: {ser.name}")
    
    try:
        while True:
            # Obtener entrada del usuario
            message = input("Ingrese mensaje para enviar (o 'q' para salir): ")
            if message.lower() == 'q':
                break

            # Enviar el mensaje
            ser.write(message.encode() + b'\n')  # Agregar carácter de nueva línea
            print(f"Enviado: {message} (bytes: {message.encode() + b'\n'})")

            # Esperar a que llegue el echo
            time.sleep(0.5)

            # Leer la respuesta
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Bytes recibidos: {response}")
                try:
                    decoded = response.decode()
                    print(f"Texto recibido: {decoded}")
                except UnicodeDecodeError:
                    print(f"No se pudo decodificar la respuesta como UTF-8")
            else:
                print("No se recibió respuesta")
                print(f"Configuración serial: {ser.get_settings()}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    
    finally:
        ser.close()
        print("Conexión serial cerrada")

if __name__ == "__main__":
    test_uart_echo() 