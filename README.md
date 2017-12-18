# GW_h5_converter
Converts existing gravitational wave simulation data into the HDF5 format to be used with PyCBC.

To use, place converter.py and a properly formatted version of metadata.txt in the same folder as any gravitational wave data files you wish to convert, then run converter.py. It will convert all files within the folder that have either .txt or .dat as its expension, but all files must use the same metadata.

The process implemented for converting gravitational wave simulations into HDF5 files is heavily dependent upon the proper formatting of a "metadata.txt" file, which stores important information about the gravitational wave to be converted. Metadata.txt is imported and turned into code when coverter.py is run, so its careful formatting is crucial. A sample metadata.txt file is attached within this repository; further details regarding formatting will be discussed in this README file. Using the two in conjunction for reference should lead to a properly formatted file. 

## Metadata Essential Fields ##

