import select
import socket

from communication import send_data, receive_data, receive_data_udp
from errors import *


class TCPServer():

    def __init__(self):
        self.sending_socket = None

    def input_(self, sock, host, port, address):
        pass

    def output_(self, sock, host, port, address):
        pass

    def connect_(self, sock, host, port, address):
        pass

    def client_connet(self, sock, host, port, address):
        pass

    def client_disconnect(self, sock, host, port, address):
        pass

    def quit_(self, sock, host, port, address):
        pass

    def connect(self, host, port):

        self.host = host
        self.port = port
        try:
            self.unconnected_socket = socket.socket()
            self.unconnected_socket.bind((self.host, self.port))
            self.unconnected_socket.listen(5)
        except:
            self.unconnected_socket.close()
            raise ServerError(
                "Somente uma instância do servidor na porta " + str(self.port) + " pode ser executada ao mesmo tempo!")

        self.connect_(self.unconnected_socket, self.host, self.port)
        self.connected_sockets = []
        self.socketaddresses = {}

    def remove_socket(self, sock):

        address = self.socketaddresses[sock]
        self.client_disconnect(sock, self.host, self.port, address)
        self.connected_sockets.remove(sock)

    def serve_forever(self):

        self.looping = True

        while self.looping:

            input_ready, output_ready, except_ready = select.select([self.unconnected_socket] + self.connected_sockets,
                                                                    [], [])

            for sock in input_ready:
                if sock == self.unconnected_socket:
                    # init socket
                    connected_socket, address = sock.accept()
                    self.connected_sockets.append(connected_socket)
                    self.socketaddresses[connected_socket] = address
                    self.client_connet(connected_socket, self.host, self.port, address)
                else:
                    try:
                        data = receive_data(sock)
                        address = self.socketaddresses[sock]
                        self.input_(sock, self.host, self.port, address)
                    except:
                        data = "client quit"

                    if data != None:
                        if data == "client quit":
                            self.remove_socket(sock)
                            continue
                        self.sending_socket = sock
                        self.handle_data(data)

    def handle_data(self, data):
        pass

    def send_data(self, data, compress=False):
        try:
            send_data(self.sending_socket, data, compress, includelength=True)
            address = self.socketaddresses[self.sending_socket]
            self.output_(self.sending_socket, self.host, self.port, address)
        except:
            self.remove_socket(self.sending_socket)

    def quit(self):
        for sock in self.connected_sockets:
            sock.close()
        self.quit_(self.host.self.port)


class UDPServer():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def input_(self, sock, host, port, address):
        pass

    def output_(self, sock, host, port, address):
        pass

    def connect_(self, sock, host, port):
        pass

    def quit_(self, host, port):
        pass

    def connect(self, host, port):

        self.host = host
        self.port = port

        try:
            self.socket.bind((host, port))
        except:
            self.socket.close()
            raise ServerError(
                "Somente uma instância do servidor na porta " + str(self.port) + " pode ser executada ao mesmo tempo!")

        self.connect_(self.socket, self.host, self.port)

    def serve_forever(self):
        self.looping = True

        while self.looping:
            data, self.lastaddress = receive_data_udp(self.socket)
            self.input_(self.socket, self.host, self.port, self.lastaddress)
            self.handle_data(data)

    def handle_data(self, data):
        pass

    def send_data(self, data, compress=False):

        try:
            send_data(self.socket, data, compress, address=self.lastaddress)
            self.output_(self.socket, self.host, self.port, self.lastaddress)
        except:
            pass  # Client disconnected

    def quit(self):
        self.socket.close()
        self.quit_(self.host, self.port)


class TCPClient():

    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port

        try:
            self.socket = socket.socket()
            self.socket.connect((self.host, self.port))
        except:
            self.socket.close()
            raise SocketError("A conexão não pôde ser aberta. Ela deve ser criada primeiro com um objeto de servidor.")

    def send_data(self, data, compress=False):
        send_data(self.socket, data, compress, includelength=True)

    def wait_for_data(self):

        input_ready, output_ready, except_ready = select.select([self.socket], [], [])
        return receive_data(self.socket)

    def check_for_data(self):
        input_ready, output_ready, except_ready = select.select([self.socket], [], [], 0.001)
        if len(input_ready) > 0:
            return receive_data(self.socket)

    def quit(self):
        self.socket.close()


class UDPClient():
    def __init__(self):
        pass

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((self.host, self.port))

    def send_data(self, data, compress=False):
        send_data(self.socket, data, compress)

    def wait_for_data(self):
        input_ready, output_ready, except_ready = select.select([self.socket], [], [])
        return receive_data_udp(self.socket)[0]

    def check_for_data(self):
        input_ready, output_ready, except_ready = select.select([self.socket], [], [], 0.001)
        if len(input_ready) > 0:
            return receive_data_udp(self.socket)[0]

    def quit(self):
        self.socket.close()
