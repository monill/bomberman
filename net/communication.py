import pickle
import zlib

from errors import *


def encode_data(data, compress):
    data = pickle.dumps(data)

    if compress != False:
        data = zlib.compress(data, compress)

    length = str(len(data))
    length = ("0" * (8 - len(length))) + length
    return length, data


def decode_data(data):
    try:
        data = pickle.loads(data)
    except:
        data = pickle.loads(zlib.decompress(data))
        return data


def send_data(sock, data, compress, include_length=False, address=None):
    length, data = encode_data(data, compress)

    if include_length:
        data = length + data

    if len(data) > 1024:
        print("Aviso: pacotes são grandes.")

    try:
        if address != None:
            sock.sendto(data, address)
        else:
            sock.send(data)
    except:
        sock.close()
        raise SocketError("A conexão está interrompida; não foi possível enviar dados!")


def receive_data(sock):
    try:
        length = int(sock.recv(8))
        data = sock.recv(length)
    except:
        sock.close()
        raise SocketError("A conexão está interrompida; dados não puderam ser recebidos!")
    data = decode_data(data)
    return data


def receive_data_udp(sock, size=1024):
    try:
        data, address = sock.recvfrom(size)
    except:
        sock.close()
        raise SocketError("A conexão está interrompida; dados não puderam ser recebidos!")
    data = decode_data(data)
    return data, address
