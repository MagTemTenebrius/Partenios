import logging

from server import UserHandler
from server.User import User


class CommandHandler(object):

    def __init__(self, conn_, adr_):
        data = conn_.recv(1024)
        # print(data.decode("utf-8"))
        login, password = data.decode("utf-8").split()
        perm = UserHandler.check_user(login, password)
        if not perm == 0:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " successful login " + login)
            self.user = User(adr_, login, perm)
            self.conn = conn_
            self.adr = adr_
            self.start()
        else:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " failed login " + login)
            conn_.send("wrong data".encode())
            conn_.shutdown(1)

    def start(self):
        self.conn.send("top".encode())
        # while 1:

        # data = conn.recv(1024)
        # print(data.decode("utf-8"))
