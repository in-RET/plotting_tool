import argparse
import os

from common import GoPlots
from gui import PYQT
from pathlib import Path


if __name__ == '__main__':
    if PYQT:
        from gui import StartGui
        StartGui()
    else:
        parser = argparse.ArgumentParser(
            prog = 'main.py',
            description='Tool to plot sankey diagrams and normale line plots form csv-files.',
            epilog = 'In.RET - Institut für regenerative Energietechnik'
        )

        parser.add_argument('folder', help="Filepath of the csv-files.")
        args = parser.parse_args()

        path_load = args.folder
        path_save = os.path.join(args.folder, "../plots")

        if not os.path.exists(path_save):
            os.makedirs(path_save)

        GoPlots(path_load, path_save, False, False)

