class User(object):
    def __init__(self, adr, name, permission):
        self.ip = adr[0]
        self.port = adr[1]
        self.name = name
        self.perm = permission

    def brake(self):
        pass

    def drive(self):
        pass
