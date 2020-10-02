import logging

from server import UserHandler
from server.User import User


# def getData(mass) :
#     print(mass.decode("utf-8"))

class CommandHandler(object):
    commands = {}

    msgs = {
        0: "permission denied",
        1: "command not found",
        2: "bad argument"
    }

    def send_msg(self, data):
        self.conn.send(data.encode())
        return
# timeout пакетами ответ от клиента.
    def read_protokol(self, conn_):
        size = int(conn_.recv(10).decode("utf-8"))
        data = ""
        print("size:", size)
        while size > 0:
            newdata = conn_.recv(size if size <= 1024 else 1024).decode("utf-8")
            size -= 1024
            print("read:", newdata)
            data = data + newdata
        print("i'm read: " + data)
        return data

    def send_data(self, msg):
        size = len(msg)
        self.conn.send((str(size)).encode())
        while not size == 0:
            self.conn.send(msg[:1024].encode())
            msg = msg[1024:]
            size = int(size / 1024)

    def __init__(self, conn_, adr_):
        msg = self.read_protokol(conn_)
        print(msg)
        login, password = msg.split()
        perm = UserHandler.check_user(login, password)
        if perm >= 0:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " successful login " + login)
            self.user = User(adr_, login, perm)
            self.conn = conn_
            self.adr = adr_
            self.start()
        else:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " failed login " + login)
            if perm == -1:
                conn_.send("wrong data".encode())
            elif perm == -2:
                conn_.send("user already use".encode())

            conn_.send("disconnect".encode())
            conn_.shutdown(1)

    def start(self):
        self.commands["logout"] = [0, self.logout, "- разлогиниться."]
        self.commands["mkdir"] = [1, self.mkdir, " <dirname> - создать директорию с именем dirname."]
        self.commands["ls"] = [0, self.ls, " [dirname] - посмотреть информацию о директории."]
        self.commands["help"] = [0, self.logout, None]
        self.commands["write"] = [1, self.logout, " <file> [text] - записать в file следующий текст. "
                                                  "Если файл не существует, то он будет содан."]
        self.commands["read"] = [1, self.logout, " <file> - считать файл."]
        self.commands["reg"] = [2, self.logout, " <login> <password> - зарегистрировать."]
        self.commands["del"] = [2, self.logout, " <login> - удалить пользователя."]
        self.commands["passchange"] = [2, self.logout, " <login> <password> - заменить текущий пароль пользователя "
                                                       "на предоставленный."]
        self.commands["list"] = [2, self.logout, " - информация о пользователях."]
        UserHandler.set_activity(self.user.name)
        self.conn.send("successful login!".encode())
        while 1:
            result = self.handler()
            if result == -1:
                break

    def handler(self):
        # data = self.conn.recv(1024).decode()
        data = self.read_protokol(self.conn)
        command = self.commands[data.split()[0]]
        logging.debug("get command :" + data.split()[0])
        if command[0] > self.user.perm:
            self.send_msg(self.msgs[0])
            return 0
        return command[1](data)

    def logout(self, data):
        logging.debug(self.user.name + " logout.")
        self.send_msg("U logout")
        self.send_msg("disconnect")
        UserHandler.stop_activity(self.user.name)
        self.conn.close()
        return -1

    def mkdir(self, data):

        pass

    def ls(self, data):
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
