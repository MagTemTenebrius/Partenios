import logging
import os

from server import UserHandler
from server.User import User
from pathlib import Path


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
        return self.send_data(data)

    # timeout пакетами ответ от клиента.
    def read_protokol(self, conn_):
        try:
            size = int(conn_.recv(10).decode("utf-8"))
        except ConnectionResetError:
            UserHandler.stop_activity(self.user.name)
            logging.debug(self.user.name + " logout.")
            return -1
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
        size = len(msg.encode())
        self.conn.send((str(size)).encode())
        while not size == 0:
            print("send", msg[:1024])
            self.conn.send(msg[:1024].encode())
            msg = msg[1024:]
            size = int(size / 1024)

    def __init__(self, conn_, adr_):
        self.conn = conn_
        self.adr = adr_
        msg = self.read_protokol(conn_)
        print(msg)
        try:
            login, password = msg.split()
        except ValueError:
            print("Bad par")
            self.send_msg("killed")
            conn_.shutdown(1)
            return
        perm = UserHandler.check_user(login, password)
        if perm >= 0:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " successful login " + login)
            Path("./users/" + login).mkdir(parents=True, exist_ok=True)
            self.user = User(adr_, login, perm)
            self.start()
        else:
            logging.debug("User " + adr_[0] + ":" + str(adr_[1]) + " failed login " + login)
            if perm == -1:
                self.send_msg("wrong data")
            elif perm == -2:
                self.send_msg("user already use")

            self.send_msg("killed")
            conn_.shutdown(1)

    # reg, try ex
    def start(self):
        self.commands["logout"] = [0, self.logout, "- разлогиниться."]
        self.commands["ls"] = [0, self.ls, " [dirname] - посмотреть информацию о директории."]
        self.commands["help"] = [0, self.help, " [command] - помощь по команде"]
        self.commands["pwd"] = [0, self.pwd, " - текущая директория"]

        self.commands["mkdir"] = [1, self.mkdir, " <dirname> - создать директорию с именем dirname."]
        self.commands["write"] = [1, self.write, " <file> [text] - записать в file следующий текст. "
                                         "Если файл не существует, то он будет содан."]
        self.commands["read"] = [1, self.read, " <file> - считать файл."]

        self.commands["reg"] = [2, self.reg_user, " <login> <password> - зарегистрировать."]
        self.commands["del"] = [2, self.del_user, " <login> - удалить пользователя."]
        self.commands["passchange"] = [2, self.change_pass,
                                       " <login> <password> - заменить текущий пароль пользователя "
                                       "на предоставленный."]
        self.commands["list"] = [2, self.list_user, " - информация о пользователях."]
        UserHandler.set_activity(self.user.name)
        self.send_msg("successful login!")
        while 1:
            result = self.handler()
            if result == -1:
                break

    def handler(self):
        # data = self.conn.recv(1024).decode()
        data = self.read_protokol(self.conn)
        if data == -1:
            return -1
        if not data.split()[0] in self.commands:
            self.send_msg("wrong command")
            return 0

        command = self.commands[data.split()[0]]
        # logging.debug("get command :" + data.split()[0])
        if command[0] > self.user.perm:
            self.send_msg(self.msgs[0])
            return 0
        return command[1](data)

    def logout(self, data):
        logging.debug(self.user.name + " logout.")
        # self.send_msg("U logout")
        self.send_msg("disconnect")
        UserHandler.stop_activity(self.user.name)
        self.conn.close()
        return -1

    def mkdir(self, data):

        pass

    def ls(self, data):
        path = ""
        start_path = "c:\\Tenebrius\\Univer\\mbks\\users\\" + self.user.name + "\\"
        if len(data.split()) > 1:
            path = data.split()[1]
        # if not os.path.abspath(path).startswith()
        # os.listdir()
        abs_path = os.path.abspath(start_path + path)
        if not abs_path.startswith(start_path) and self.user.perm < 5:
            self.send_msg(self.msgs[0])
            return
        self.send_msg(str(os.listdir(abs_path)))
        return
        # logging.debug(self.user.name + ": " + data)
        pass

    def help(self, data):
        if len(data.split()) == 1:
            command = "help"
        else:
            command = data.split()[1]
        command_el = self.commands[command]
        # logging.debug("get command :" + data.split()[0])
        if command_el[0] > self.user.perm:
            self.send_msg(self.msgs[0])
            return 0
        self.send_msg(command + command_el[2])
        return

    def write(self, data):
        start_path = "c:\\Tenebrius\\Univer\\mbks\\users\\" + self.user.name + "\\"
        if len(data.split()) > 3:
            path = data.split()[1]
            abs_path = os.path.abspath(start_path + path)
            if not abs_path.startswith(start_path) and self.user.perm < 5:
                self.send_msg(self.msgs[0])
                return
            with open(start_path + path, "a") as file:
                file.write(data[(len(data.split()[0]) + len(data.split()[1]) + 2):])
                file.close()
            return
        self.send_msg(self.msgs[2])
        return

    def read(self, data):
        start_path = "c:\\Tenebrius\\Univer\\mbks\\users\\" + self.user.name + "\\"
        if len(data.split()) > 1:
            path = data.split()[1]
            abs_path = os.path.abspath(start_path + path)
            if not abs_path.startswith(start_path) and self.user.perm < 0:
                self.send_msg(self.msgs[0])
                return
            try:
                with open(start_path + path, "r") as file:
                    text = file.read()
                    file.close()
                    self.send_msg(text)
            except FileNotFoundError:
                self.send_msg("FNF")
            return
        self.send_msg(self.msgs[2])
        return

    def reg_user(self, data):
        if len(data.split()) != 3:
            self.send_msg("bad arg")
            return
        a, login, password = data.split()
        if UserHandler.create_user(login, password):
            self.send_msg("ok")
        else:
            self.send_msg("err")
        pass

    def del_user(self, data):
        if len(data.split()) != 2:
            self.send_msg("bad arg")
            return
        a, login = data.split()
        if UserHandler.delete_user(login):
            self.send_msg("ok")
        else:
            self.send_msg("err")
        pass

    def change_pass(self, data):
        if len(data.split()) != 3:
            self.send_msg("bad arg")
            return
        a, login, newpass = data.split()
        if UserHandler.pasasword_change(login, newpass):
            self.send_msg("ok")
        else:
            self.send_msg("err")
        pass

    def list_user(self, data):
        self.send_msg(UserHandler.list())
        pass

    def pwd(self, data):
        start_path = "c:\\Tenebrius\\Univer\\mbks\\users\\" + self.user.name + "\\"
        self.send_msg(start_path)
        return
