from enum import IntEnum
class Actions(IntEnum):
    Exit = 0,
    Register = 100,
    clients_list = 101,
    pkey = 3,
    get_messages = 4,
    send_message = 5,
    request_symetric_key = 51,
    send_symetric_key = 52

VERSION = 1
MAX_LENGTH = 1024
UID_LENGTH = 16
USERNAME_MAX_LENGTH = 255
# client uid, version, code, payload size
REQUEST_HEADER_LENGTH = UID_LENGTH + 1 + 1 + 4

# version, code, payload size
RESPONSE_FORMAT = lambda payload_size: "B H I {}s".format(payload_size)
