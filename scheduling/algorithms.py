class Algorithms:
    """
    This is an abstract class to instance algorithms
    """
    def __init__(self):
        self.name = 'Algorithms'

    def resolve(self, lot = []):
        return lot


class CLook(Algorithms):
    """"
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'clook'


class CScan(Algorithms):
    """"
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'cscan'


class Fcfs(Algorithms):
    """
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'fcfs'


class Fifo(Algorithms):
    """
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'fifo'


class Look(Algorithms):
    """
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'look'


class Scan(Algorithms):
    """"
    Receive a lot and process it, return the lot 
    like Scan algorithm says
    """
    def __init__(self):
        self.name = 'scan'
