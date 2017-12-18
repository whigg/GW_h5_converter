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
