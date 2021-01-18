from CONSTS.CONSTS import UID_LENGTH, USERNAME_MAX_LENGTH
import struct


class User:
    def __init__(self, name, u_id=None, public_key=None, last_seen=None):
        self.name = name
        self.id = u_id
        self.public_key = public_key
        self.last_seen = last_seen
        self.messages = []

    def receiveMessage(self, message):
        self.messages.append(message)

    def pack(self):
        format = "{}s {}s".format(UID_LENGTH, USERNAME_MAX_LENGTH)
        return struct.pack(format, self.id.bytes, bytes(self.name.ljust(255, '\0'), 'utf-8'))

    def pack_messages(self):
        print("Hey")
