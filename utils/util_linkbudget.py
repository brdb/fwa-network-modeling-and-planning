#!/usr/bin/python

import logging
import numpy as np

# Logging definitions
log_level = logging.DEBUG
log_format = "[%(asctime)s] - %(levelname)s - %(message)s"
datefmt = '%d-%b-%y %H:%M:%S'
log_fn = 'util.log'
logging.basicConfig(filename=log_fn, level=log_level, format=log_format, datefmt=datefmt)

def get_atmosphericloss(d,f):
    """ 
    Lookup table with atmospheric path loss, obtained from ITU recommendation P.676-12.

    Params
    ------
    d : integer
        Distance in m between the nodes.
    f : integer
        Carrier frequency in Hz.

    Return
    ------
    al : float
        Atmospheric loss in dB
    """ 
    sa = 0
    if f == 28e9: 
        sa = 0.06
    elif f == 60e9: 
        sa = 20
    elif f == 140e9: 
        sa = 0.4
    else:
        logging.info('Unsupported frequency for atmospheric loss')

    al = sa * d / 1000

    return al


def get_rain_attenuation(d, f, pr):
    """ 
    Lookup table with rain attenuation

    Params
    ------
    d : integer
        Distance in m between the nodes.
    f : integer
        Carrier frequency in Hz.
    pr : float
        Rain rate in mm/h
    Return
    ------
    ra : float
        Rain attenuation in dB
    """
    sa = 0
    if f == 28e9: 
        if pr == 15:
            sa = 0
        elif pr == 25:
            sa = 0
    elif f == 60e9: 
        if pr == 15:
            sa = 6.8
        elif pr == 25:
            sa = 10.1
    elif f == 140e9: 
        if pr == 15:
            sa = 9.0
        elif pr == 25:
            sa = 12.6
    else:
        logging.info('Unsupported frequency for rain attenuation')

    ra = sa * d / 1000

    return ra


def get_vegetation_attenuation(d, f):
    """ 
    Lookup table with vegetation attenuation

    Params
    ------
    d : integer
        Vegetation depth.
    f : integer
        Carrier frequency in Hz.

    Return
    ------
    va : float
        Vegetation attenuation in dB
    """
    va = 0
    if f < 100e9: 
        # COST 235 model
        va = 15.6 * np.power(f/1e6, -0.009) * np.power(d, 0.26)
    elif (f > 110e9) and (f < 170e9): 
        # VED model 
        pai = 3;
        va = 20.4 * np.power(f/1e9, -0.4) * np.power(d, 0.3) * np.power(pai, 0.9)
    else:
        logging.info('Unsupported frequency for vegetation attenuation')

    return va


def get_pathloss(d, f=60e9, sa=0, vd=0, pr=0):
    """ 
    Return free space path loss, calculated via Friis formula

    Params
    ------
    d : integer
        Distance in m between the nodes.
    f : integer
        Carrier frequency in Hz.
    sa: float
        Specific attenuation in dB/km.
    vd: float
        Percentage of link distance covered by vegetation.
    pr : float
        Precipitation rate in mm/h.
 

    Return
    ------
    pl : float
        Calculated path loss in dB
    """

    # Speed of light in air
    c = 3e8;

    # Free space path loss
    fspl = 20 * np.log10(4 * np.pi * d * f / c)

    # Atmospheric loss
    al = get_atmosphericloss(d,f)

    # Attenuation  due to rain
    ra = get_rain_attenuation(d, f, pr)

    # Attenuation  due to vegetation
    va = get_vegetation_attenuation(vd*d, f)

    # Total path loss
    pl = fspl + al + ra + va + sa*d/1000
    pl = 71.0 + 17.8 * np.log10(d) + va + ra

    return pl


def get_throughput_Ieee80211ad(prx):
    """ 
    Lookup table for MCS and throughput for IEEE Std. 802.11ad based on received power

    Params
    ------
    prx : float
        Received power in dBm.

    Return
    ------
    tp : float
        Throughput in Mbps
    """

    tp = 0

    # Data rate as a function of received power
    Prs = [-78 , -68 , -66 , -64 , -64 , -62 , -63 , -62 , -61 , -59 , -55 , -54 , -53]
    DR = [27.5 , 385 , 770 , 962.5 , 1155 , 1251 , 1540 , 1925 , 2310 , 2502 , 3080 , 3850 , 4620]

    for prs in Prs: 
        if prs < prx: tp = DR[Prs.index(prs)]

    return tp


def get_throughput_mmWave5G(prx):
    """ 
    Lookup table for MCS and throughput for 5G at 28 GHz, based on received power

    Note: from https://nrcalculator.firebaseapp.com/cheatsheet.html: 
        maxThroughput = (modulation bits) x (scaling factor) x (coding rate) x (PRB x 12 / ( 10^-3 / (14 * 2^numerology))) x (1 - overhead) x (number of layers)

    From https://support.tetcos.com/support/solutions/articles/14000136717-calculating-the-5g-data-rate:
        Date Rate = N * Q * R * f * (Nprb * 12 / Ts) * (1 - OH)
        where N is the number of layers, Q is the modulation order, R is the code rate, f is a scaling factor, Nprb is the maximum Resource Block allocation, Ts is the symbol duration and OH is the overhead. Complete details of this are provided in NetSim's 5G user manual.
    Params
    ------
    prx : float
        Received power in dBm.

    Return
    ------
    tp : float
        Throughput in Mbps
    """
    noisefloor = -84 # Thermal noise, 10*log10(k B T / 1mW) with B = 1 GHz
    snr_input = prx - noisefloor

    # Data rate as a function of SNR, with 1/3 code rate
    #           bpsk qpsk 16qam 64qam 256qam
    # mod. order 2   4     16 ...  
    #   1.0e+04 * [0.0194    0.0388    0.1552    0.6207    2.4828 ]
    Snr_min = [2.2, 5.2, 12.7, 19.2, 25.2]
    DR = [dr / 3 for dr in [760, 1530, 3060, 4590, 6110]]

    for snr in Snr_min: 
        if snr < snr_input: tp = DR[Snr_min.index(snr)]

    return tp


def get_linkbudgetparameters():
    Pt = 10
    Gt = 32.3
    Gr = 32.3
    Lt = 2.5
    Lr = 0
    Mi = 3

    return [Pt, Gt, Gr, Lt, Lr, Mi]


def get_throughput(pl,f=60e9):
    """ 
    Return maximum throughput, calculated via link budget

    Params
    ------
    pl : float
        Link path loss
 

    Return
    ------
    tp : integer
        Maximum throughput in Mbps
    """

    # Initialization
    tp = 0

    # Link budget parameters
    [Pt, Gt, Gr, Lt, Lr, Mi] = get_linkbudgetparameters()

    # Calculate received power
    prx = Pt + Gt + Gr - Lt - Lr - Mi - pl

    if f == 60e9: 
        tp = get_throughput_Ieee80211ad(prx)
    elif  f == 28e9: 
        tp = get_throughput_mmWave5G(prx)
    else:
        logging.info('Unsupported frequency for throughput calculation')

    return tp


def get_capacity(pl,f=60e9):
    """ 
    Return link capacity, calculated via Shannon 

    Params
    ------
    pl : float
        Link path loss in dB

    f : integer
        Carrier frequency in Hz
 

    Return
    ------
    cap : integer
        Channel capacity in Mbps
    """

    # Link budget parameters
    [Pt, Gt, Gr, Lt, Lr, Mi] = get_linkbudgetparameters()

    # Calculate received power
    prx = Pt + Gt + Gr - Lt - Lr - Mi - pl

    # Get channel bandwidth
    if f == 28e9: 
        bw = 400e6;
    elif f == 60e9: 
        bw = 2e9;
    elif f == 140e9:
        bw = 4e9;
    else:
        logging.info('Unsupported frequency for capacity calculation')

    # Define noise floor (thermal noise)
    k = 1.381e-23; # Boltzmann's constant
    T = 293; # Temperature in Kelvin (20º)
    nf = 10 * np.log10( k * bw * T / 1e-3 )

    # Define signal-to-noise ratio
    snr = prx - nf;

    cap = bw * np.log2(1 + np.power(10, snr/10)) / 1e6

    return cap
