import selectors
import socket
import struct
import uuid
from UserManager.UserManager import UserManager
from CONSTS.CONSTS import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    sel = selectors.DefaultSelector()
    manager = UserManager()


    def accept(sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)


    def read(conn, mask):
        data = conn.recv(REQUEST_HEADER_LENGTH)  # Should be ready
        if data:
            # name_length = len(data) - (REQUEST_HEADER_LENGTH)
            # request_format = "<{}s B B I {}s".format(UID_LENGTH, name_length)
            # client_id_bytes, version, action_code, payload_size, payload = struct.unpack(request_format, data)
            client_id_bytes, version, action_code, payload_size = \
                struct.unpack(REQUEST_FORMAT, data)
            client_id = uuid.UUID(bytes=client_id_bytes)

            #
            if action_code == Actions.Register.value:

                payload = conn.recv(payload_size)
                name = str(payload, 'utf-8')
                uid = manager.add_user(name)
                response = struct.pack(RESPONSE_FORMAT(UID_LENGTH), VERSION, Response_Codes.registration_success.value,
                                       UID_LENGTH, uid.bytes)
                conn.send(response)
            #
            elif action_code == Actions.clients_list.value:
                packed_users = [user.pack() for user in manager.get_other_users(client_id)]
                payload = b"".join(packed_users)
                response = struct.pack(RESPONSE_FORMAT(len(payload)), VERSION, Response_Codes.client_list_success.value,
                                       len(payload), payload)
                print(response)
                conn.send(response)

            elif action_code == Actions.send_message.value:
                message_meta_bytes = conn.recv(MESSAGE_META_LENGTH)
                to_id_bytes, msg_type, msg_length = struct.unpack(MESSAGE_META_FORMAT, message_meta_bytes)
                to_id = uuid.UUID(bytes=to_id_bytes)
                content_bytes = conn.recv(msg_length)
                content = str(content_bytes, 'utf-8')

                msg_id = manager.send_message(client_id, to_id, msg_type, msg_length, content)
                payload = struct.pack(SEND_MESSAGE_RESPONSE_FORMAT, to_id_bytes, msg_id)
                response = struct.pack(RESPONSE_FORMAT(len(payload)), VERSION,
                                       Response_Codes.message_sent_success.value,
                                       len(payload), payload)
                conn.send(response)



            elif action_code == Actions.get_messages.value:
                packed_messages = [message.pack() for message in manager.get_user_messages(client_id)]
                payload = b"".join(packed_messages)
                response = struct.pack(RESPONSE_FORMAT(len(payload)), VERSION, Response_Codes.waiting_messages_success,
                                       len(payload), payload)
                conn.send(response)

        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()


    sock = socket.socket()
    sock.bind(('localhost', 1234))
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
