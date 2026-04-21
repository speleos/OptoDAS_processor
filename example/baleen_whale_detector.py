# --- Baleen whale call detector ---

# --- USER SETTINGS
# ---------------------------------------------------------------------------
# Detection mode:
# "single" = run on one channel defined by CHANNEL_IDX
# "auto"   = choose automatically the strongest channel and run on that one
# "all"    = run on all channels in the stream
DETECT_MODE = "single"     # "single", "auto", or "all"
CHANNEL_IDX = 337          # used only when DETECT_MODE = "single"

# Initial detection parameters
BAND_DETECT = (15, 25)   # Frequency band used for filtering, amplitude calculation, and peak search
ENV_WIN = 0.2            # Length of the smoothing window applied to the amplitude
THRESH = 4.5             # Detection threshold relative to the median filtered amplitude
MIN_DIST = 8.0           # Minimum spacing between consecutive detections to avoid false positives

# Cross-correlation with a matched filter
TEMPLATE_PATH = "./finwhale_100Hz.txt"
TEMPLATE_FS = 100.0     # Original sampling rate of the template. If different from stream, it is resampled
SEARCH_WIN_SEC = 1.0    # Time window used to search for the best correlation peak
CORR_THRESH = 0.15      # Minimum correlation value required to keep a detection

# Spectrogram parameters
SPEC_SOURCE = "raw"     # Trace used for the spectrogram, "raw" or "filtered" data
SPEC_FMIN = 10          # Frequency interval
SPEC_FMAX = 40
SPEC_NPERSEG = 1042     # Number of samples per spectrogram window
SPEC_NOOVERLAP = 900    # Number of overlapping samples between consecutive windows
SPEC_NFFT = 2048
SPEC_DR = 15            # Display dynamic range in dB below the maximum plotted level
CMAP = "jet"

# --- GENERAL FUNCTIONS
# ---------------------------------------------------------------------------
def bandpass(x, fs, lo, hi, order=4):
    nyq = 0.5 * fs
    lo = max(0.001, float(lo))
    hi = min(float(hi), nyq * 0.99)
    b, a = butter(order, [lo / nyq, hi / nyq], btype="band")
    return filtfilt(b, a, x)

def rms(x):
    x = np.asarray(x, dtype=float)
    return np.sqrt(np.mean(x**2))

def print_stats(name, values, fmt="{:.3f}"):
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if values.size == 0:
        print(f"{name} Mean:    n/a")
        print(f"{name} Median:  n/a")
        print(f"{name} Std:     n/a")
        print(f"{name} min:     n/a")
        print(f"{name} max:     n/a")
        return
    print(f"{name} Mean:    " + fmt.format(np.mean(values)))
    print(f"{name} Median:  " + fmt.format(np.median(values)))
    print(f"{name} Std:     " + fmt.format(np.std(values)))
    print(f"{name} min:     " + fmt.format(np.min(values)))
    print(f"{name} max:     " + fmt.format(np.max(values)))

def centers_to_edges(c, start=None, end=None):
    c = np.asarray(c, dtype=float)
    if len(c) == 1:
        if start is None:
            start = c[0] - 0.5
        if end is None:
            end = c[0] + 0.5
        return np.array([start, end], dtype=float)

    edges = np.empty(len(c) + 1, dtype=float)
    edges[1:-1] = 0.5 * (c[:-1] + c[1:])

    if start is None:
        start = c[0] - 0.5 * (c[1] - c[0])
    if end is None:
        end = c[-1] + 0.5 * (c[-1] - c[-2])

    edges[0] = start
    edges[-1] = end
    return edges

def trace_label(tr, idx):
    station = getattr(tr.stats, "station", "")
    if station:
        return station
    return f"channel_{idx}"

def prepare_template(fs):
    tpl = np.loadtxt(TEMPLATE_PATH).astype(np.float64)
    tpl -= tpl.mean()

    if TEMPLATE_FS != fs:
        tpl = resample_poly(
            tpl,
            up=int(round(fs)),
            down=int(round(TEMPLATE_FS))
        ).astype(np.float64)
        tpl -= tpl.mean()

    n_tpl = len(tpl)
    pulse_width = (n_tpl - 1) / fs
    half_pulse_samp = int(round(0.5 * pulse_width * fs))
    n_search_window = int(round(SEARCH_WIN_SEC * fs))

    # zero + master + zero
    tpl_plus = np.concatenate([np.zeros(n_tpl), tpl, np.zeros(n_tpl)])

    return tpl, tpl_plus, n_tpl, half_pulse_samp, n_search_window

def auto_choose_channel(stream):
    peaks = []
    for i, tr in enumerate(stream):
        x_raw = tr.data.astype(np.float64)
        fs = float(tr.stats.sampling_rate)
        x_det = bandpass(x_raw, fs, *BAND_DETECT)
        peaks.append(np.nanmax(np.abs(x_det)))
    return int(np.nanargmax(peaks))

def process_trace(tr, idx):
    x_raw = tr.data.astype(np.float64)
    fs = float(tr.stats.sampling_rate)
    start_time = tr.stats.starttime.datetime
    channel_label = trace_label(tr, idx)

    tpl, tpl_plus, n_tpl, half_pulse_samp, n_search_window = prepare_template(fs)

    # Detection trace
    x_det = bandpass(x_raw, fs, *BAND_DETECT)

    env = np.abs(x_det)

    win_n = max(1, int(ENV_WIN * fs))
    amp_smooth = np.convolve(env, np.ones(win_n) / win_n, mode="same")

    thr = THRESH * np.median(env)
    dist = max(1, int(MIN_DIST * fs))

    raw_picks, _ = find_peaks(
        amp_smooth,
        height=thr,
        distance=dist
    )

    results = []

    for p in raw_picks:
        approx_start = max(0, p - half_pulse_samp)

        i0 = approx_start - n_tpl
        i1 = approx_start + 2 * n_tpl

        if i0 < 0 or i1 > len(x_det):
            continue

        st2 = x_det[i0:i1]

        if len(st2) != len(tpl_plus):
            continue

        cc = obspy_cc(
            st2,
            tpl_plus,
            n_search_window,
            normalize="naive",
            method="direct",
            demean=True
        )

        i_max = int(np.argmax(cc))
        master_corr = float(np.max(cc))
        master_shift = (i_max - n_search_window) / fs

        if master_corr < CORR_THRESH:
            continue

        refined_start = approx_start + (i_max - n_search_window)

        sig0 = refined_start
        sig1 = refined_start + n_tpl
        noi0 = refined_start - n_tpl
        noi1 = refined_start

        if noi0 < 0 or sig1 > len(x_det):
            continue

        signal_win = x_det[sig0:sig1]
        noise_win = x_det[noi0:noi1]

        amp_max = float(np.max(np.abs(signal_win)))
        signal_rms = float(rms(signal_win))
        noise_rms = float(rms(noise_win))
        snr = np.nan if noise_rms == 0 else signal_rms / noise_rms

        tsec = refined_start / fs
        abs_time = start_time + timedelta(seconds=float(tsec))

        results.append({
            "sample": int(refined_start),
            "time_s": float(tsec),
            "datetime": abs_time,
            "corr": float(master_corr),
            "shift_s": float(master_shift),
            "amp_max": float(amp_max),
            "signal_rms": float(signal_rms),
            "noise_rms": float(noise_rms),
            "snr": float(snr),
        })

    return {
        "idx": idx,
        "label": channel_label,
        "fs": fs,
        "start_time": start_time,
        "x_raw": x_raw,
        "x_det": x_det,
        "amp_smooth": amp_smooth,
        "thr": thr,
        "raw_picks": raw_picks,
        "results": results,
    }

def choose_plot_result(processed):
    if len(processed) == 1:
        return processed[0]

    # Prefer the channel with the most kept detections
    kept_counts = [len(p["results"]) for p in processed]
    if np.max(kept_counts) > 0:
        return processed[int(np.argmax(kept_counts))]

    # If none kept, use the one with most raw picks
    raw_counts = [len(p["raw_picks"]) for p in processed]
    return processed[int(np.argmax(raw_counts))]


# --- BASIC CHECKS
# ---------------------------------------------------------------------------
if st==None or len(st) == 0:
    raise RuntimeError("Stream 'st' is empty.")

if not os.path.exists(TEMPLATE_PATH):
    raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")

# --- CHANNEL SELECTION
# ---------------------------------------------------------------------------
if DETECT_MODE not in ("single", "auto", "all"):
    raise ValueError("DETECT_MODE must be 'single', 'auto', or 'all'")

if DETECT_MODE == "single":
    if CHANNEL_IDX is None:
        raise ValueError("Set CHANNEL_IDX when DETECT_MODE = 'single'")
    if CHANNEL_IDX < 0 or CHANNEL_IDX >= len(st):
        raise IndexError(f"CHANNEL_IDX out of range: {CHANNEL_IDX}")
    process_indices = [CHANNEL_IDX]

elif DETECT_MODE == "auto":
    auto_idx = auto_choose_channel(st)
    process_indices = [auto_idx]

else:  # DETECT_MODE == "all"
    process_indices = list(range(len(st)))


# --- RUN DETECTOR
# ---------------------------------------------------------------------------
processed = []
for idx in process_indices:
    processed.append(process_trace(st[idx], idx))

# Channel used for plotting
plot_result = choose_plot_result(processed)

# Flatten all kept detections for global summary
all_results = []
for p in processed:
    for rec in p["results"]:
        rec2 = rec.copy()
        rec2["channel_idx"] = p["idx"]
        rec2["channel_label"] = p["label"]
        all_results.append(rec2)


# --- OUTPUT
# ---------------------------------------------------------------------------
if DETECT_MODE in ("single", "auto"):
    p = processed[0]
    print(f"Detection mode       : {DETECT_MODE}")
    print(f"Chosen channel index : {p['idx']}")
    print(f"Chosen channel label : {p['label']}")
    print(f"Sampling rate        : {p['fs']:.1f} Hz")
    print(f"Frequency BW         : {BAND_DETECT} Hz")
    print(f"ENV_WIN              : {ENV_WIN} s")
    print(f"Raw picks            : {len(p['raw_picks'])}")
    print(f"Kept detections      : {len(p['results'])}")

    for i, rec in enumerate(p["results"], start=1):
        print(
            f"{i:02d} | t = {rec['time_s']:7.2f} s | {rec['datetime']} | "
            f"Cmax = {rec['corr']:.3f} | Shift = {rec['shift_s']:.3f} s | "
            f"Amp = {rec['amp_max']:.3f} | Signal RMS = {rec['signal_rms']:.3f} | "
            f"Noise RMS = {rec['noise_rms']:.3f} | SNR = {rec['snr']:.2f}"
        )

else:
    print(f"Detection mode       : {DETECT_MODE}")
    print(f"Processed channels   : {len(processed)}")
    print(f"Frequency BW         : {BAND_DETECT} Hz")
    print(f"ENV_WIN              : {ENV_WIN} s")
    print()

    nonzero = [p for p in processed if (len(p["raw_picks"]) > 0 or len(p["results"]) > 0)]
    print(f"Channels with picks  : {len(nonzero)}")
    print(f"Total kept detections: {len(all_results)}")
    print()

    # Print concise summary only for channels with at least one raw or kept detection
    for p in nonzero:
        print(
            f"idx={p['idx']:5d} | label={p['label']} | "
            f"raw={len(p['raw_picks']):3d} | kept={len(p['results']):3d}"
        )

# --- SUMMARY STATS
print("*******************************")
print(f"Number of lines found {len(all_results)}")

if len(all_results) > 0:
    cmax_arr = [r["corr"] for r in all_results]
    shift_arr = [r["shift_s"] for r in all_results]
    snr_arr = [r["snr"] for r in all_results]

    print_stats("Cmax", cmax_arr, "{:.3f}")
    print()
    print_stats("Shift", shift_arr, "{:.3f}")
    print()
    print_stats("SNR", snr_arr, "{:.3f}")


# --- PLOT: DETECTION RESULTS + SPECTROGRAM
# ---------------------------------------------------------------------------
picks = np.array([rec["sample"] for rec in plot_result["results"]], dtype=int)
raw_picks = plot_result["raw_picks"]
amp_smooth = plot_result["amp_smooth"]
thr = plot_result["thr"]
fs = plot_result["fs"]
x_raw = plot_result["x_raw"]
x_det = plot_result["x_det"]
channel_label = plot_result["label"]
channel_idx = plot_result["idx"]
start_time = plot_result["start_time"]

t = np.arange(len(amp_smooth)) / fs
x_spec = x_raw if SPEC_SOURCE == "raw" else x_det

f, tt, Sxx = spectrogram(
    x_spec,
    fs=fs,
    window="hann",
    nperseg=SPEC_NPERSEG,
    noverlap=SPEC_NOOVERLAP,
    nfft=SPEC_NFFT,
    detrend=False,
    scaling="spectrum",
    mode="magnitude"
)

Sxx_db = 20 * np.log10(Sxx + 1e-12)
sel = (f >= SPEC_FMIN) & (f <= SPEC_FMAX)

duration = len(x_spec) / fs
t_edges = centers_to_edges(tt, start=0.0, end=duration)
f_sel = f[sel]
f_edges = centers_to_edges(f_sel)

vmax = np.percentile(Sxx_db[sel, :], 99.9)
vmin = vmax - SPEC_DR

fig, (ax0, ax1) = plt.subplots(
    2, 1, figsize=(12, 6), sharex=True,
    gridspec_kw={"height_ratios": [1, 2]}
)
fig.subplots_adjust(right=0.80, hspace=0.10)

# Top panel: smoothed amplitude
ax0.plot(t, amp_smooth, lw=1.0, color="black", label="Smoothed amplitude")
ax0.axhline(thr, color="red", ls="--", lw=1.0, label="Amplitude threshold")

if len(raw_picks):
    ax0.plot(
        raw_picks / fs,
        amp_smooth[raw_picks],
        "o",
        ms=4,
        mfc="none",
        mec="orange",
        label="Raw picks"
    )

ax0.set_ylabel("Amplitude")
ax0.set_title(f"Channel {channel_idx} ({channel_label}) | start = {start_time}")
ax0.set_xlim(0, duration)
ax0.legend(
    loc="upper left",
    bbox_to_anchor=(1.01, 1.0),
    borderaxespad=0.0,
    frameon=False
)

# Bottom panel: spectrogram
ax1.pcolormesh(
    t_edges,
    f_edges,
    Sxx_db[sel, :],
    shading="flat",
    cmap=CMAP,
    vmin=vmin,
    vmax=vmax
)

ax1.set_ylim(SPEC_FMIN, SPEC_FMAX)
ax1.set_xlim(0, duration)
ax1.set_ylabel("Frequency (Hz)")
ax1.set_xlabel("Time (s)")

for p in picks:
    ax1.axvline(p / fs, color="white", ls="--", lw=1.0, alpha=0.9)

plt.setp(ax0.get_xticklabels(), visible=False)
plt.savefig('Whale_detector.png', bbox_inches='tight', pad_inches=0)
plt.show()
plt.close()
