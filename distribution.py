"""This module contains the dist_to_images() function, which plots
signal strength distributions for each room, based on the
Wireless Indoor Localization dataset (see README.md for details).

The module also features a command-line interface.
"""

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from argparse import ArgumentParser

# Public API declaration
__all__ = ['dist_to_images']

_DEF_FILENAME = 'wifi_localization.txt'
_DEF_IMAGEDIR = 'images'
_DEF_ROOTNAME = 'room'
_DEF_BINS = 20
_FACECOLOUR = '#f2f2f2'

def dist_to_images(data_file: str = _DEF_FILENAME,
                   image_dir: str = _DEF_IMAGEDIR,
                   image_rootname: str = _DEF_ROOTNAME,
                   bins: int = _DEF_BINS,
                   ) -> None:
    """Plots signal strength distributions for each room, based on
    the data in wifi_localization.txt, to PNG files.

    data_file: the source file; defaults to wifi_localization.txt

    image_dir: directory name that will contain the PNG files

    image_stem: the name that the PNG files will share.
    Default is 'room'; and the resulting files will be
    room_1.png ... room_4.png
    If such files exist, they will be overwritten.

    bins: the number of bins for the histograms."""
    
    df = pd.read_csv(data_file,
                     sep = '\t',
                     header = None,
                     names  = ['d' + str(i) for i in range(1, 8)] + ['room'],
                     )
    
    if not Path(image_dir).exists():
        Path.mkdir(image_dir)

    for room in df.room.drop_duplicates():
        fig, axes = plt.subplots(4, 2,
                                 figsize = (10.24, 7.68),
                                 sharex = True,
                                 sharey = True,
                                 )

        axes = axes.flatten()
        dfr = df[df.room == room].drop(labels = 'room', axis = 1)

        for ax, dev, i in zip(axes, dfr, range(len(dfr.columns))):
            ax.hist(dfr[dev],
                    bins = bins,
                    color = ''.join(('C', str(i))),
                    )
            ax.legend([' '.join(('Device ', str(i+1)))], loc='best')
            ax.set_facecolor(_FACECOLOUR)

        axes[-1].set_visible(False)
        axes[-3].tick_params(labelbottom=True)
        fig.suptitle(f'Signal strength distribution for each location in Room {room}')

        fig.savefig(Path(image_dir)
                    / Path(''.join((image_rootname, '_', str(room), '.png'))))

    return

# CLI
# ---

# 'distribution.py data_file image_dir image_rootname bins'

if __name__ == '__main__':
    
    parser = ArgumentParser(prog = 'distribution',
                            description = 'Plots wi-fi signal strength distribution!',
                            epilog = 'Thank you for using %(prog)s!',
                            )

    input_args = parser.add_argument_group('Input file-related argument')
    output_args = parser.add_argument_group('Output file-related arguments')

    input_args.add_argument(
        '-df', '--data_file',
        default=_DEF_FILENAME,
        help='Path to the source data file.'
        f' Defaults to {_DEF_FILENAME}'
        )

    output_args.add_argument(
        '-id', '--image_dir',
        default=_DEF_IMAGEDIR,
        help='Directory where the output files will be '
        f'placed. Defaults to {_DEF_IMAGEDIR}'
        )

    output_args.add_argument(
        '-ir', '--image_rootname',
        default=_DEF_ROOTNAME,
        help='The root of the image files stem.'
        ' The resulting files will be names as: '
        '<root>_<room_number>.png.'
        f' Defaults to {_DEF_ROOTNAME}'
        )

    parser.add_argument('-b', '--bins',
                        default=_DEF_BINS,
                        help='The number of bins for the distribution.'
                        f' Defaults to {_DEF_BINS}',
                        type=int
                        )

    args = parser.parse_args()
    
    dist_to_images(data_file = args.data_file,
                   image_dir = args.image_dir,
                   image_rootname = args.image_rootname,
                   bins = args.bins
                   )
    
    
























    
