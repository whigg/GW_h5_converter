# GW_h5_converter
Converts existing gravitational wave simulation data into the HDF5 format to be used with PyCBC.

To use, place converter.py and a properly formatted version of metadata.txt in the same folder as any gravitational wave data files you wish to convert, then run converter.py. It will convert all files within the folder that have either .txt or .dat as its expension, but all files must use the same metadata.

Gravitational wave data files must have a minimum of three columns of data: column 1 must be timestamps, and columns two and three must be either the plus and cross values for the magnitude of strain, or else column two must be magnitude and column three must be argument (angle).

The process implemented for converting gravitational wave simulations into HDF5 files is heavily dependent upon the proper formatting of a "metadata.txt" file, which stores important information about the gravitational wave to be converted. Metadata.txt is imported and turned into code when coverter.py is run, so its careful formatting is crucial. A sample metadata.txt file is attached within this repository; further details regarding formatting will be discussed in this README file. Using the two in conjunction for reference should lead to a properly formatted file. 

## Style Guide

Since the metadata file will be read in as code, the file should contain data in the standard variable/value format. 
```
  Ex: 
    variableText   = "text"
    variableInt    = 11
    variableFloat  = 1.0
```    
Anything that is included in the metadata file but is not intended to be read into converter.py as code (in other words, anything useful to have but that is not inlcluded by default should be commented out with a pound (#), per Python convention
```
  Ex:
    # this line is commented out
    this line is not
```
## Metadata Critical Fields
The following fields must exist in the metadata file, and must have a meaningful value from the list of possible values for each:

#### dataFormat = "PlusCross"
This field explains what format strain data was saved in. **Possible values:** 
```
PlusCross - data columns two and three in original data file represent 
            two strain values, along opposite directions
MagArg    - data column two in original file represents strain magnitude
            (amplitude); column three represents argument (angle)
```
#### timeFormat = "Msun"
Indicates what ocnvention of units was used to represent time. **Possible values:**
```
Msun    - Solar units. 1 Msun = the mass of one Sol
Mtotal  - Units as a fraction of mass of binary system, in units of Msun
          Ex: If mass of binary system is 2.5 Sols, then 1 Msun in time would be .4 Mtotal
s       - Seconds.
```
#### strainFormat = "rhOverM"
This field idenitfies the units that were used to express the magnitude of strain values. If dataFormat is PlusCross and strainFormat is anything other than rhOverM, columns 1 and 2 of data file will be converted to rhOverM. If dataFormat is MagArg, only column 2 will be converted. **Possible Values:**
```
rhOverM - Strain value, multiplied by observer distance (I believe?) and divided by system mass
rh      - Strain value, multiplied by observer distance (I think)
```
#### massFormat = "Msun"


#### grav_mass1 = 1.528
Mass of object 1, in whatever units are defined by massFormat

#### grav_mass2 = 1.222
Mass of object 2, in whatever units are defined by massFormat

#### l = 2
#### m = 2
