from serial import Serial

ENCODING = "utf-8"

POLL_BIT = b"s"

GAIN = "gain"
STICK = "stick"
SAVE_ONE = "sone"
SAVE_TWO = "stwo"
PLAY_ONE = "pone"
PLAY_TWO = "ptwo"



class EsploraInterface():
    """
    Interface to the Esplora controller.
    """

    def __init__(self, port="/dev/ttyACM0", baud=9600):
        """
        Opens serial connection to esplora.
        """
        self._connection = Serial(port, baud)

    def get_state_generator(self):
        """
        Returns current state of esplora.
        """
        while True:
            try:
                ebytes = self._connection.readline()
                data = ebytes.decode(ENCODING).strip().split(",")
                data[0] = float(data[0]) / 1023
                joystick = float(data[-1])
                if 100 < joystick:
                    data[-1] = -1
                elif -100 > joystick:
                    data[-1] = 1
                else:
                    data[-1] = 0
                yield data
            except ValueError:
                yield None


