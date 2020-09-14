import json
import logging


def init():
    with open('users.json', 'r') as file:
        logging.info("Users db loading...")
        init.data_users = json.load(file)
        logging.debug("Users: ")
        for user in init.data_users["users"]:
            logging.debug('\t' + user["login"] + ":" + user["pass"] + " \tperm=" + str(user["perm"]))
        logging.info("User database loading completed!")


def check_user(login, password):
    for i in init.data_users["users"]:
        if i["login"] == login:
            if i["pass"] == password:
                return i["perm"]
            else:
                return 0
    return 0
