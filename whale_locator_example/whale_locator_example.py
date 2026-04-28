# File to load (uncomment or type in the name of the one interested in):
file = "pos_test_100.0Hz.mseed"
# file = "neg_test_100.0Hz.mseed"


# Settings for the envelope plots:
vmin=.7
vmax=2
cmap="Greys"
plotwidth = 6
plotlength = 8


# Parameters for the whale call curve calculation:
c = 1.5                 # Velocity in water (km/s).
maxdist = 8             # Length of whale call in either direction from central point (km).
whale_distance_min = 0  # Search distance of whale to the cable (km). 
whale_distance_max = 12


# Parameters for the signal search:
# (Here, the distance and time limits are determined by the size of the mseed files that are provided.)
km_min = 9              # Search distance along the cable (km).
km_max = 40
km_step = 1             # Be aware that time will increase quite fast when increasing the resolution.
time_min = 0            # Search time interval (s).
time_max = 70
time_step = 1
max_detections = 10     # Maximum number of features to be found within one set of data.
                        # This is needed, so that the program does not run forever, in case something goes wrong.
threshold = 300         # Minimum required amplitude to be classified as potential whale call.
                        # This value might need to be calibrated more with further data.
                        # At the moment it is based on the difference in amplitude measured on the negative and the positive example.
                        # (See notes at the end.)

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sp
from scipy import ndimage
from obspy import Stream, read

def fkfilt(data,nnx,nns,dx,dt,min_channel,max_channel,vmin=1400,vmax=1600,xint=1,xmin=0,tint=1,\
           tmin=0,blur=10,wavdir='both',plot_filter=True,plot_result=True):
    
    fs=1/dt
    print("Return the Discrete Fourier Transform sample frequencies...")
    f = np.fft.fftfreq(nns,d=1/fs)
    k = np.fft.fftfreq(nnx,d=dx*xint) # Needs to be multiplied by xint!
    
    f = np.fft.fftshift(f)
    k = np.fft.fftshift(k)
    
    print("Compute the 2-dimensional discrete Fourier Transform...")
    ft2 = np.fft.fft2(data)
    del data
    ft2s=np.fft.fftshift(ft2)
    del ft2
    
    print("Return a list of coordinate matrices from coordinate vectors...")
    F,K = np.meshgrid(f,k)
    del f, k
    
    # Change null values to very small ones to be able to divide afterwards.
    K = np.where(K==0, 1e-10, K)
    C = F/K
    
    print("Create filter mask...")
    # Create a mask of zeros in the same shape as C.
    filt = np.zeros(C.shape)
    # Create a mask to "mute" entries by replacing zeros with ones where C is in the desired range.
    condition = np.logical_and(np.abs(C) >= vmin, np.abs(C) <= vmax)
    filt[condition] = 1.

    if wavdir=='pos':
        condition2 = ((K > 0) | (F > 0)) & ((K < 0) | (F < 0))
        filt[condition2] = 0
    if wavdir=='neg':
        condition2 = ((K < 0) | (F > 0)) & ((K > 0) | (F < 0))
        filt[condition2] = 0
    del C,F,K
    
    # Blur mask.
    sigval=int(blur/xint)
    filt_blur = ndimage.gaussian_filter(filt, sigma=sigval)
    
    print("Apply mask...")
    ft2_filt = ft2s * filt_blur
    # del fts2
    ft2s_filt = np.fft.ifftshift(ft2_filt)
    del ft2_filt
    # Invert FFT.
    data_filt = np.fft.ifft2(ft2s_filt)
    del ft2s_filt

    if plot_filter==True or plot_result==True:
        import matplotlib.pyplot as plt
    
    if plot_filter==True:
        print("Plot filter design on data...")
        plt.figure(figsize=(5,5))
        # plt.imshow(abs(ft2s.T[0:int(nns/2),:]),aspect='auto',extent=[min(k),max(k),0,max(f)])
        # plt.imshow(np.log10(abs(ft2s.T[0:int(nns/2),:])),aspect='auto',extent=[min(k),max(k),0,max(f)])
        plt.imshow(np.log10(abs(ft2s.T)),aspect='auto',extent=[max(k),min(k),min(f),max(f)])
        plt.gca().invert_xaxis()
        # plt.colorbar()
        # plt.imshow(abs(filt_blur.T[0:int(nns/2),:]-1),extent=[min(k),max(k),0,max(f)],\
        plt.imshow(abs(filt_blur.T-1),extent=[max(k),min(k),min(f),max(f)],\
                   aspect='auto',cmap="Greys",alpha=0.3)
        plt.title("Fourier Transformed Data with filter mask")
        plt.xlabel('Wavenumber (1/m)')
        plt.ylabel('Frequency (Hz)')
        plt.gca().invert_xaxis()
        plt.tight_layout()
        plt.show()

    if plot_result==True:
        print("Calculate envelopes...")
        # Calculate envelopes of filtered traces.
        en_f = abs(sp.hilbert(data,axis=1))
        mdn_f = np.tile(np.median(en_f,axis=1),(nns,1)).T
        enmd_f = en_f / abs(mdn_f)
        
        en_ff = abs(sp.hilbert(data_filt.real,axis=1))
        mdn_ff = np.tile(np.median(en_ff,axis=1),(nns,1)).T
        enmd_ff = en_ff / abs(mdn_ff)
        
        # # Define new time and distance axes
        # timez = (np.arange(nns)*tint)/fs
        # dist = (np.arange(nnx)*xint + xmin)*dx

        print("Plot data before and after filtering...")
        extent=[dx*5*min_channel/1000,dx*5*max_channel/1000,\
                            0,dt*nns]
        # extent=[dfdas.meta["dx"]*5*min_channel[0]/1000,dfdas.meta["dx"]*5*max_channel[0]/1000,\
        #                     0,dfdas.meta["dt"]*dfdas.meta["dimensionSizes"][0]]
        
        plt.figure(figsize=(6,8))
        plt.imshow(enmd_f.T,extent=extent,aspect='auto',\
                   norm='log',origin='lower',cmap='Greys',vmin=.7,vmax=15)
        plt.title("Data before f-k filtering")
        plt.tight_layout()

        plt.figure(figsize=(6,8))
        plt.imshow(enmd_ff.T,extent=extent,aspect='auto',\
                   norm='log',origin='lower',cmap='Greys',vmin=.7,vmax=15)
        plt.title("Data after 2D f-k filter ("+str(vmin)+"< v <"+str(vmax)+" m/s) - "+wavdir)
        plt.tight_layout()
        plt.show()

    return data_filt

st = read(file)
print(file+" shape: "+str(np.shape(st)))
print(st[0].stats)

dt = st[0].stats.delta
dx = 1.0213001907746815 # This value is specific to the Madeira cable. Unfortunately, mseed does not save dx.
time = st[0].stats.starttime
nnx = np.shape(st)[0]
nns = np.shape(st)[1]

# In this case these values are set by the limits of the mseed files, but this can be adapted when other data is used.
min_channel = [1900]
max_channel = [8000]

print("Bandpass")
st.filter(type="bandpass",freqmin=10,freqmax=40,corners=8,zerophase=True)
print("Use f-k filter")
st = fkfilt(st,nnx,nns,dx,dt,min_channel[0],max_channel[0],vmax=99999,plot_filter=False,plot_result=False)
print("Done.")

# Calculate envelope
print("Use only real part of the data.")
en = abs(sp.hilbert(st.real,axis=1))
mdn = np.tile(np.median(en,axis=1),(nns,1)).T
enmd = en / abs(mdn)

# Plot the envelope of the filtered data
fig = plt.figure(figsize=(plotwidth,plotlength))
ax = plt.imshow(enmd.T,aspect='auto',\
                extent=[dx*5*min_channel[0]/1000,dx*5*max_channel[0]/1000,\
                        0,dt*nns],\
                origin='lower',norm="log",cmap=cmap,vmin=vmin,vmax=vmax)
plt.xlabel('Distance (km)')
plt.ylabel('Time (s)')
plt.title("Start time : " + str(time))
plt.tight_layout()
plt.show()

xsearch = np.arange(km_min,km_max,km_step);ysearch = np.arange(time_min,time_max,time_step)
Lsearch = np.arange(whale_distance_min,whale_distance_max)

# Definition of plot range.
xmin = dx*5*min_channel[0]/1000
xmax = dx*5*max_channel[0]/1000
ymin = 0
ymax = dt*nns

fig,axs = plt.subplots(4,3)
fig.set_figheight(12)
fig.set_figwidth(12)

Zlist = []
best_sol = []
for L in Lsearch:
    ampgrid = []
    for xx in xsearch:
        for yy in ysearch:
            xrange = np.arange(xx - maxdist, xx + maxdist, .1)
            yrange = np.ones(len(xrange)) * yy + np.sqrt(L**2 + abs(xrange - xx)**2) / c
            curve = np.concatenate((xrange.reshape(-1,1),yrange.reshape(-1,1)),axis=1)
            ampval = 0
            for cpoint in curve:
                try:
                    ampval += enmd[round((cpoint[0] - xmin) * np.shape(enmd)[0] / (xmax - xmin)),round((cpoint[1] - ymin) * np.shape(enmd)[1] / (ymax - ymin))]
                except:
                    ampval += 0
            ampgrid.append(ampval)
        
    Z = np.array(ampgrid).reshape((len(xsearch),len(ysearch)))
    Zlist.append(Z)
    X, Y = np.meshgrid(xsearch,ysearch)

    ax_flat = axs.flatten()
    clt = ax_flat[L].pcolormesh(X,Y,Z.T,vmin=100)
    ax_flat[L].set_title("L: " + str(L) + " km")
    ax_flat[L].set_xlabel('Distance (km)')
    ax_flat[L].set_ylabel('Time (s)')
    fig.colorbar(clt)
    plt.tight_layout()

    xval=X[Z.T==np.amax(Z)][0]
    yval=Y[Z.T==np.amax(Z)][0]

    print("For L of", L, "maximum amplitude of", np.amax(Z), "found at:", xval, "km", yval, "s")

    best_sol.append([L, xval, yval, np.amax(Z)])

Zarray = np.stack(Zlist)

do_more = 1
detection = 0
takeout = []
while do_more == 1:
    # Find best overall solution.
    best = np.array(best_sol)
    idx = np.argmax(best[:,-1])
    bestL, bestx, besty, bestZ = best[idx, :]

    if bestZ < 300:
        print("")
        print("=======================================")
        print("NO MORE GOOD SOLUTION FOUND HERE. STOP!")
        print("=======================================")
        do_more = 0
    elif detection == max_detections:
        print("==============================================")
        print("TOO MANY DETECTIONS FOR ONE SET OF DATA. STOP!")
        print("==============================================")
        do_more = 0
    else:
        detection += 1
        print("====================")
        print("Best overall result:")
        print("====================")
        print("Distance along cable:",str(bestx),"km")
        print("Time:",str(besty),"s")
        print("Distance from cable:",str(bestL),"km")

        xrange = np.arange(bestx - 8, bestx + 8, .1)
        yrange = np.ones(len(xrange)) * besty + np.sqrt(bestL**2 + abs(xrange - bestx)**2) / c

        # Plot the envelope of the filtered data
        fig = plt.figure(figsize=(6,6))
        ax = plt.imshow(enmd.T,aspect='auto',\
                        extent=[xmin,xmax,ymin,ymax],\
                        origin='lower',norm="log",cmap=cmap,vmin=vmin,vmax=vmax)
        plt.plot(xrange,yrange, 'r-')
        plt.xlabel('Distance (km)')
        plt.ylabel('Time (s)')
        plt.title(str(bestx) + " km; " + str(besty) +" s; Distance from cable: " + str(bestL))
        plt.tight_layout()
        plt.show()

        print("==============================================")
        print("Take area out of the plot and search the rest:")
        print("==============================================")

        minx = bestx - 10
        maxx = bestx + 10
        miny = besty + np.sqrt(bestL**2) / c - 10
        maxy = besty + + np.sqrt(bestL**2 + abs(8)**2) / c + 10

        takeout.append([minx,maxx,miny,maxy])

        print(str(minx),"-",str(maxx),"km")
        print(str(miny),"-",str(maxy),"s")
        print("==============================================")

        mask_x = (xsearch > minx) & (xsearch < maxx)
        mask_y = (ysearch > miny) & (ysearch < maxy)
        Zarray[np.ix_(range(Zarray.shape[0]), mask_x, mask_y)] = 0

        fig,axs = plt.subplots(4,3)
        fig.set_figheight(12)
        fig.set_figwidth(12)

        for L in Lsearch:
            ax_flat = axs.flatten()
            clt = ax_flat[L].pcolormesh(X,Y,Zarray[L,:,:].T,vmin=100)
            ax_flat[L].set_title("L: " + str(L) + " km")
            ax_flat[L].set_xlabel('Distance (km)')
            ax_flat[L].set_ylabel('Time (s)')
            fig.colorbar(clt)

        plt.tight_layout()
        plt.show()
        
        best_sol = []
        for L in Lsearch:
            xval=X[Zarray[L,:,:].T==np.amax(Zarray[L,:,:])][0]
            yval=Y[Zarray[L,:,:].T==np.amax(Zarray[L,:,:])][0]

            print("For L of", L, "maximum amplitude of", np.amax(Zarray[L,:,:]), "found at:", xval, "km", yval, "s")

            best_sol.append([L, xval, yval, np.amax(Zarray[L,:,:])])
