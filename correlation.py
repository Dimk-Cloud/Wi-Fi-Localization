"""This module defines the get_corrs() function, which determines
pairwise correlations for each pair of devices, independently
for each room, based on the Wireless Indoor Localization dataset
(see README.md for details).

The module also features a command-line interface.
"""

import pandas as pd
from argparse import ArgumentParser
from pathlib import Path

# Public API declaration
__all__ = ['get_corrs']


_DEF_FILENAME = 'wifi_localization.txt'
_DEF_OUTFILE = 'correlations.html'
_DEF_COLORMAP = 'Greens'
_DEF_PRECISION = 6
_DEF_TITLE = 'Wi-fi signal strength correlation values.'

def corr_to_html(data_file: str = _DEF_FILENAME,
                 outfile: str = _DEF_OUTFILE,
                 colormap: str = _DEF_COLORMAP,
                 precision: int = _DEF_PRECISION,
                 absolute: bool = False) -> int:

    """Produces an HTML file with four tables, each representing the correlation
    table of signal strength values for one room.

    outfile: the resulting HTML file;

    colormap: matplotlib color map to use as a heat map;

    precision: the floating point precision to format float values;

    absolute: output absolute values of correlation coefficients.'

    Returns: the number of bytes written.

    """
    
    #global df
    df = pd.read_csv(data_file,
                     sep = '\t',
                     header = None,
                     names  = ['d' + str(i) for i in range(1, 8)] + ['room'],
                     )

    df = df.groupby('room').corr().abs() if absolute else df.groupby('room').corr()

    html = [f'<!DOCTYPE html><html lang="en"><head><title>{_DEF_TITLE}'
            '</title></head><body style="background-color: '
            f'#f2f2f2;"><article><H1>{_DEF_TITLE}</H1>']

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

    with open(outfile, 'wt') as wh:
        bts = wh.write('<br><br>'.join(html))

    return bts
    

# CLI
# ---

# 'correaltion.py data_file outfile colormap precision'

if __name__ == '__main__':
    
    parser = ArgumentParser(prog = 'correaltion',
                            description = 'Saves pairwise correlations for each pair of devices '
                            'to an HTML file, one table for each room.',
                            epilog = 'Thank you for using %(prog)s!',
                            )

    parser.add_argument(
        '-df', '--data_file',
        default=_DEF_FILENAME,
        help='Path to the source data file.'
        f' Defaults to {_DEF_FILENAME}'
        )

    parser.add_argument(
        '-rf', '--result_file',
        default=_DEF_OUTFILE,
        help='Path to the HTML file with results.'
        f' Defaults to {_DEF_OUTFILE}'
        )

    parser.add_argument(
        '-cm', '--colormap',
        default=_DEF_COLORMAP,
        help='matplotlib color map to use as a heat map.'
        f' Defaults to "{_DEF_COLORMAP}"'
        )

    parser.add_argument(
        '-p', '--precision',
        default=_DEF_PRECISION,
        choices=list(range(0, 7)),
        help='The floating point precision to format float values.'
        f' Defaults to {_DEF_PRECISION}',
        type=int
        )

    parser.add_argument(
        '-a', '--absolute',
        action='store_true',
        default=False,
        help='Output absolute values of correlation coefficients.'
        f' Defaults to False'
        )

    args = parser.parse_args()
    
    corr_to_html(
        data_file = args.data_file,
        outfile = args.result_file,
        colormap = args.colormap,
        precision = args.precision,
        absolute = args.absolute
        )
    























    
