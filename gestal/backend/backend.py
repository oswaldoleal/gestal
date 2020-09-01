from models import Task
from persistence import Persistence, DefaultStorage

class Backend:
    # this persistence object should be handled as a singleton TODO
    persistence = None

    def __init__(self):
        self.persistence = Persistence()