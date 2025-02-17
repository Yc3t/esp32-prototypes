import socket
import json
import datetime

def start_udp_server(host='0.0.0.0', port=3333):
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    
    print(f"Iniciando servidor UDP en {host}:{port}")
    sock.bind(server_address)
    
    try:
        while True:
            # Recibir datos
            print("\nEsperando mensaje...")
            data, address = sock.recvfrom(1024)
            
            # Obtener timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\nMensaje recibido de {address} a las {timestamp}")
            try:
                # Decodificar y parsear JSON
                message = json.loads(data.decode())
                
                # Imprimir información formateada
                print("\nInformación del dispositivo:")
                print(f"Número de secuencia: {message['sequence']}")
                print(f"ID del dispositivo: {message['device_id']}")
                print(f"SSID conectado: {message['connected_ssid']}")
                print(f"BSSID del AP: {message['connected_bssid']}")
                print(f"Nivel de señal (RSSI): {message['rssi']} dBm")
                print(f"Dirección IP: {message['ip']}")
                
            except json.JSONDecodeError as e:
                print(f"Error decodificando JSON: {e}")
                print(f"Datos recibidos: {data.decode()}")
                
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
    finally:
        sock.close()

if __name__ == "__main__":
    start_udp_server()