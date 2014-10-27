#Main class to launch and run mixer
import argparse
import sys

from EsploraInterface import EsploraInterface
from OutputAudioStream import OutputAudioStream

DEFAULT_SERIAL = "/dev/ttyACM0"
DEFAULT_BAUD = 9600

def main():
    """
    Main function reads audio file from command line and begins mixing.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file", help="Path to audio file to mix")
    parser.add_argument("-p", "--port", type=str, default=DEFAULT_SERIAL, help="Serial port for esplora. Default is {0}".format(DEFAULT_SERIAL))
    parser.add_argument("-b", "--baud", type=int, default=DEFAULT_BAUD, help="Baudrate for esplora. Default is {0}".format(DEFAULT_BAUD))
    args = parser.parse_args()

    audio_file = args.audio_file
    esplora = EsploraInterface(args.port, args.baud)
    esplora_out = esplora.get_state_generator()

    audio = OutputAudioStream(audio_file, esplora_out)
    audio.playback()
    audio.close()

if __name__ == "__main__":
    main()
