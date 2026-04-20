import datetime,time
import os,sys
import numpy as np
import warnings
from collections.abc import Iterable
from simpledas import h5pydict
import xdas as xd
from sympy import symbols, sympify
import re
import simpledas
import builtins
import math
import h5py
import pandas as pd
import copy

from obspy.core.util import AttribDict
from obspy.taup import TauPyModel
from obspy import UTCDateTime, read, Trace, Stream
from obspy.io.segy.segy import SUFile,SEGYTraceHeader, SEGYBinaryFileHeader
from obspy.io.segy.core import _read_segy
from obspy.signal.array_analysis import array_processing,array_transff_wavenumber,array_transff_freqslowness,get_geometry
from obspy.signal.invsim import cosine_taper
from obspy.imaging.cm import obspy_sequential
from obspy.geodetics import degrees2kilometers,locations2degrees
from obspy.core.inventory import Inventory, Network, Station, Channel, Site
#from obspy.signal.invsim import corn_freq_2_paz

from typing import Literal
from collections.abc import Sequence
from matplotlib import mlab

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
from matplotlib.patches import ConnectionPatch
from matplotlib.transforms import (Bbox, TransformedBbox,
                                   blended_transform_factory)
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import (BboxConnector,
                                                   BboxConnectorPatch,
                                                   BboxPatch)
import scipy.signal as sps
from scipy import signal
from scipy.signal import hilbert, square, ShortTimeFFT
from scipy.signal.windows import gaussian,hann

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import subprocess
from multiprocessing import Process

#check if code is running in jupyter
if hasattr(builtins, "__IPYTHON__"):
    from tqdm.notebook import tqdm
    from ipywidgets import FloatProgress
    #%matplotlib widget
    #%config InlineBackend.print_figure_kwargs = {'bbox_inches':None}
else:
    from tqdm import tqdm

from DAS_processor import *

from sources import sources

from shared_config import   channel_ranges,freq_params,\
                            rms_params,path_params,trace_header,beamforming_kwargs,\
                            station_coordinates,spec_freq_params,clock_offset,\
                            fk_params,acquisition_params,stationxml_params


events_to_process = [
       
        "Get-S3-data",
        "MSEED_20231028-30_A",
    ]


exec_params={
    "save_figures": True,
    "replace_figures": False,
    "save_DFDAS": True,
    "decimate_das": False, 
    "decimate_obspy": False,
    "MSEED": False, "write_MSEED": False,  "stationXML": False, "encode_station_name": True, "julian_date": True, "degrade_coordinates": True, "precision": 3, "error_metres": 200,
    "write_WAV": False,
    "write_SEGY": False,
    "write_SU": False,
    "DEBUG": False,
    "plot_section": True, "plot_land_station": False, "plot_traces": True, "plot_section_colour": False, "plot_stack": False,"land_station_channels": "HH*",
    "plot_spectrogram": False,
    "fkfilt": False, "fk_plot_filt": True, "fk_plot_result": True,
    "plot_envelope": False,  "envelope_cmap": 'Greys', "envelope_vmin": .7, "envelope_vmax": 2,
    "spectrum_vs_channel": False,
    "normalise": False,
    "calc_nsd": False,
    "plot_nsd": False,
    "calc_rms": False,
    "calc_global_snr": False,
    "apply_filter": True,
    "highpass": False,
    "TeCVA": False,
    "MUSIC": False,
    "Hilbert": False,
    "broadband_test": False,
    "Coherence": False, "Coherence_batch_size" : 2000,
    "Beamforming": False, "Arrival_separation": True, "Beamforming_pre_filter": True, "Show_beamforming": True, "Save_beamforming": True,
    "events_to_process": events_to_process,
    "station": station,
    "land_station": land_station,
    "clock_offset": clock_offset,
    "verbose": False, 
}

global_params = {
    "freq_params": freq_params,
    "exec_params": exec_params,
    "running_params": [],
    "rms_params": rms_params,
    "path_params": path_params,
    "stationxml_params": stationxml_params,
    "trace_header": trace_header,
    "channel_ranges": channel_ranges,
    "sources": sources,
    "beamforming_kwargs": beamforming_kwargs,
    "station_coordinates": station_coordinates,
    "spectrogram_freq_params": spec_freq_params,
    "fk_params": fk_params,
    "acquisition_params": acquisition_params,
    "clock_offset": clock_offset,
}


input_output={
    # Inputs
    "min_channel": None,
    "max_channel": None,
    "roi_step": None,
    "filemeta": None,

    # Outputs
     "dfdas": None,
     "st": None,

    # Processing chain
     "process_chain": [],
}

if exec_params.get("verbose"):
    print("exec_params:")
    for key, value in exec_params.items():
        if value:
            print(f"{key}: {value}")

#validate input

for key, value in sources.items():
   source_type = value.get("channel_ranges")
   if source_type not in channel_ranges:
        print(f"{key}: '{source_type}' does not exist in the defined channel_ranges.")
        sys.exit()


print('»»» Processing event windows.')
for event in tqdm(events_to_process, desc="Processing events"):
    if not event in sources:
        valid_events = "\n".join(key for key in sources)
        print(f'{event} not in list of defined events.\nValid events are:\n{valid_events}')
        continue
    else:
        print(f'Working on event: {event}.')
        
    print(f'#########################\n#########################\n\nProcessing event {event}. station: {station},station_coordinates: {station_coordinates[station]}')

    start_time_event = time.time()

    # 1. Initialize
    DAS = DASProcessor(global_params)

    # Get the operation mode, defaulting to 'seismic' if not specified
    event_mode = sources[event].get("mode", "")
    success = False

    with DAS.temporary_event_paths(event):
        if event_mode == "time_lapse":
            DAS.process_time_lapse(event)

        elif event_mode == "s3_download":
            success=get_data_from_S3(
            bucket_name=event_info["s3_bucket"],
            endpoint_url=event_info["endpoint_url"],
            starttime=datetime.datetime.fromisoformat(event_info["start_time"]),
            endtime=datetime.datetime.fromisoformat(event_info["end_time"]),
            local_path=event_info["DAS_data_path"],
            unsigned=event_info["unsigned"]
        )
            if success:
                print(f"S3 download for {event} completed successfully.")
                break
        else:
            # 2. Process event (check if files exist, load data, populate metadata)
            success = DAS.load_event_data(event, station_coordinates, station, mode=event_mode)
    
    # 3. Check result
    if success:
        print("Event data loaded successfully!")
        print(f"Shape of DAS data (samples x channels): {DAS.dfdas.shape}")
        print(f"DFDAS start time: {DAS.datetime_start}, duration: {DAS.duration} seconds.")
    
        event_info = DAS.sources.get(event, {})
        process_chain = event_info.get('process_chain')
        if process_chain: # This evaluates to True if it's a non-empty list
            print(f"Executing process chain for {event}...")
            DAS.run_process_chain() 
            print("Process chain completed.")
        else:
            print(f"No process chain defined for {event}. Skipping automated steps.")
    elif event_mode != "time_lapse":
        print("Event processing failed or no data was found.")

    end_time_event = time.time()
    elapsed_time = end_time_event - start_time_event
    
    print(f"\n>>> FINISHED: {event}")
    print(f">>> Execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("#########################\n")
