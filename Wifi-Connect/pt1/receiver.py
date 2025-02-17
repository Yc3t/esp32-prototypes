import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
server_address = ('0.0.0.0', 3333)  # Listen on all available interfaces
print(f'Starting UDP server on port {server_address[1]}')
sock.bind(server_address)

try:
    while True:
        # Receive data
        print('\nWaiting to receive message...')
        data, address = sock.recvfrom(4096)
        
        print(f'Received {len(data)} bytes from {address}')
        print(f'Data: {data.decode()}')

except KeyboardInterrupt:
    print('\nClosing socket...')
    sock.close()