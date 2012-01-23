class Server(object):

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def __eq__(self, other):
        return self.host == other.host \
           and self.username == other.username \
           and self.password == other.password

    def __repr__(self):
        return 'Server(host=%r,username=%r,password=%r)' \
             % (self.host, self.username, self.password)
