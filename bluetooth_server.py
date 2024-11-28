# bluetooth_server
import bluetooth

# Set up the Bluetooth server
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

print("Waiting for connection...")
client_sock, address = server_sock.accept()
print(f"Connected to {address}")

try:
    while True:
        pulse_data = b'abcd'
        client_sock.send(pulse_data)
        print(f"Sent: {pulse_data}")
except Exception as e:
    print(f"Error: {e}")
finally:
    client_sock.close()
    server_sock.close()
