import socket
import sys
import tf_lstm as lstm
import _thread as thread

HOST = ''
PORT = 8404

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg)
    sys.exit()

s.listen(0)
print('Socket now listening')

# block until connected
conn, addr = s.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))

m = lstm.Model(100)

while 1:
    sig = conn.recv(1024)
    print(sig)

#    if sig == 'newcurve':
#        data = conn.recv(1024)
#        print(data)
#        thread.start_new_thread(lstm.run, (m, 5, data, "./saved"))

conn.close()

s.close()
