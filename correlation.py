"""This module defines the get_corrs() function, which returns
pairwise correlations for each pair of devices, independently
for each room, based on the Wireless Indoor Localization dataset
(see README.md for details).

The module also features a command line interface which enables saving
the results to an HTML file.
"""

import pandas as pd

from argparse import ArgumentParser
from pathlib import Path

# Public API declaration
__all__ = ['get_corrs', 'INPUT_FILE', 'OUTPUT_FILE', 'MPL_COLORMAP', 'PRECISION']

INPUT_FILE = 'data/wifi_localization.txt'
OUTPUT_FILE = 'data/correlations.html'
MPL_COLORMAP = 'Greens'
PRECISION = 6
_HTML_TITLE = 'Wi-fi signal strength correlation values.'

def corr_to_html(data_file: str = INPUT_FILE,
                 colormap: str = MPL_COLORMAP,
                 precision: int = PRECISION,
                 absolute: bool = False) -> str:

    """Takes a CSV-file with the raw data of the Wi-Fi Localization project (see README.md
    for details). Returns an HTML output containing four tables, each representing the
    correlation table of signal strength values across all devices, for one room.
    Input parameters:

    data_file: a CSV-file containing the raw data of the Wi-Fi Localization project.

    colormap: matplotlib color map to use as a heat map for each table.

    precision: the floating point precision to format float values (the default values for
    the abovementioned parameters are specified as the module's constants).

    absolute: if True, output the absolute values of correlation coefficients.'

    Returns: the HTML string.
    """

    if not Path(data_file).is_file():
        raise FileNotFoundError(f'File {data_file} can not be found.')
    
    df = pd.read_csv(data_file,
                     sep = '\t',
                     header = None,
                     names  = ['d' + str(i) for i in range(1, 8)] + ['room'],
                     )

    df = df.groupby('room').corr().abs() if absolute else df.groupby('room').corr()

    html = [f'<!DOCTYPE html><html lang="en"><head><title>{_HTML_TITLE}'
            '</title></head><body style="background-color: '
            f'#f2f2f2;"><article><h1>{_HTML_TITLE}</h1>']

    for i in df.index.get_level_values(0).unique():
        html.append(
            df.loc[i].style
            .set_caption(f'ROOM {i}')
            .set_table_styles([{'selector' : 'tr, td, caption', 'props' : 'padding: 10px;'},
                               {'selector' : 'caption', 'props' : 'font-weight: bold'},        
                               ])
            .format(precision = precision)
            .background_gradient(axis=None, cmap=colormap)
            .to_html()
            )

    html.append('</article></body></html>')

    return '<br><br>'.join(html)
    

# CLI
# ---

def main():

    _DESCRIPTION = \
    '''Takes a CSV-file with the raw data of the Wi-Fi Localization project (see README.md
    for details). Saves the result to an HTML file containing four tables, each representing
    the correlation table of signal strength values across all devices, for one room.'''

    parser = ArgumentParser(prog = 'correlation',
                            description = _DESCRIPTION,
                            epilog = 'Thank you for using %(prog)s!')

    # Group the following two options as related to file names
    files_help_group = parser.add_argument_group(
        title='Input and output files',
        description='The script takes raw CSV data from one file and saves the results '
                    'to another file, as specified below.'
        )
    files_help_group.add_argument(
        '-df', '--data_file',
        default=INPUT_FILE,
        help='Path to the source data file.'
        f' Defaults to {INPUT_FILE}.',
        metavar='<source file>'
        )
    files_help_group.add_argument(
        '-rf', '--result_file',
        default=OUTPUT_FILE,
        help='Path to the HTML file with results (will be overwritten if exists).'
        f' Defaults to {OUTPUT_FILE}.',
        metavar='<target file>'
        )
    

    # Group the following options as related to data presentation
    data_help_group = parser.add_argument_group(
        title='Data formatting and presentation',
        description='The following options relate to how the data is presented in HTML tables.'
        )

    data_help_group.add_argument(
        '-cm', '--colormap',
        default=MPL_COLORMAP,
        help='matplotlib color map to use as a heat map for each table.'
        f' Defaults to "{MPL_COLORMAP}."',
        metavar='<matplotlib color map>'
        )

    data_help_group.add_argument(
        '-p', '--precision',
        default=PRECISION,
        choices=list(range(0, 7)),
        help='The floating point precision to format float values.'
        f' Defaults to {PRECISION}.',
        type=int,
        metavar='<decimal precision>'
        )

    data_help_group.add_argument(
        '-a', '--absolute',
        action='store_true',
        help='Output the absolute values of correlation coefficients.'
        f' Defaults to False (if not provided).',
        )

    args = parser.parse_args()

    #print('The following arguments have been received:\n', args)
    #import sys; sys.exit()
    
    html = corr_to_html(
        data_file = args.data_file,
        colormap = args.colormap,
        precision = args.precision,
        absolute = args.absolute
        )

    result_file_path = Path(args.result_file)
    if not result_file_path.parent.exists():
        result_file_path.parent.mkdir()
    result_file_path.write_text(html, encoding='utf-8')
##    else:
##        parser.error(
##            f'Directory "{result_file_path.parent}" can not be created '
##            f'for the file {args.result_file}')

if __name__ == '__main__':
    main()














    
