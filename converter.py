#  ***h5_converter_2.py***
#     This program converts .txt or .dat files of waveform data into
#     .h5 format and converts important data fields into formats that are 
#     used as standard inside PyCBC, so that the .h5 files can be used within
#     the PyCBC framework.
    
#     The program is dependent upon a properly formatted "metadata.txt"
#     file, which it will convert into code upon running this program, 
#     to collect key parameters about the waveform that is being converted.
    
#     Thorough documentation will eventually be created on all of this, but
#     there have been too many recent changes to make documentation worth
#     it yet.

# import all essential libraries
import glob
import numpy as np
import romspline as romSpline
import h5py
from pycbc import pnutils
import lal
import hashlib
import pycbc.types as types
from pycbc.waveform import utils as wfutils

# converts time to seconds, in keeping with PyCBC standard
# initial time format will be indicated inside metadata.txt
# previous time formats seen: 
#     seconds (s) 
#     solar units (Msun)
# Mtotal represents the total gravitational mass of the binary system, 
# as a ratio of Msun. This hasn't been seen yet, but seems likely enough
# that I included it anyway.
def convert_time(timeFormat, times, total_grav_mass):
    if (timeFormat == "s"):
        for time in times:
            time /= lal.MTSUN.SI
            timeFormat = "Msun"
    if (timeFormat == "Msun"):
        for time in times:
            time /= total_grav_mass
            timeFormat = "Mtotal"
    if (timeFormat == "Mtotal"):
        return times
    else:
        print "Time is in an unrecognized format. Please edit the metadata file and try again."
        sys.exit()

# converts any distances used in the original file into units of Mpc,
# in keeping with PyCBC convention.
# unused as of yet; here in case it ever becomes useful
        
# # convert distance to Mpc
# def convert_distance(distFormat, distance):
#     if (distFormat == "Msun"):
#         distance *= lal.MRSUN_SI
#         distFormat = "m"
#     elif (distFormat == "km"):
#         distance *= 1000
#         distFormat = "m"
#     if (distFormat == "m"):
#         distance /= lal.PC_SI
#         distFormat = "pc"
#     if (distFormat == "pc"):
#         distance /= 10e6
#         distFormat = "Mpc"
#     if (distFormat == "Mpc"):
#         return distance
#     else:
#         print "Distance is in an unrecognized format. Please edit the metadata file and try again."
#         sys.exit()

# converts strain to rh/m, in keeping with PyCBC convention
# initial strain format will be indicated inside metadata.txt
# IMPORTANT NOTE: if strain data is in Magnitude/Argument format rather
# than Plus/Cross format, ONLY the first field represents "strain"; the
# second field is the angle of the strain, and so should NOT be adjusted
# if in Plus/Cross, both fields are magnitudes (in different directions),
# so both will need to be converted to rh/m if they aren't already
def convert_strain(strainFormat, strainVal1, strainVal2, total_grav_mass):
    if (strainFormat == "rh"):
        for i in range(0, len(strainVal1)):
            strainVal1[i] /= total_grav_mass
        # ONLY if in PlusCross
        if (dataFormat == "PlusCross"):
            for i in range(0, len(strainVal2)):
                strainVal2[i] /= total_grav_mass
        return strainVal1, strainVal2
    elif (strainFormat == "rhOverM"):
        return strainVal1, strainVal2
    else:
        print "Strain is in an unrecognized format. Please edit the metadata file and try again."
        sys.exit()

# converts mass to Msun, in keeping with PyCBC convention
# initial mass format will be indicated inside metadata.txt
# previous mass formats seen:
#     SI units (kg)
#     ratio of the total mass of the system in units of Msun (mTotal)
def convert_mass(massFormat, grav_mass1, grav_mass2, total_grav_mass):
    if (massFormat == "kg"):
        print "Old mass:"
        print mass1
        grav_mass1 /= lal.MSUN_SI
        grav_mass2 /= lal.MSUN_SI
        massFormat = "Msun"
        print "New mass:"
        print mass1
    elif (massFormat == "mTotal"):
        grav_mass1 *= total_grav_mass
        grav_mass2 *= total_grav_mass
        massFormat = "Msun"
    if (massFormat == "Msun"):
        return grav_mass1, grav_mass2
    else:
        print "Mass1/mass2 is in an unrecognized format. Please edit the metadata file and try again."
        sys.exit()

# open the metadata.txt file and read it in as code
exec(open('metadata.txt', 'r'))

# find all files that qualify for conversion, based on their file extension,
# and store them all as a list.
# directory: use same relative directory
# (i.e. copy this file into the directory where your .dat/.txt and
# metadata.txt are)
datafiles = glob.glob('*.txt' or '*.dat')

# go through list and convert each file as necessary into its own .h5
for datafile in datafiles:
    
    # exclude metadata.txt itself from conversion
    if (datafile == "metadata.txt"):
        continue
    else:
        rawname = datafile.replace('.txt','')
        h5file = rawname + '.h5'

        # Hardcoded for now, but something we could in theory include in metadata
        delta_t = 1./16384
        f_lower_hz = 700.0 

        # because it's just easier to think in Hz, then let the computer do the conversion...
        # if I remember correctly, this is a new thing in PyCBC in recent months. it stumped
        # us for a while
        f_lower = f_lower_hz * (lal.TWOPI * total_grav_mass * lal.MTSUN_SI)

        # import data fields from file
        times, strainVal1, strainVal2 = np.loadtxt(datafile, usecols=(0,1,2), unpack=True)
        
        # run conversion functions for correct PyCBC conventions
        grav_mass1, grav_mass2 = convert_mass(massFormat, grav_mass1, grav_mass2, total_grav_mass)
        strainVal1, strainVal2 = convert_strain(strainFormat, strainVal1, strainVal2, total_grav_mass)
        times = convert_time(timeFormat, times, total_grav_mass)

        with h5py.File(h5file,'w') as fd:

            # Set metadata
            # still need to add values for love number, radius, lambda, etc.
            mchirp, eta = pnutils.mass1_mass2_to_mchirp_eta(grav_mass1, grav_mass2)
            fd.attrs.create('NR_group', 'CSUF_GWPAC_NS')
            fd.attrs.create('sim_name', 'Deitrich')
            fd.attrs.create('EOS','ALF2')
            hashtag = hashlib.md5()
            fd.attrs.create('type', 'BNS')
            hashtag.update(fd.attrs['type'])
            fd.attrs.create('hashtag', hashtag.digest())
            fd.attrs.create('Format', 1)
            fd.attrs.create('f_lower_at_1MSUN', f_lower)
            fd.attrs.create('eta', eta)
            fd.attrs.create('spin1x', spin1x)
            fd.attrs.create('spin1y', spin1y)
            fd.attrs.create('spin1z', spin1z)
            fd.attrs.create('spin2x', spin2x)
            fd.attrs.create('spin2y', spin2y)
            fd.attrs.create('spin2z', spin2z)

            # XXX HARDCODING for non-spinning / aligned-spin
            # this, too, could one day be in metadata.txt, if we found it worthy
            fd.attrs.create('LNhatx', 0.0)
            fd.attrs.create('LNhaty', 0.0)
            fd.attrs.create('LNhatz', 1.0)
            fd.attrs.create('nhatx', 1.0)
            fd.attrs.create('nhaty', 0.0)
            fd.attrs.create('nhatz', 0.0)
            fd.attrs.create('Lmax', 2)

            # track all mass types we've run into; different people care
            # about different ones
            fd.attrs.create('ADM_mass1', ADM_mass1)
            fd.attrs.create('ADM_mass2', ADM_mass2)
            fd.attrs.create('Baryon_mass1', Baryon_mass1)
            fd.attrs.create('Baryon_mass2', Baryon_mass2)
            fd.attrs.create('grav_mass1', grav_mass1)
            fd.attrs.create('grav_mass2', grav_mass2)
            fd.attrs.create('lambda1',lambda_1)
            fd.attrs.create('lambda2',lambda_2)


            # find the largest amplitude and set its time stamp to t=0; adjust all others
            # this should be a resonably accurate way of finding the moment of "merger" 
            # and making it t=0, in keeping with PyCBC conventions
            dmax = 0
            maxloc = 0
            strainMag = 0
            for i in range(0, len(strainVal1)):
                if (dataFormat == "MagArg"):
                    strainMag = strainVal1[i]
                elif (dataFormat == "PlusCross"):
                    strainMag = np.sqrt((strainVal1[i])**2 + (strainVal2[i])**2)
                else:
                    print "dataFormat is incorrect or is not specified. Edit the metadata file and try again."
                if strainMag > dmax:
                    maxloc = i
                    dmax = strainMag
            timeAdjust = times[maxloc]
            for i in range(0, len(times)):
                times[i] = (times[i] - timeAdjust)

            # leaving this here for now; sometimes I've needed to test with 
            # different values/equations
            massMpc = 1

            strainVal1 = types.TimeSeries(strainVal1/massMpc, delta_t=delta_t)
            strainVal2 = types.TimeSeries(strainVal2, delta_t=delta_t)

            # run romSpline to convert into reduced order spline, then assign final .h5 values
            # and write all data to .h5 file
            # handled independently for Magnitude/Argument vs. Pluss/Cross data, based on 
            # unique needs for each format
            if (dataFormat == "MagArg"):
                strainAmp = np.array(strainVal1)
                strainPhase = np.array(strainVal2)

                print 'fitting spline...'
                sAmpH = romSpline.ReducedOrderSpline(times, strainAmp, rel=True, verbose=False)
                sPhaseH = romSpline.ReducedOrderSpline(times, strainPhase, rel=True, verbose=False)

                grAmp = fd.create_group('amp_l%d_m%d' %(l,m))
                sAmpH.write(grAmp)

                grPhase = fd.create_group('phase_l%d_m%d' %(l,m))
                sPhaseH.write(grPhase)

                print 'spline created'
            elif (dataFormat == "PlusCross"):
                strainAmp = wfutils.amplitude_from_polarizations(strainVal1, strainVal2/massMpc).data
                strainPhase = wfutils.phase_from_polarizations(strainVal1, strainVal2/massMpc).data 

                print 'fitting spline...'
                sAmpH = romSpline.ReducedOrderSpline(times, strainAmp, rel=True, verbose=False)
                sPhaseH = romSpline.ReducedOrderSpline(times, strainPhase, rel=True, verbose=False)

                grAmp = fd.create_group('amp_l%d_m%d' %(l,m))
                sAmpH.write(grAmp)

                grPhase = fd.create_group('phase_l%d_m%d' %(l,m))
                sPhaseH.write(grPhase)

                print 'spline created'
            else:
                print "dataFormat is incorrect or is not specified. Edit the metadata file and try again."
