# bluetooth_client
import bluetooth
serverAddress = "XX:XX:XX:XX:XX:XX"  #Pi 1's MAC
port = 1

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    client_sock.connect((serverAddress, port))
    print("Connected to server")

    # Continuously receive data
    while True:
        data = client_sock.recv(1024)
        if data:
            print(f"Received: {data.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
finally:
    client_sock.close()
