"""Deny Python network sockets in Stage 14 rehearsal processes."""
import socket


def _deny(*_args, **_kwargs):
    raise RuntimeError("Stage 14 offline guard: network access denied")


socket.socket.connect = _deny
socket.socket.connect_ex = _deny
socket.socket.bind = _deny
socket.create_connection = _deny
socket.getaddrinfo = _deny
