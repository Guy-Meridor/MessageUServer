from Classes.User import User
from Classes.Message import Message
import uuid

class UserManager:
    def __init__(self):
        self.users = {}
        # For Checks
        self.add_user("YOS")
        self.add_user("SHIRLY")

    def add_user(self, username):
        if [user for user in self.users.values() if user.name == username]:
            raise Exception("user name already exists")

        uid = uuid.uuid1()
        usr = User(username, uid)
        self.users[username] = usr
        print (username, uid, sep=" - ")
        return uid

    def send_message(self, sender_id, receiver_id, content):
        receiver = self.users[receiver_id]
        sender = self.users[sender_id]
        msg = Message(sender, content)
        receiver.receiveMessage(msg)


    def get_other_users(self, client_id):
        return [self.users[id] for id in self.users if id != client_id]