def fkspec(data,path=''):
    # 09/02/2024
    """
    ===================================================
    Create f-k spectrum.
    ===================================================
    data           Input data.
    path           Work parth, default is current path.
    ===================================================
    """
    import numpy as np

    # Compute the 2-dimensional discrete Fourier Transform.
    ft2 = np.fft.fft2(data)
    ft2s = np.fft.fftshift(ft2)
    
    return ft2s

def rmean(data):
    # 01/2024
    """
    Remove mean from each individual channel.
    """
    import numpy as np
    nns = np.shape(data)[1]
    mn = np.tile(np.mean(data,axis=1),(nns,1)).T
    data_mn = data - mn

    return data_mn

def fkmisfit(data,fs,dx,z_up,z_down,current,incidence,kk,\
             chint=1,side="both",cutoffvalpos=50,cutoffvalneg=20,adjfac=1,lim_current1=-.3,lim_current2=.3,lim_ang1=0,lim_ang2=0,lim_z_shal=5,lim_z_deep=100,\
             figpath="./",figname="output.pdf",\
             dolimit=False,doshowmisfit=False,doplot=False,dosave=False):
    """
    Calculate misfit between data and theoretical dispersion curve.
    
    Using the following input:
    data            The block of data.
    fs              1/dt
    dx              Spacing of data.
    z_up            Upper limit value of seafloor depth in m (cable depth will change over the interval, so chose both limits).
    z_down          Lower limit value of seafloor depth in m.
    current         Water current value in m/s (e.g., 0.05).
    incidence       Incidence angle of waves (0 to 90 deg).
    kk              Wavenumber vector (span of wavenumbers used for the TDCs (theoretical dispersion curves)).
    
    chint           Interval between selected channels (default: 1, which means "every channel").
    side            Choose which side to fit ("both" (default)/"land"/"sea")
    cutoffval       FOR OPTION 1:
                    The threshold is checked against the maximum in every line (ie. frequency).
                    BUT: for larger frequencies the signal is so faint that it does not make sense to find the maximum there anymore.
                    So, when the strength is less than 1/cutoffval of the strongest total maximum, ignore the output!
                    (default: 1/50 for cutoffvalpos = 50,
                              1/20 for cutoffvalneg = 20)
                    FOR OPTION 2:
                    The threshold is an absolute value. One set of values that has been found to be working with the 2023 data is:
                        0.001 for the landward side.
                        0.0005 for the oceanward side.
    adjfac          Adjustment factor that is applied to the misfit when the TDC is higher (larger f value at same k) than the data point.
                    This way, the TDC is forced to stay mostly below (smaller f value at same k) the points at the (more or less) sharp edge.
                    (default: 1 - no adjustment)
    
    Values for limiting input
    (The term "inner curve" refers to the curve with higher frequencies, which is normally deeper and/or with higher incidence angle.):
    lim_current1    Water current value limit 1 in m/s. (default: -0.3)
    lim_current2    Water current value limit 2 in m/s. (default: 0.3)
    lim_ang1        Incidence angle of waves for inner curve (0 to 90 deg). (default: 0)
    lim_ang2        Incidence angle of waves for outer curve (0 to 90 deg). (default: 0)
    lim_z_deep      Value of seafloor depth in m for inner curve. (default: 100)
    lim_z_shal      Value of seafloor depth in m for outer curve. (default: 5)

    figpath         Path to save the figure. (only if doplot==True; default: in current folder)
    figname         Name of the figure. (only if doplot==True; default: output.png)
    
    dolimit         Decide, whether to take the original data, or the one limited by TDC. (default: do not limit)
    doshowmisfit    Show the individual misfits of upper and lower TDC, as well as total value. (default: do not show)
    doplot          Make a plot of the misfit calculation. (default: do not plot)
    dosave          Save the plot instead of displaying it. (only works if doplot==True)
    """

    import numpy as np
    import copy
    import matplotlib.pyplot as plt
    
    # Calculate theoretical dispersion curves
    g = 9.81
    incc = np.cos(incidence/180*np.pi)

    # Multiply best misfit value with a general factor (gf) to make the numbers easier to read.
    gf = .01
    
    ffup = (np.sqrt(2*np.pi*g*kk/incc*np.tanh(2*np.pi*kk/incc*z_up))+current*2*np.pi*kk/incc)/(2*np.pi)
    ffdown = (np.sqrt(2*np.pi*g*kk/incc*np.tanh(2*np.pi*kk/incc*z_down))+current*2*np.pi*kk/incc)/(2*np.pi)
    
    nnx = data.shape[0]
    nns = data.shape[1]

    # Return the Discrete Fourier Transform sample frequencies.
    f = np.fft.fftfreq(nns,d=1/fs*np.sqrt(2*np.pi))
    # Needs to be multiplied by chint!
    k = np.fft.fftfreq(nnx,d=dx*chint)
    f = np.fft.fftshift(f)
    k = np.fft.fftshift(k)
    fft_freqs = np.fft.fftfreq(nns, d=1.0)

    # Compute the 2-dimensional discrete Fourier Transform.
    ft2s=fkspec(data)

    ffhalf = int(np.shape(ft2s)[1]/2)
    kkhalf = int(np.shape(ft2s)[0]/2)

    # Create threshold. A tval = 2 means 50%.
    tval = 1
    tvalpos = 1
    tvalneg = 1
    
    # Create limit TDCs to exclude values that are too far out.
    incc1 = np.cos(lim_ang1/180*np.pi)
    incc2 = np.cos(lim_ang2/180*np.pi)
    lim1aff=(np.sqrt(2*np.pi*g*kk/incc1*np.tanh(2*np.pi*kk/incc1*lim_z_deep))+lim_current1*2*np.pi*kk/incc1)/(2*np.pi)
    lim1bff=(np.sqrt(2*np.pi*g*kk/incc2*np.tanh(2*np.pi*kk/incc2*lim_z_shal))+lim_current2*2*np.pi*kk/incc2)/(2*np.pi)
    lim2aff=(np.sqrt(2*np.pi*g*kk/incc1*np.tanh(2*np.pi*kk/incc1*lim_z_deep))+lim_current2*2*np.pi*kk/incc1)/(2*np.pi)
    lim2bff=(np.sqrt(2*np.pi*g*kk/incc2*np.tanh(2*np.pi*kk/incc2*lim_z_shal))+lim_current1*2*np.pi*kk/incc2)/(2*np.pi)

    # Put the correct halves together to create two full curves (one UP, one DOWN).
    halfp = int(np.shape(lim1aff)[0]/2)
    limUPff = copy.deepcopy(lim1aff)
    limUPff[halfp:] = lim2aff[halfp:]
    limDOff = copy.deepcopy(lim1bff)
    limDOff[halfp:] = lim2bff[halfp:]

    F,K = np.meshgrid(f,k)
    # Change null values to very small ones to be able to divide afterwards.
    K = np.where(K==0, 1e-10, K)
    C1alim=(2*np.pi*F)/(np.sqrt(2*np.pi*g*K/incc1*np.tanh(2*np.pi*K/incc1*lim_z_deep))+lim_current1*2*np.pi*K/incc1)
    C1blim=(2*np.pi*F)/(np.sqrt(2*np.pi*g*K/incc2*np.tanh(2*np.pi*K/incc2*lim_z_shal))+lim_current2*2*np.pi*K/incc2)
    C2alim=(2*np.pi*F)/(np.sqrt(2*np.pi*g*K/incc1*np.tanh(2*np.pi*K/incc1*lim_z_deep))+lim_current2*2*np.pi*K/incc1)
    C2blim=(2*np.pi*F)/(np.sqrt(2*np.pi*g*K/incc2*np.tanh(2*np.pi*K/incc2*lim_z_shal))+lim_current1*2*np.pi*K/incc2)
    C1 = copy.deepcopy(C1alim)
    C1[halfp:] = C2alim[halfp:]
    C2 = copy.deepcopy(C1blim)
    C2[halfp:] = C2blim[halfp:]

    # Create a mask of zeros in the same shape.
    filt = np.zeros(ft2s.shape)

    # Tests have shown that this number works best
    limitval = 0.4

    # Create a mask to "mute" entries by replacing zeros with ones where C is in the desired range.
    condition = np.logical_and(np.abs(C1) <= limitval, np.abs(C2) >= limitval)
    filt[condition] = 1.

    # Apply mask.
    ft2_filt = ft2s * filt

    # Decide, whether to take the original data, or the one limited by TDC.
    if dolimit==False:
        takedata = ft2s
    elif dolimit==True:
        takedata = ft2_filt

    # Calculate the maximum amplitude (divided by the threshold) on either side.
    allpos = np.amax(abs(takedata[:kkhalf,:ffhalf]))/tval
    allneg = np.amax(abs(takedata[kkhalf:,:ffhalf]))/tval

    # OPTION 1 (relative values)
    ftbinpos = np.zeros(np.shape(takedata))
    ftbinneg = np.zeros(np.shape(takedata))
    for fval in range(0,int(np.shape(takedata)[1]/2)):
        threshpos = np.amax(abs(takedata[:kkhalf,fval]))/tvalpos
        threshneg = np.amax(abs(takedata[kkhalf:,fval]))/tvalneg
        if threshpos < allpos/cutoffvalpos:
            threshpos = allpos/cutoffvalpos
        if threshneg < allneg/cutoffvalneg:
            threshneg = allneg/cutoffvalneg

        ftbinpos[abs(takedata[:,fval]) >= threshpos,fval] = int(1)
        ftbinpos[abs(takedata[:,fval]) < threshpos,fval] = int(0)
        ftbinneg[abs(takedata[:,fval]) >= threshneg,fval] = int(1)
        ftbinneg[abs(takedata[:,fval]) < threshneg,fval] = int(0)

    # ###

    # # OPTION 2 (absolute values)
    # # Use absolute values (in case the maximum amplitude for one slice is unusually low,
    # # which would otherwise translate to the entire f-k space).
    # ftbinpos = np.zeros(np.shape(takedata))
    # ftbinneg = np.zeros(np.shape(takedata))
    # # Find the maximum value per frequency both in land- and seaward direction.
    # for fval in range(0,int(np.shape(takedata)[1]/2)):
    #     locpos = np.amax(abs(takedata[:kkhalf,fval]))
    #     locneg = np.amax(abs(takedata[kkhalf:,fval]))

    #     if locpos > cutoffvalpos:
    #         ftbinpos[abs(takedata[:,fval]) == locpos,fval] = int(1)
    #     if locneg > cutoffvalneg:
    #         ftbinneg[abs(takedata[:,fval]) == locneg,fval] = int(1)
    # ####

    ftbin = copy.deepcopy(ftbinpos)
    ftbin[kkhalf:,:ffhalf] = ftbinneg[kkhalf:,:ffhalf]

    ftbin_half = ftbin[:, :int(np.shape(ftbin)[1]/2)]
    x, y = np.meshgrid(np.linspace(max(fft_freqs), 0, ftbin_half.shape[1]) ,np.linspace(-min(k), -max(k), ftbin_half.shape[0]))

    # Test where the signal first reaches the maximum and set ison from 0 to 1 (or 2 to avoid extra step).
    # Once it drops back down after that, save the k value for that frequency.
    fedge = []
    kedge = []
    fedgeno = []
    kedgeno = []
    ksave = -999
    misfit_up = 0
    misfit_down = 0
    for fval in range(0,int(np.shape(ft2s)[1]/2)):
        #### POSITIVE K SIDE ###
        if side == "both" or side == "land":
            for kval in range(int(np.shape(ft2s)[0]/2)-1,-1,-1):
                if ftbin[kval,fval] == 1:
                    kedge.append(kval)
                    fedge.append(fval)

                    kktemp = y[kval,0]
                    fftemp = x[0,fval]

                    # Check TDC freq value in comparison with data point, to see if the cuve is above or below the point.
                    fupcheck=(np.sqrt(2*np.pi*g*kktemp/incc*np.tanh(2*np.pi*kktemp/incc*z_up))+current*2*np.pi*kktemp/incc)/(2*np.pi)
                    fdowncheck=(np.sqrt(2*np.pi*g*kktemp/incc*np.tanh(2*np.pi*kktemp/incc*z_down))+current*2*np.pi*kktemp/incc)/(2*np.pi)
                    if fupcheck > fftemp:
                        mfacup = adjfac
                    else:
                        mfacup = 1
                    if fdowncheck > fftemp:
                        mfacdown = adjfac
                    else:
                        mfacdown = 1

                    # Calculate difference between data and theoretical values.
                    # Go through all theoretical values and find the smallest one.
                    allmisfit_up = []
                    allmisfit_down = []
                    # To save computational time, go through the loop twice:
                    # 1. coarse over the entire range.
                    # 2. fine around the best value.
                    stepsize = 5
                    for ii in range(0,len(kk),stepsize):
                        allmisfit_up.append([kk[ii],ffup[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffup[ii])**2),ii])
                        allmisfit_down.append([kk[ii],ffdown[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffdown[ii])**2),ii])
                    allmisfit_up_sorted = sorted(allmisfit_up, key=lambda x: x[2])
                    allmisfit_down_sorted = sorted(allmisfit_down, key=lambda x: x[2])
                    for ii in range(allmisfit_up_sorted[0][3]-stepsize,allmisfit_up_sorted[0][3]+stepsize):
                        allmisfit_up.append([kk[ii],ffup[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffup[ii])**2),ii])
                    for ii in range(allmisfit_down_sorted[0][3]-stepsize,allmisfit_down_sorted[0][3]+stepsize):
                        allmisfit_down.append([kk[ii],ffdown[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffdown[ii])**2),ii])
                    allmisfit_up_sorted = sorted(allmisfit_up, key=lambda x: x[2])
                    allmisfit_down_sorted = sorted(allmisfit_down, key=lambda x: x[2])
                    adjpos = np.amax(abs(ft2s[:kkhalf,fval]))/(allpos*tvalpos)
                    # Also decide, whether to apply the weighting factor, or the square root of it, or not apply it at all.
                    # misfit_up += ( allmisfit_up_sorted[0][2] * adjpos * mfacup * gf) ** 2
                    # misfit_down += ( allmisfit_down_sorted[0][2] * adjpos * mfacdown * gf) ** 2
                    misfit_up += ( allmisfit_up_sorted[0][2] * np.sqrt(adjpos) * mfacup * gf) ** 2
                    misfit_down += ( allmisfit_down_sorted[0][2] * np.sqrt(adjpos) * mfacdown * gf) ** 2
                    # misfit_up += ( allmisfit_up_sorted[0][2] * mfacup * gf) ** 2
                    # misfit_down += ( allmisfit_down_sorted[0][2] * mfacdown * gf) ** 2

        #### NEGATIVE K SIDE ###
        if side == "both" or side == "sea":
            for kval in range(int(np.shape(ft2s)[0]/2)+1,np.shape(ft2s)[0]):
                if ftbin[kval,fval] == 1:
                    kedge.append(kval)
                    fedge.append(fval)

                    kktemp = y[kval,0]
                    fftemp = x[0,fval]

                    # Check TDC freq value in comparison with data point, to see if the cuve is above or below the point.
                    fupcheck=(np.sqrt(2*np.pi*g*kktemp/incc*np.tanh(2*np.pi*kktemp/incc*z_up))+current*2*np.pi*kktemp/incc)/(2*np.pi)
                    fdowncheck=(np.sqrt(2*np.pi*g*kktemp/incc*np.tanh(2*np.pi*kktemp/incc*z_down))+current*2*np.pi*kktemp/incc)/(2*np.pi)
                    if fupcheck > fftemp:
                        mfacup = adjfac
                    else:
                        mfacup = 1
                    if fdowncheck > fftemp:
                        mfacdown = adjfac
                    else:
                        mfacdown = 1

                    # Calculate difference between data and theoretical values.
                    # Go through all theoretical values and find the smallest one.
                    allmisfit_up = []
                    allmisfit_down = []
                    # To save computational time, go through the loop twice:
                    # 1. coarse over the entire range.
                    # 2. fine around the best value.
                    stepsize = 5
                    for ii in range(0,len(kk),stepsize):
                        allmisfit_up.append([kk[ii],ffup[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffup[ii])**2),ii])
                        allmisfit_down.append([kk[ii],ffdown[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffdown[ii])**2),ii])
                    allmisfit_up_sorted = sorted(allmisfit_up, key=lambda x: x[2])
                    allmisfit_down_sorted = sorted(allmisfit_down, key=lambda x: x[2])
                    for ii in range(allmisfit_up_sorted[0][3]-stepsize,allmisfit_up_sorted[0][3]+stepsize):
                        allmisfit_up.append([kk[ii],ffup[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffup[ii])**2),ii])
                    for ii in range(allmisfit_down_sorted[0][3]-stepsize,allmisfit_down_sorted[0][3]+stepsize):
                        allmisfit_down.append([kk[ii],ffdown[ii],np.sqrt((kktemp-kk[ii])**2+(fftemp-ffdown[ii])**2),ii])
                    allmisfit_up_sorted = sorted(allmisfit_up, key=lambda x: x[2])
                    allmisfit_down_sorted = sorted(allmisfit_down, key=lambda x: x[2])
                    adjneg = np.amax(abs(ft2s[kkhalf:,fval]))/(allneg*tvalneg)
                    # Also decide, whether to apply the weighting factor, or the square root of it, r not apply it at all.
                    # misfit_up += ( allmisfit_up_sorted[0][2] * adjneg * mfacup * gf) ** 2
                    # misfit_down += ( allmisfit_down_sorted[0][2] * adjneg * mfacdown * gf) ** 2
                    misfit_up += ( allmisfit_up_sorted[0][2] * np.sqrt(adjneg) * mfacup * gf) ** 2
                    misfit_down += ( allmisfit_down_sorted[0][2] * np.sqrt(adjneg) * mfacdown * gf) ** 2
                    # misfit_up += ( allmisfit_up_sorted[0][2] * mfacup * gf) ** 2
                    # misfit_down += ( allmisfit_down_sorted[0][2] * mfacdown * gf) ** 2



    misfit = misfit_up + misfit_down

    if doshowmisfit == True:
        print("MISFIT UP:",misfit_up,"; MISFIT DOWN:",misfit_down,"; MISFIT TOTAL:",misfit)

    if doplot == True:
        fig, ax = plt.subplots(figsize=(6,6))
        extend=.5e-2
        im = ax.imshow(abs(ft2s.T[0:int(nns/2),:]), aspect='auto', extent=[-min(k), -max(k), 0, max(fft_freqs)], clim=(0, extend))

        kplot = y[kedge,0]
        kplotno = y[kedgeno,0]
        fplot = x[0,fedge]
        fplotno = x[0,fedgeno]

        ax.plot(kk,ffup,'b',kk,ffdown,'r')
        if dolimit==False:
            ax.legend([str(z_up)+' m',str(z_down)+' m'])
        elif dolimit==True:
            ax.plot(kk,limUPff,'k--',kk,limDOff,'k--',lw=.75)
            ax.legend([str(z_up)+' m',str(z_down)+' m','detection limit'])

        # Get the positions of 1s
        ones = ftbin_half == 1.0
        ax.scatter(y[ones], x[ones], color='black', s=10, marker='s')

        ax.plot(kplotno,fplotno,"rx")
        ax.plot(kplot,fplot,"x", color='orange', markersize=1)
        ax.vlines(0,0,0.4,lw=1,ls=":",color="black")

        ax.set_xlabel('Wavenumber (1/m)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title("Current: "+str(current)+" m/s; Incidence Angle: "+str(incidence))
        ax.invert_xaxis()
        
        if dosave == True:
            plt.tight_layout()
            plt.show()
            fig.savefig(figpath+figname)
            plt.tight_layout()
            plt.close()
        elif dosave == False:
            plt.tight_layout()
            plt.show()

    return misfit
