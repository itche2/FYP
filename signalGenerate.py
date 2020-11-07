import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, io, filtering
import os
import pdb

def transmit_signal(fs, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, shift=0, nData_frames=1, **kwargs):
##    def transmit_signal(fs, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, Nsc=1, shift=0, nData_frames=1, **kwargs):
    """
    Parameters
    ----------
        fs: float
            desired sampling frequency
        M : int
            QAM order
        N : int
            number of symbols per polarization
        nmodes : int, optional
            number of modes/polarizations
        fb  : float, optional
            symbol rate 
        bitclass : Bitclass object, optional
            class for initialising the bit arrays from which to generate the symbols, by default use
            RandomBits.
        dtype : numpy dtype, optional
            dtype of the array. Should be either np.complex128 (default) for double precision or np.complex64
        **kwargs 
            kword arguments to pass to bitclass
    """
    #Generating signal
    sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, **kwargs)
    
    #Adjusting signal size to number of data frames required
    #Produce bad memory allocation
##    if nData_frames>1:
##        sig_temp = sig
##        for i in range(nData_frames-1):
##            sig_temp = np.hstack([sig_temp, sig])
##        sig=sig.recreate_from_np_array(sig_temp)

    #Resampling signal at transmitter output AWG
    DACrate=fs
    transmitted_sig=sig.resample(DACrate, beta=0.1, renormalise=True) #DAC resampling
    delay(transmitted_sig, shift, nmodes=nmodes)
    transmitted_sig = extend_signal(transmitted_sig,xtnd_w_zero=0) # extending signal to fit 2^18 symbols
    return transmitted_sig

def export_signal(DACrate, sig, M, N, nmodes=1, fb=1, fs=1, bitclass=signals.RandomBits, dtype=np.complex128, compress=False, **kwargs):
##    def export_signal(DACrate, sig, M, N, nmodes=1, fb=1, fs=1, bitclass=signals.RandomBits, dtype=np.complex128, Nsc=1, **kwargs):
    if compress==True:
        #Saving signal to file in compressed form
        sig.save_to_file('saved_signal.txt')

    else:
        #Checking if directory exists
        if not os.path.isdir('data_files'):
            os.makedirs('data_files')

        #Exporting signal properties
        f_sig_p = "data_files/sig_prop.txt"
        f_sig_prop = open(f_sig_p, "w")
        f_sig_prop.writelines(str(DACrate) + '\n' + str(M) + '\n' + str(N) + '\n' + str(nmodes) + '\n' + str(fb) + '\n' + str(bitclass) + '\n' + str(dtype) + '\n' + str(**kwargs) + '\n')    
        f_sig_prop.close()

        #Exporting transmitted signal 
        fname = "data_files"
    ##    with open(fname + "/RRC_PM" + M + "_" + str(fb) + "Gbd_" + str(Nsc) + "_sc_" + str(DACrate) + "GSaps_real_X.txt", 'w') as RX:
    ##        for item in sig.real[0]:
        with open(fname + "/tmp_real_X.txt", 'w') as RX:
            for item in sig.real[0]:
                RX.write('%s\n' % item)
        with open(fname + "/tmp_imag_X.txt", 'w') as IX:
            for item in sig.imag[0]:
                IX.write('%s\n' % item)                
        with open(fname + "/tmp_real_Y.txt", 'w') as RY:
            for item in sig.real[1]:
                RY.write('%s\n' % item)
        with open(fname + "/tmp_imag_Y.txt", 'w') as IY:
            for item in sig.imag[1]:
                IY.write('%s\n' % item)
                    
        #Exporting data generated
        with open(fname + "/data_real_X.txt", 'w') as RX_D:
            for item in sig.symbols.real[0]:
                RX_D.write('%s\n' % item)
        with open(fname + "/data_imag_X.txt", 'w') as IXD:
            for item in sig.symbols.imag[0]:
                IXD.write('%s\n' % item)                
        with open(fname + "/data_real_Y.txt", 'w') as RYD:
            for item in sig.symbols.real[1]:
                RYD.write('%s\n' % item)
        with open(fname + "/data_imag_Y.txt", 'w') as IYD:
            for item in sig.symbols.imag[1]:
                IYD.write('%s\n' % item)

##def extend_signal(sig,xtnd_w_zero=1):        
##    #Extend the signal to 2^18 number of symbols
##    sig_len_xtnd = 2**18-sig.shape[1] #length of extension of signal
##    sig_temp=sig
##
##    #Extend the signal to 2^18 number of symbols with zeros
##    if xtnd_w_zero == 1:    
##        xtnd_arr=np.zeros((2,sig_len_xtnd))
##        sig_temp = np.hstack([sig_temp, xtnd_arr])
##        sig_xtnd=sig.recreate_from_np_array(sig_temp)
##
##    #Extend the signal to 2^18 number of symbols with the signal itself
##    else: 
##        sig_temp = np.hstack([sig_temp, sig[:,:sig_len_xtnd]])
##        sig_xtnd=sig.recreate_from_np_array(sig_temp)
##    return sig_xtnd
##
##def delay(sig, shift, nmodes):
##    if nmodes == 1:
##        sig = np.roll(sig, shift, axis=0) #single polarization desynchronization
##    if nmodes == 2:
##        sig = np.roll(sig, shift, axis=1) #dual polarization desynchronization
##    return sig
    
