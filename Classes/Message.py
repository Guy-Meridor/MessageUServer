from CONSTS.CONSTS import UID_LENGTH, USERNAME_MAX_LENGTH
import struct

class Message:
    counter = 1

    def __init__(self, from_client, Type, size, content):
        self.from_client = from_client
        self.content = content
        self.size = size
        self.Type = Type

        self.id = Message.counter
        Message.counter += 1

    def pack(self):
        format = "I B I {}s".format(self.size)
        return struct.pack(format, self.id, self.Type, self.size,
                           bytes(self.content, 'utf-8'))
