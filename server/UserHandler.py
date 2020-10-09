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
    if get_activity(login):
        return -2
    password_hash = hashlib.md5(password.encode())
    logging.debug("Pass hash:" + password_hash.hexdigest())
    for i in init.data_users["users"]:
        if i["login"] == login:
            if i["pass"] == password_hash.hexdigest():
                return i["perm"]
            else:
                return -1
    return -1


def get_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            return i["activity"] if "activity" in i else False
    return False


def set_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["activity"] = True


def create_user(login, password):
    for i in init.data_users["users"]:
        if i["login"] == login:
            return False
    a = {}
    a["login"] = login
    a["pass"] = hashlib.md5(password.encode()).hexdigest()
    a["perm"] = 0
    a["activity"] = False
    init.data_users["users"].append(a)
    return True


def delete_user(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["login"] = 0
            i["pass"] = 0
            i["perm"] = 0
            i["activity"] = False
            return True
    return False


def pasasword_change(login, password):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["pass"] = hashlib.md5(password.encode()).hexdigest()
            return True
    return False


def stop_activity(login):
    for i in init.data_users["users"]:
        if i["login"] == login:
            i["activity"] = False


def list():
    result = ""
    for i in init.data_users["users"]:
        status = str("online") if get_activity(i["login"]) else str("offline")
        result += str(i["login"]) + ":" + str(i["pass"]) + " (" + str(i["perm"]) + ") " + str(status) + "\n"
    return result
