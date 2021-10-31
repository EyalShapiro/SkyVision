import threading
from networktables import NetworkTables

SKYNET_IP = '10.44.16.2'
VISION_TABLE_NAME = "Vision"

vision_table = None


def init_and_wait():
    """
    A blocking function that will init and wait
    """
    global vision_table
    vision_table = NetworkTables.getTable(VISION_TABLE_NAME)
    cond = threading.Condition()
    notified = [False]

    def connection_listener(connected, info):
        print("Connected: {} \n info : {}".format(connected, info))
        print("Connected to",vision_table)
        with cond:
            notified[0] = True
            cond.notify()

    
    NetworkTables.initialize(server=SKYNET_IP)
    NetworkTables.addConnectionListener(connection_listener,
                                        immediateNotify=True)

    with cond:
        if not notified[0]:
            cond.wait()


def get_bool(key: str, default: bool) -> bool:
    """
    Gets a boolean value from the table if initiated
    """
    if vision_table is None:
        print("vision_table wasn't initialized, please use init")
        return
    return vision_table.getBoolean(key, default)


def set_bool(key: str, value: bool):
    """
    Sets a boolean value in the table if initiated
    """
    if vision_table is None:
        print("vision_table wasn't initialized, please use init")
        return
    vision_table.putBoolean(key, value)

def get_number(key: str, default: float) -> float:
    """
    Gets a float value from the table if initiated
    """
    if vision_table is None:
        print("vision_table wasn't initialized, please use init")
        return
    return vision_table.getNumber(key, default)


def set_number(key: str, value: float):
    """
    Sets a float value in the table if initiated
    """
    if vision_table is None:
        print("vision_table wasn't initialized, please use init")
        return
    vision_table.putNumber(key, value)


if __name__ == "__main__":
    print("This is a library, so you can't run it as main.")