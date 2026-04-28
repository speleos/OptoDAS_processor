from datetime import datetime
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import time
from whale_locator_functions import fkspec, rmean, fkmisfit

# Data from external server - please change these details to work with your data.
days = [20240630,20240701,20240702]
savefig = "/home/idl/SUBMERSE/FIGURES/Fit_fk/"
whatpath="to_define"

# # Test Data stored on this machine for fast processing (just uncomment this part and change the loop further down to "test mode")
# days = "indiv"
# whatpath = "defined"
# fpath = "/home/idl/SUBMERSE/DATA/GeoLAB/Testfolder/"
# theinterval = "225959"
# thefile = str(theinterval) + ".hdf5"
# savefig = fpath+"SAVEFIG/"+theinterval+"/"

# Define seafloor depths at shallowest and lowest point, as well as channel range.
hup=5;hdown=14.5;chmin=460;chmax=560
kk=np.arange(-0.09,0.09,0.0001)

cutoffvalpos = 20
cutoffvalneg = 10

lim_ang1 = 0
lim_ang2 = 0
lim_z_shal = 5
lim_z_deep = 100
adjfac = 2
side = "both"
channelswap = 1
chint = 1

for theday in days:
    if whatpath=="to_define":
        # Change this path accordingly.
        fpath = "/mnt/SUBMERSE/DATA_dphi/"+str(theday)+"/processed/1Hz_30min/"
        arr = np.sort(os.listdir(fpath))
    else:
        fpath=whatpath
    
    savename2=str(theday)+"_CH"+str(chmin)+"-"+str(chmax)+"_cutoffp"+str(cutoffvalpos)+"cutoffn"+str(cutoffvalneg)+"_adjfac"+str(adjfac)
    if os.path.isfile(savename2):
        addname = "new"
        print("RESULTS FILE ALREADY EXISTS, CREATING NEW ONE, MAKE SURE TO CLEAR IT")
    else:
        addname = ""

    resultmat = []
    for thefile in arr:

        start_time = time.time()
        
        # Exclude directories. ONLY FROM Data from external server.
        pathvar = os.path.join(fpath,thefile)
        if os.path.isdir(pathvar):
            continue

        thetime = thefile[0:6]
        hfile = thetime+".hdf5"
        print(fpath+hfile)
        
        fp = h5py.File(fpath+hfile,'r')
        rawData = np.swapaxes(fp['data'],0,1)
        rawMean = rmean(rawData)

        # Introduce some useful parameters.
        ns=fp['header/dimensionSizes'][()][0]
        dt=fp['header/dt'][()]
        fs=1/dt

        nx=fp['header/dimensionSizes'][()][1]
        xint=fp['header/channels'][()][1]-fp['header/channels'][()][0]
        dx=fp['header/dx'][()]*xint

        at=datetime.fromtimestamp(fp['header/time'][()])
        ft=datetime.fromtimestamp(fp['header/time'][()]+dt*ns)

        if channelswap != 1:
            chmin = int(chmin/channelswap)
            chmax = int(chmax/channelswap)

        # Select a block of data from the middle of the cable
        tr = rawMean[chmin:chmax:chint,:]

        # Option to have two runs, one coarse and one fine:
        multipass = True

        if multipass == True:
            incangcoarse = 10
            incangfine = 2
            incangmax = 60
            # We have to add one point to maximum value to get the last point calculated.
            incanglist = range(0,incangmax+incangcoarse,incangcoarse)
            UUcoarse = 0.2
            UUfine = 0.05
            UUmin = -1.0
            UUmax = 1.0
            UUlist = np.arange(UUmin,UUmax+UUcoarse,UUcoarse)
        elif multipass == False:
            incanglist = range(0,60,2)
            UUlist = np.arange(-1,1,0.05)

        misfitlist = []
        misfitlist_fine = []
        # Cycle through different current values (see Williams et al., 2019) and incidence angles (Sladen et al., 2019).
        if multipass == True:
            for UUval in UUlist:
                for incang in incanglist:
                    UU = round(UUval,2)
                    # print(fs,dx,hup,hdown,UU,incang,side,cutoffvalpos,cutoffvalneg,adjfac,lim_ang1,lim_z_down)
                    misfit = fkmisfit(tr,fs,dx,hup,hdown,UU,incang,kk,\
                                    side=side,cutoffvalpos=cutoffvalpos,cutoffvalneg=cutoffvalneg,adjfac=adjfac,lim_ang1=lim_ang1,lim_ang2=lim_ang2,\
                                    lim_z_shal=lim_z_shal,lim_z_deep=lim_z_deep,\
                                    dolimit=True,doplot=False)
                    misfitlist.append(misfit)
            # Find lowest value
            X,Y = np.meshgrid(UUlist,incanglist)
            Z = np.reshape(misfitlist,np.shape(X.T))
            levels1 = np.linspace(np.amin(misfitlist),np.amax(misfitlist),50)
            lowX=X[Z.T==np.amin(Z)]
            lowY=Y[Z.T==np.amin(Z)]
            print("Minimum value at:",lowX[0],lowY[0])
            
            UUmin_fine = lowX[0] - UUcoarse
            if UUmin_fine < UUmin:
                UUmin_fine = UUmin
            UUmax_fine = lowX[0] + UUcoarse
            if UUmax_fine > UUmax:
                UUmax_fine = UUmax
            UUlist_fine=np.arange(UUmin_fine,UUmax_fine+UUfine,UUfine)
            incangmin_fine = lowY[0] - incangcoarse
            if incangmin_fine < 0:
                incangmin_fine = 0
            incangmax_fine = lowY[0] + incangcoarse
            if incangmax_fine > incangmax:
                incangmax_fine = incangmax
            incanglist_fine=np.arange(incangmin_fine,incangmax_fine+incangfine,incangfine)
            
            # Second round in fine grid
            for UUval in UUlist_fine:
                for incang in incanglist_fine:
                    UU = round(UUval,2)
                    misfit = fkmisfit(tr,fs,dx,hup,hdown,UU,incang,kk,\
                                    side=side,cutoffvalpos=cutoffvalpos,cutoffvalneg=cutoffvalneg,adjfac=adjfac,lim_ang1=lim_ang1,lim_ang2=lim_ang2,\
                                    lim_z_shal=lim_z_shal,lim_z_deep=lim_z_deep,\
                                    dolimit=True,doplot=False)
                    misfitlist_fine.append(misfit)


        elif multipass == False:    
            for UUval in UUlist:
                for incang in incanglist:
                    UU = round(UUval,2)
                    misfit = fkmisfit(tr,fs,dx,hup,hdown,UU,incang,kk,\
                                    side=side,cutoffvalpos=cutoffvalpos,cutoffvalneg=cutoffvalneg,adjfac=adjfac,lim_ang1=lim_ang1,lim_ang2=lim_ang2,\
                                    lim_z_shal=lim_z_shal,lim_z_deep=lim_z_deep,\
                                    dolimit=True,doplot=False)
                    misfitlist.append(misfit)
        

        fig, ax = plt.subplots(figsize=(10,8))

        X,Y = np.meshgrid(UUlist,incanglist)
        Z = np.reshape(misfitlist,np.shape(X.T))

        # levels1 = np.linspace(np.amin(misfitlist),np.amax(misfitlist),50)
        levels1 = np.geomspace(np.amin(misfitlist),np.amax(misfitlist),50)
        ax.contour(X,Y,Z.T, levels=levels1,linewidths=.5)
        ax.plot(X,Y,"kx",ms=2)


        if multipass == False:
            lowX=X[Z.T==np.amin(Z)]
            lowY=Y[Z.T==np.amin(Z)]

        elif multipass == True:
            print(UUmin_fine, incangmin_fine, UUmax_fine-UUmin_fine, incangmax_fine-incangmin_fine)
            ax.add_patch(plt.Rectangle((UUmin_fine, incangmin_fine), UUmax_fine-UUmin_fine, incangmax_fine-incangmin_fine, fc="white",zorder=2))

            
            X,Y = np.meshgrid(UUlist_fine,incanglist_fine)
            Z = np.reshape(misfitlist_fine,np.shape(X.T))
            
            levels1 = np.geomspace(np.amin(misfitlist_fine),np.amax(misfitlist_fine),20)
            ax.contour(X,Y,Z.T, levels=levels1,linewidths=.5)
            ax.plot(X,Y,"kx",ms=1)

            lowX=X[Z.T==np.amin(Z)]
            lowY=Y[Z.T==np.amin(Z)]

        UU_min = round(lowX[0],2)
        incang_min = lowY[0]

        ax.plot(UU_min,incang_min,marker="x",c="red",ms=20)
        ax.vlines(UU_min,np.amin(incanglist),lowY,color="red")
        ax.hlines(incang_min,np.amin(UUlist),lowX,color="red")
        
        print("Misfit plot, best solution at "+str(UU_min)+" m/s, "+str(incang_min)+" deg.")
        resultmat.append([thetime, UU_min, lowY[0]])
        
        ax.set_title("Misfit plot, best solution at "+str(UU_min)+" m/s, "+str(incang_min)+" deg.")
        ax.set_xlabel("Current (m/s)")
        ax.set_ylabel("Incidence Angle (deg)")

        savename=str(theday)+"_"+thetime+"_CH"+str(chmin)+"-"+str(chmax)+"_adjfac"+str(adjfac)
        fig.savefig(savefig+"misfit_"+savename+".pdf")
        # plt.show()
        plt.close()


        fig, ax = plt.subplots(figsize=(18,12))
        # Compute the 2-dimensional discrete Fourier Transform.
        ft2s=fkspec(tr)
        nnx = tr.shape[0]
        nns = tr.shape[1]
        # Needs to be multiplied by chint!
        k = np.fft.fftfreq(nnx,d=dx*chint)
        k = np.fft.fftshift(k)
        fft_freqs = np.fft.fftfreq(nns, d=1.0)
        g = 9.81
        incc = np.cos(incang_min/180*np.pi)
        ffup = (np.sqrt(2*np.pi*g*kk/incc*np.tanh(2*np.pi*kk/incc*hup))+UU_min*2*np.pi*kk/incc)/(2*np.pi)
        ffdown = (np.sqrt(2*np.pi*g*kk/incc*np.tanh(2*np.pi*kk/incc*hdown))+UU_min*2*np.pi*kk/incc)/(2*np.pi)
        extend=.5e-2
        im = ax.imshow(abs(ft2s.T[0:int(nns/2),:]), aspect='auto', extent=[-min(k), -max(k), 0, max(fft_freqs)], clim=(0, extend))
        ax.plot(kk,ffup,'r--',kk,ffdown,'b--')
        ax.legend([str(hup)+' m',str(hdown)+' m'])
        ax.set_xlabel('Wavenumber (1/m)')
        ax.set_ylabel('Frequency (Hz)')
        ax.set_title("Current: "+str(UU_min)+" m/s; Incidence Angle: "+str(lowY[0])+" deg")
        ax.invert_xaxis()
        fig.savefig(savefig+"fk_"+savename+".pdf")
        plt.tight_layout()
        plt.close()

        misfit = fkmisfit(tr,fs,dx,hup,hdown,UU_min,incang_min,kk,\
                        side=side,cutoffvalpos=cutoffvalpos,cutoffvalneg=cutoffvalneg,adjfac=adjfac,lim_ang1=lim_ang1,lim_ang2=lim_ang2,\
                        lim_z_shal=lim_z_shal,lim_z_deep=lim_z_deep,\
                        figpath=savefig,figname="detect_"+savename+".pdf",\
                        dolimit=True,doplot=True,dosave=True)
        
        print("--- %s seconds ---" % (time.time() - start_time))

    resultmat = np.array(resultmat, dtype=float)

    np.savetxt(savefig+"00_results_"+savename2+addname+".txt",resultmat,fmt='%06d\t%.2f\t%.2f',delimiter="\t")
    print("Day "+str(theday)+" done.")
