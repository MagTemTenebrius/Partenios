import socket
import logging
import threading

from server import UserHandler
from server.CommandHandler import CommandHandler

port = 5050

sock = socket.socket()
sock.bind(('', port))
sock.listen()
users = []
logging.basicConfig(format='%(asctime)s [Partenios Server] [%(levelname)s] %(message)s', level=logging.DEBUG,
                    datefmt='%H:%M:%S')

logging.info("Server is running on the port " + str(port))
# logging.info('Admin logged in')

UserHandler.init()

# logging.debug(UserHandler.get_activity("root"))
# logging.debug(UserHandler.set_activity("root"))
# logging.debug(UserHandler.get_activity("root"))
# logging.debug(UserHandler.stop_activity("root"))

threads = {}


while 1:
    conn, adr = sock.accept()
    logging.info("User connect " + adr[0] + str(adr[1]))
    my_thread = threading.Thread(target=CommandHandler, args=(conn, adr,))
    my_thread.start()
    threads[adr[1]] = my_thread
