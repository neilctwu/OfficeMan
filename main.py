from recorder import Recorder
from officeman import OfficeMan
from threading import Thread


if __name__ == '__main__':
    t1 = Thread(target = OfficeMan, args=(8220,))
    t2 = Thread(target = Recorder, args=(8220, 44100))
    t1.start()
    t2.start()
