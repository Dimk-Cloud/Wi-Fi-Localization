"""This module contains the dist_to_images() function, which plots
signal strength distributions for each device and for each room, based on the
Wireless Indoor Localization dataset (see README.md for details).

The module also features a command line interface.
"""

import pandas as pd
import matplotlib.pyplot as plt
import io
import zipfile

from pathlib import Path
from argparse import ArgumentParser
from collections import namedtuple

plt.style.use('seaborn-v0_8')

# Public API declaration
__all__ = ['dist_to_images', 'INPUT_FILE', 'IMAGEDIR', 'IMAGE_STEM', 'BINS'] #, 'FACECOLOUR']

INPUT_FILE = 'data/wifi_localization.txt'
IMAGEDIR = 'data/images'
IMAGE_STEM = 'room'
BINS = 20
#FACECOLOUR = '#f2f2f2'

def dist_to_images(data_file: str = INPUT_FILE,
                   image_dir: str = IMAGEDIR,
                   image_stem: str = IMAGE_STEM,
                   archive: str | None = None,
                   bins: int = BINS         
                   ) -> None:
    """Based on the raw data of the Wi-Fi Localization project (see README.md for details),
    the function plots signal strength distributions for each room, for each device.
    The plots are saved to PNG files. Input parameters:

    data_file: the source (input) file.

    image_dir: directory name that will contain the PNG files or the archive file,
    if the 'archive' option is True.

    image_stem: the string that PNG file names will start from (shared by all the file names).
    PNG file names are constructed as follows: <image_stem>_i.png, where i is the room number.
    If default, the resulting files will be named as follows: room_1.png ... room_4.png
    If such files exist, they will be overwritten.

    bins: the number of bins for the plotted distributions (histograms).

    archive: if a name is provided, a zip archive with that name containing the PNG files
    will be saved in 'image_dir', instead of the PNG files. The archive member files will be
    named according to the 'image_stem' rules as described above.
    """

    if not Path(data_file).is_file():
        raise FileNotFoundError(f'File {data_file} can not be found.')
    
    df = pd.read_csv(data_file,
                     sep = '\t',
                     header = None,
                     names  = ['d' + str(i) for i in range(1, 8)] + ['room'],
                     )
    image_dir_path = Path(image_dir)
    if not image_dir_path.exists():
        image_dir_path.mkdir()

    if archive:
        ArchiveMember = namedtuple('ArchiveMember', 'name content')  # PEP 8 UpperCamelCase
        archive_members: list[ArchiveMember] = []

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
            #ax.set_facecolor(FACECOLOUR)

        axes[-1].set_visible(False)
        axes[-3].tick_params(labelbottom=True)
        fig.suptitle(f'Signal strength distribution for each device in Room {room}')

        image_fname = ''.join((image_stem, '_', str(room), '.png'))

        if archive:
            bin_content = io.BytesIO()
            fig.savefig(bin_content, format='png')
            archive_members.append(
                ArchiveMember(
                    name = image_fname,
                    content = bin_content.getvalue()
                    )
                )
        else:        
            fig.savefig(image_dir_path/image_fname, format='png')

        plt.close(fig)

    if archive:
        with zipfile.ZipFile(file=image_dir_path/archive,
                             mode='w',
                             compression=zipfile.ZIP_DEFLATED) as ar:
            for archive_member in archive_members:
                ar.writestr(archive_member.name, data=archive_member.content)

    return None

# CLI
# ---

# 'distribution.py data_file image_dir image_rootname bins'

def main():

    _DESCRIPTION = \
    """Based on the raw data of the Wi-Fi Localization project (see README.md for details),
    the script plots signal strength distributions for each device and for each room.
    The plots are saved to PNG files."""
    
    parser = ArgumentParser(prog = 'distribution',
                            description = _DESCRIPTION,
                            epilog = 'Thank you for using %(prog)s!',
                            )

    # Group the following four options as related to directories and file names
    files_help_group = parser.add_argument_group(
        title='Input and output files',
        description='The script takes raw CSV data from one file and saves the results '
                    'as a series of PNG images or as a single archive, as specified below.'
        )

    files_help_group.add_argument(
        '-df', '--data_file',
        default=INPUT_FILE,
        help=f'Path to the source CSV file. Defaults to {INPUT_FILE}',
        metavar='<source file>',
        )

    files_help_group.add_argument(
        '-id', '--image_dir',
        default=IMAGEDIR,
        help=f"""Directory where the output files will be placed. If the archive name is provided
        (the -a option below), the archive will be placed there. Defaults to {IMAGEDIR}""",
        metavar='<image folder>'
        )

    files_help_group.add_argument(
        '-is', '--image_stem',
        default=IMAGE_STEM,
        help=f"""The string that PNG file names will start from (shared by all the file names).
        PNG file names are constructed as follows: <image_stem>_i.png, where i is the room number.
        If default, the resulting files will be named as follows: room_1.png ... room_4.png.
        If such files exist, they will be overwritten. 'Defaults to '{IMAGE_STEM}'.""",
        metavar='<image stem>'
        )

    files_help_group.add_argument(
        '-a', '--archive',
        default=None,
        help="""If a name is provided, a zip archive with that name containing the PNG files
        will be saved in 'image_dir', instead of PNG files. The archive member files will be
        named according to the 'image_stem' rules as described above. Defaults to None, meaning 
        PNG files will not be archived.""",
        metavar='<archive file name>'
        )

    # Create a separate help group for the BINS option
    bins_help_group = parser.add_argument_group(title='Data presentation')

    bins_help_group.add_argument('-b', '--bins',
                        default=BINS,
                        help=f'The number of bins for each distribution. Defaults to {BINS}.',
                        type=int,
                        metavar='<number of bins>'
                        )
    
    args = parser.parse_args() # '-h'.split())
    #print('The following arguments have been received:\n', args)
    
    dist_to_images(data_file = args.data_file,
                   image_dir = args.image_dir,
                   image_stem = args.image_stem,
                   archive = args.archive,
                   bins = args.bins
                   )
    
if __name__ == '__main__':
    main()























    
