class JobStatus(object):
    FAILING = "FAILING"
    OK = "OK"
    UNKNOWN = "UNKNOWN"

class Job(object):

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def __eq__(self, other):

        return self.name == other.name \
           and self.status == other.status