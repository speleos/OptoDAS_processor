def plot_combined_das(data, sxx_db, t_edges, f_edges, vmin, vmax, filename=None, times=None):
    # Create a 1x2 grid (1 row, 2 columns)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6, 6), gridspec_kw={'width_ratios': [1, 0.5]})

    # --- LEFT PANEL: DAS Envelope (Distance vs Time) ---
    x_min = dfdas.meta["dx"] * roi_step * min_channel[0] / 1000
    x_max = dfdas.meta["dx"] * roi_step * max_channel[0] / 1000
    y_max_time = dfdas.meta["dt"] * dfdas.meta["dimensionSizes"][0]

    ax0.imshow(data.T, aspect='auto',
               extent=[x_min, x_max, 0, y_max_time],
               origin='lower', norm="log", cmap='Greys', vmin=0.7, vmax=2.0)

    if times is not None:
      for i, t in enumerate(times):
        # Label only the first line so the legend only shows one entry
        label = 'Detections' if i == 0 else ""
        ax0.axhline(y=t,
                   color='red',
                   linestyle='--',
                   linewidth=1,
                   alpha=0.8,
                   label=label)
        ax0.legend(loc='upper right')

    ax0.set_xlabel('Distance (km)')
    ax0.set_ylabel('Time (s)')
    ax0.set_title("DAS Envelope")

    # --- RIGHT PANEL: Spectrogram (Frequency vs Time) ---
    # We transpose Sxx_db and swap t/f edges so Time stays on the Y-axis
    pcm = ax1.pcolormesh(
        f_edges,    # X-axis: Frequency
        t_edges,    # Y-axis: Time
        sxx_db.T,   # Transposed to match Y=Time
        shading="flat",
        cmap='jet', # Or your CMAP variable
        vmin=vmin,      # Or your vmin variable
        vmax=vmax        # Or your vmax variable
    )

    if times is not None:
        for t in times:
            ax1.axhline(y=t,
                        color='red',
                        linestyle='--',
                        linewidth=1,
                        alpha=0.8)

    ax1.set_xlim(SPEC_FMIN, SPEC_FMAX)
    ax1.set_ylim(0, y_max_time) # Ensure Time scale matches ax0
    ax1.invert_xaxis()
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_title("Spectrogram")
    ax1.tick_params(axis='y', which='both', left=True, right=True, labelleft=False, labelright=True)
    ax0.tick_params(axis='y', which='both', left=True, right=True, labelleft=True, labelright=False)

   # Add a colorbar for the spectrogram
   # plt.colorbar(pcm, ax=ax1, label='dB')

    plt.suptitle(f"{filename}\nStart: {dfdas.meta['time']}")
    plt.tight_layout()

    if filename:
        fig.savefig(f'{filename}_combined.png', dpi=300, bbox_inches='tight')

    plt.show()
