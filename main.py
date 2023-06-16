import cv2
import socket
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('Host IP:', host_ip)
port = 1234
socket_address = (host_ip, port)

server_socket.bind(socket_address)
server_socket.listen(5)
print("Listening for incoming connections...")

client_socket, addr = server_socket.accept()
print('Connected to:', addr)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    serialized_frame = pickle.dumps(frame)
    message = struct.pack("Q", len(serialized_frame)) + serialized_frame
    client_socket.sendall(message)
    cv2.imshow('Server - Sending', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
server_socket.close()
