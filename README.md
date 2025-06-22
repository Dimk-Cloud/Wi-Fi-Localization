# Introduction and Acknowledgment.

This small project contains code to explore and analyze the Wireless Indoor Localization dataset.

The dataset is hosted at https://archive.ics.uci.edu/dataset/422/wireless+indoor+localization
under a Creative Commons Attribution 4.0 International (CC BY 4.0) license.

The dataset is contained in wifi_localization.txt (not hosted here), which is used as the data source for this humble project.


# The `distribution` module.

The `distribution` module defines the `dist_to_images` function, which reads the data and plots signal strength distributions for each device and for each room. With four rooms, and each room containing data for seven devices, the function outputs four images, each one with seven plots. The plots are saved as distinct PNG files for each room and optionally can be archived.

The module also provides a command-line interface (CLI).

The function's docstring and the CLI's help messages provide more detailed information.


# The `correlation` module.

The `correlation` module defines the `corr_to_html` function, which reads the dataset and returns an HTML output containing four tables. Each table is a correlation table of signal strength values across all devices, for one room.

The module also provides a command-line interface (CLI), which enables saving the output of the function to an HTML file.

The function's docstring and the CLI's help messages provide more detailed information.



# Building a classification model.

To be continued .....



