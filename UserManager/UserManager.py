from Classes.User import User
from Classes.Message import Message
import uuid


class UserManager:
    def __init__(self):
        self.users = {}

        # for checks
        # self.add_user("YOS")
        # self.add_user("SHIRLY")
        #
        #
        # guyid = uuid.UUID("fd3401f1-5b44-11eb-be77-a434d938b306")
        # guy = User("GuyM", guyid)
        # self.users[guyid] = guy
    #
    #     muid = uuid.UUID("847bd5be-5b27-11eb-ae5c-a434d938b306")
    #     m = User("M", muid)
    #     self.users[muid] = m
    #
    #
    #     self.receive_welcome_messages(guyid)
    # #     end checks

    def add_user(self, username):
        if [user for user in self.users.values() if user.name == username]:
            raise Exception("user name already exists")

        uid = uuid.uuid1()
        usr = User(username, uid)
        self.users[uid] = usr

        print(usr.id, usr.name, sep=" - ")
        return uid

    def send_message(self, sender_id, receiver_id, Type, size, content):
        receiver = self.users[receiver_id]
        sender = self.users[sender_id]
        msg = Message(sender, Type, size, content)
        receiver.receiveMessage(msg)

        print (sender.name, "sent ", msg.content, "to ", receiver.name)
        return msg.id

    def get_other_users(self, client_id):
        print([uid for uid in self.users])
        return [self.users[uid] for uid in self.users if uid != client_id]

    def get_user_messages(self, client_id):
        return self.users[client_id].messages

    def receive_welcome_messages(self, client_id):
        # Get messages from old clients (checks)
        for user in self.get_other_users(client_id):
            content = "Hey, Im {}".format(user.name)
            self.send_message(user.id, client_id, 1, len(content), content)
        #
