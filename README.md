# GW_h5_converter
Converts existing gravitational wave simulation data into the HDF5 format to be used with PyCBC.

The process implemented for converting gravitational wave simulations into HDF5 files is heavily dependent upon the proper formatting of a "metadata.txt" file, which stores important information about the gravitational wave to be converted. Metadata.txt is imported and turned into code when coverter.py is run, so its careful formatting is crucial. A sample metadata.txt file is attached within this repository; further details regarding formatting will be discussed in this README file. Using the two in conjunction for reference should lead to a properly formatted file. 

