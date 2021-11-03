import threading
from networktables import NetworkTables

TABLE = None

def init_and_wait(REMOTE_IP = '10.44.16.2',TABLE_NAME = "Vision"):
    """
    A blocking function that will init and wait
    """
    global TABLE
    TABLE = NetworkTables.getTable(TABLE_NAME)
    cond = threading.Condition()
    notified = [False]

    def connection_listener(connected, info):
        print("Connected: {} \n info : {}".format(connected, info))
        with cond:
            notified[0] = True
            cond.notify()

    
    NetworkTables.initialize(server=REMOTE_IP)
    NetworkTables.addConnectionListener(connection_listener,
                                        immediateNotify=True)

    with cond:
        if not notified[0]:
            cond.wait()

def get_bool(key: str, default: bool) -> bool:
    """
    Gets a boolean value from the table if initiated
    """
    if TABLE is None:
        print("vision_table wasn't initialized, please use init")
        return
    return TABLE.getBoolean(key, default)

def set_bool(key: str, value: bool):
    """
    Sets a boolean value in the table if initiated
    """
    if TABLE is None:
        print("vision_table wasn't initialized, please use init")
        return
    TABLE.putBoolean(key, value)

def get_number(key: str, default: float) -> float:
    """
    Gets a float value from the table if initiated
    """
    if TABLE is None:
        print("vision_table wasn't initialized, please use init")
        return
    return TABLE.getNumber(key, default)

def set_number(key: str, value: float):
    """
    Sets a float value in the table if initiated
    """
    if TABLE is None:
        print("vision_table wasn't initialized, please use init")
        return
    TABLE.putNumber(key, value)

if __name__ == "__main__":
    print("This is a library, so you can't run it as main.")