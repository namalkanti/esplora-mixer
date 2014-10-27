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

        Arguments:
        port - The path to the serial port the esplora is connected to
        baud - The baudrate for the arduino controller
        """
        self._connection = Serial(port, baud)

    def get_state_generator(self):
        """
        Creates generator that polls esplora for state

        Returns:
        Generator that will poll esplora and formats data neatly
        """
        while True:
            try:
                self._connection.write(b"s")
                ebytes = self._connection.readline()
                poll = ebytes.decode(ENCODING).strip().split(",")
                data={}
                data[GAIN] = float(poll[0]) / 1023
                joystick = float(poll[-1])
                if 100 < joystick:
                    data[STICK] = -1
                elif -100 > joystick:
                    data[STICK] = 1
                else:
                    data[STICK] = 0
                data[SAVE_ONE] = int(poll[1])
                data[SAVE_TWO] = int(poll[2])
                data[PLAY_ONE] = int(poll[3])
                data[PLAY_TWO] = int(poll[4])
                yield data
            except ValueError:
                yield None


