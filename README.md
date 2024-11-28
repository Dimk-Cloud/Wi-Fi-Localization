# Introduction and Acknowledgment.

This small project contains some code to explore and analyze the Wireless Indoor Localization dataset.

The dataset is hosted at https://archive.ics.uci.edu/dataset/422/wireless+indoor+localization
under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.

The dataset is contained in wifi_localization.txt, which is used as the source for this project's code.


# The `distribution` module.

The `distribution` module defines the `dist_to_images` function, which reads the data and plots signal strength distributions for each device and for each room. With four rooms, and each room containing data for seven devices, the function outputs four images, each one with seven graphs.

The function takes the input file name, the output directory name, the root name of image files and the number of bins as optional arguments. The module also provides a command-line interface (CLI).

The function's docstring and the CLI's help messages contain more detailed information.


# The `correlation` module.

The `correlation` module defines the `corr_to_html` function, which reads the original data and produces an HTML file with four tables. Each table is a correlation table of signal strength values across all devices, for one room.

The function takes the input and output file names, the color map, the float precision value and the absolute flag as optional arguments. The module also provides a command-line interface (CLI).

The color map is a matplotlib color map which is used to apply a heat map to each table. More about color maps: https://matplotlib.org/stable/users/explain/colors/colormaps.html

The precision is an integer used to print correlation values, which are floats. 

More detailed information can be found in the function's docstring and the CLI's help messages.


# Building a classification model.

To be continued .....



