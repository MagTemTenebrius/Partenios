import json
import logging
import hashlib


def init():
    with open('users.json', 'r') as file:
        logging.info("Users db loading...")
        init.data_users = json.load(file)
        logging.debug("Users: ")

        for user in init.data_users["users"]:
            logging.debug('\t' + user["login"] + ":" + user["pass"] + " \tperm=" + str(user["perm"]))
        logging.info("User database loading completed!")


def check_user(login, password):
    password_hash = hashlib.md5(password.encode())
    logging.debug("Pass hash:" + password_hash.hexdigest())
    for i in init.data_users["users"]:
        if i["login"] == login:
            if i["pass"] == password_hash.hexdigest():
                return i["perm"]
            else:
                return 0
    return 0


def get_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            return i["activity"] if "activity" in i else False
    return False


def set_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["activity"] = True


def stop_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["activity"] = False
