import logging

from server import UserHandler
from server.User import User


class CommandHandler(object):
    commands = {}

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
        self.logout()

        self.commands["logout"] = [0, self.logout(), "- разлогиниться."]
        self.commands["mkdir"] = [1, self.mkdir(), " <dirname> - создать директорию с именем dirname."]
        self.commands["ls"] = [0, self.ls(), " [dirname] - посмотреть информацию о директории."]
        self.commands["help"] = [0, self.logout(), None]
        self.commands["write"] = [1, self.logout(), " <file> [text] - записать в file следующий текст. "
                                                    "Если файл не существует, то он будет содан."]
        self.commands["read"] = [1, self.logout(), " <file> - считать файл."]
        self.commands["reg"] = [2, self.logout(), " <login> <password> - зарегистрировать."]
        self.commands["del"] = [2, self.logout(), " <login> - удалить пользователя."]
        self.commands["passchange"] = [2, self.logout(), " <login> <password> - заменить текущий пароль пользователя "
                                                         "на предоставленный."]
        self.commands["list"] = [2, self.logout(), " - информация о пользователях."]
        UserHandler.set_activity(self.user.name)
        self.conn.send("top".encode())
        while 1:
            result = self.handler()
            if result == -1:
                break

    def handler(self):
        data = self.conn.recv(1024)
        self.commands[data.decode()]

    def logout(self):
        pass

    def mkdir(self):

        pass

    def ls(self):
        pass

    def help(self):
        pass

    def write(self):
        pass

    def read(self):
        pass

    def reg_user(self):
        pass

    def del_user(self):
        pass

    def change_pass(self):
        pass

    def list_user(self):
        pass
