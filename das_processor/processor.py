import inspect
import datetime,time
import julian
import os
import numpy as np
import warnings
from collections.abc import Iterable
from rich import inspect
from simpledas import h5pydict
from sympy import symbols, sympify
import re
import simpledas
import xdas as xd
import builtins
import string
import math
import h5py
import pandas as pd
import pickle
import json

import inspect
from contextlib import contextmanager

from obspy.core.util import AttribDict
from obspy.taup import TauPyModel
from obspy import UTCDateTime, read, Trace, Stream
from obspy.io.segy.segy import SUFile,SEGYTraceHeader, SEGYBinaryFileHeader
from obspy.io.segy.core import _read_segy
from obspy.signal.array_analysis import array_processing,array_transff_wavenumber,array_transff_freqslowness,get_geometry
from obspy.signal.invsim import cosine_taper
from obspy.imaging.cm import obspy_sequential
from obspy.geodetics import degrees2kilometers,locations2degrees
from obspy.core.inventory import Inventory, Network, Station, Channel, Site, Comment, Response, Equipment, Operator
from obspy.core.inventory import InstrumentSensitivity, Person, ResponseStage, PolesZerosResponseStage, CoefficientsTypeResponseStage
from obspy.core.inventory import read_inventory
#from obspy.signal.invsim import corn_freq_2_paz

from matplotlib import mlab

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MultipleLocator
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
from matplotlib.patches import ConnectionPatch,Rectangle
from matplotlib.transforms import (Bbox, TransformedBbox,
                                   blended_transform_factory)
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import (BboxConnector,
                                                   BboxConnectorPatch,
                                                   BboxPatch)
import scipy.signal as sps
from scipy import ndimage
from scipy import signal
from scipy.signal import hilbert, square, ShortTimeFFT
from scipy.signal.windows import gaussian,hann

import concurrent.futures
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
import subprocess
from multiprocessing import Process

from memory_profiler import profile

#check if code is running in jupyter
if hasattr(builtins, "__IPYTHON__"):
    from tqdm.notebook import tqdm
    from ipywidgets import FloatProgress
    #%matplotlib widget
    #%config InlineBackend.print_figure_kwargs = {'bbox_inches':None}
else:
    from tqdm import tqdm

from shared_config import channel_ranges
from sources_list import sources

# define class for storing results

class DASProcessor:
    def __init__(self, global_params):
        self.exec_params = global_params.get('exec_params', {})
        self.path_params = global_params.get('path_params', {})
        self.sources = global_params.get('sources', {})
        self.station_coordinates = global_params.get('station_coordinates', {})
        self.acquisition_params = global_params.get('acquisition_params', {})
        self.trace_header = global_params.get('trace_header', {})
        
        # Internal state
        self.files = []
        self.dfdas = None
        self.mseed = None
        self.filemeta = None
        self.roi_step = 0
        self.first_chan = 0
        self.last_chan = 0
        self.event= None
        self.filename_suffix = ""
        
        # New attributes to store parameters calculated during processing
        self.datetime_start = None
        self.duration = None
        self.channels = []
        self.figsize = (10, 8) # Default

    # Channel Results
        self.channels = np.array([])
        self.min_channel = []
        self.max_channel = []
        self.channel_step = []
        self.chIndex = []

    def get_current_params(self):
        """Returns the internal state in the old dictionary format for compatibility."""
        return {
            'exec_params': self.exec_params,
            'path_params': self.path_params,
            'acquisition_params': self.acquisition_params,
            'sources': self.sources,
            'station_coordinates': self.station_coordinates
        }
    
    @contextmanager
    def temporary_event_paths(self, event_name):
        """
        Temporarily overrides path_params for a specific event 
        and restores them automatically.
        """
        # 1. Store original values
        original = {
            "experiment_path": self.path_params.get("experiment_path"),
            "MSEED_path": self.path_params.get("MSEED_path"),
            "events_path": self.path_params.get("events_path")
        }

        # 2. Get new values from sources
        event_info = self.sources.get(event_name, {})
        overrides = {
            "experiment_path": event_info.get("DAS_data_path"),
            "MSEED_path": event_info.get("mseed_output_path"),
            "events_path": event_info.get("events_path")
        }

        # 3. Apply overrides if they exist
        try:
            for key, new_val in overrides.items():
                if new_val:
                    print(f"Override: Setting {key} to {new_val}")
                    self.path_params[key] = new_val
            
            yield  # <--- This is where your processing code runs
            
        finally:
            # 4. RESET to defaults no matter what happens
            for key, old_val in original.items():
                self.path_params[key] = old_val
            print("Paths restored to defaults.")

    def run_process_chain(self, suffix=""):
        """
        Iterates through the 'process_chain' defined in the source 
        and executes methods dynamically.
        Passes a suffix (e.g., '_timelapse_1') to methods for unique filenames
        """
        event_info = self.sources.get(self.event, {})
        chain = event_info.get('process_chain', [])

        for step in chain:
            operation = step.get('operation')
            params = step.get('params',{}) #Ensure it's a dict
            
            # Check if the method exists in the class
            if hasattr(self, operation):
                method = getattr(self, operation)
                print(f"--- Executing: {operation} with params {params} ---")
            
                # 1. Get the function's "menu" of accepted arguments
                sig = inspect.signature(method)
                accepted_keys = sig.parameters.keys()

                # 2. Add 'event' to the params temporarily if the method wants it
                if 'event' in accepted_keys and 'event' not in params:
                    params['event'] = self.event

                # 3. Add 'suffix' if you want to pass it for unique naming
                if 'suffix' in accepted_keys and 'suffix' not in params:
                    params['suffix'] = suffix

                # 4. FILTER: Only keep keys that exist in the method signature
                filtered_params = {k: v for k, v in params.items() if k in accepted_keys}

                print(f"--- Executing: {operation} with params {filtered_params} (from {params}) ---")
            
               # 5. UNPACK and CALL: No more 'if operation == ...' blocks needed!
                method(**filtered_params)
            else:
                print(f"Warning: Method {operation} not found in DASProcessor.")

    def get_time_lapse_windows(self, event):
        """Generates start times for continuous windows."""
        event_info = self.sources.get(event, {})
        start_time = UTCDateTime(event_info.get("start_time"))
        end_time = UTCDateTime(event_info.get("end_time"))
        duration = event_info.get("window_duration")

        start_times = []
        current = start_time
        while current < end_time:
            start_times.append(current)
            current += duration

        print(f'{len(start_times)} windows of {duration}s to process')
        return start_times, duration
    
    def process_time_lapse(self, event):
        """Main loop for time-lapse processing."""
        print(f'»»» Working on time lapse: {event}')
        
        # 1. Generate the windows
        start_times, window_duration = self.get_time_lapse_windows(event)
        self.duration = window_duration # Set window length for the processor

        events_path = self.path_params.get("events_path")
        event_safe = event.replace(" ", "_")

        # 2. Iterate through windows
        for i, start_dt in enumerate(start_times):
            suffix = f"_{start_dt.strftime('%Y%m%d_%H%M')}"
            target_hdf5 = os.path.join(events_path, f"{event_safe}{suffix}.hdf5")

            # Check if we should skip before loading raw data
            if os.path.exists(target_hdf5):
                print(f"Window {i+1}/{len(start_times)}: Skipping (Already exists: {os.path.basename(target_hdf5)})")
                continue

            print(f"\n--- Processing Window {i+1}/{len(start_times)}: {start_dt} ---")
            
            # Update the start time for this iteration
            self.datetime_start = start_dt
            
            # 3. Load data for this specific window
            # This triggers check_data_access -> get_roi_step -> actual loading
            success = self.load_event_data(event, mode="time_lapse")
            
            if success:
                # 4. Execute the chain for this window
                # We pass a suffix so plots/files are named uniquely
                self.filename_suffix = suffix
                self.run_process_chain(suffix=self.filename_suffix)
                
                # Clean up memory/cache for next window
                self.mseed_stream = None 
                self.dfdas = None
            else:
                print(f"Skipping window {i+1} due to loading error.")
    
        return False

    def load_event_data(self, event, station_coordinates=None, station=None, mode='seismic'):
        """
        The main pipeline execution method. 
        """
        print(f'Working on event: {event}.')

        # 1. Initial setup
        self.dfdas = None
        self.mseed_stream = None
        self.event = event
        
        # Accessing sources (ensure sources is available globally or passed in)
        self.acquisition_params["gps_status"] = sources.get(event, {}).get("GPS", False)
        
        # 2. Get initial trim times
        if mode != "time_lapse":
            # Standard logic using station files
            self.figsize, self.datetime_start, self.duration = self.calculate_trim_times(event,station)
        else:
            # Time Lapse Logic: 
            # self.datetime_start was already set by process_time_lapse loop.
            # We MUST ensure it is a native datetime object for simpledas compatibility.
            if hasattr(self.datetime_start, 'datetime'):
                self.datetime_start = self.datetime_start.datetime
            self.figsize = (10, 8) # Default for time-lapse

        # 3. Locate files and metadata
        self.locate_event_data(event)
        if not self.files:
            print(f"No files found for {event}. Execution aborted for this event.")
            return False 
        
        # 4. Handle Stale GPS Logic
        # We check if the GPS status changed after looking at the file headers
        if self.acquisition_params.get("gps_status") == True:
            if sources.get(event, {}).get("GPS") == False:
                print("GPS information was stale. Recalculating start times.")
                figsize, self.datetime_start, self.duration = self.calculate_trim_times(
                    event, {'exec_params': self.exec_params, 'path_params': self.path_params, 'acquisition_params': self.acquisition_params}, 
                    station_coordinates, station
                )
                # Re-locate files with updated time
                self.locate_event_data(event, self.datetime_start)

        # 5. Check if we found anything
        if not self.files:
            print(f'No data available for event {event}. Skipping!')
            return False # Signal to the loop to continue

        # 6. Calculate Channels
        # We pass self.roi_step, self.first_chan, etc., which were filled by locate_event_data
        self.channels, min_ch, max_ch, ch_step = self.calculate_channels(event)

        # Exit early if channels array is empty
        if self.channels.size == 0:  # Use .size for NumPy arrays
            print(f"No valid channels found for event {event}. Exiting.")
            return False

        # 7. Final Load
        self.load_dfdas_file(event, self.datetime_start, self.duration, self.channels)
        
        return True # Success!

    def locate_event_data(self,event):

        events_path = self.path_params.get("events_path")
        experiment_path = self.path_params.get("experiment_path")
        # replace spaces with underscores in event name for filename
        hdf5_file = f'{events_path}/{event.replace(" ", "_")}.hdf5'

        self.event=event

        print(f'Finding files for event: {event}')
        print(f'Trying file list from {events_path}')

        if os.path.exists(hdf5_file):
            self.files=[hdf5_file]
            with h5py.File(self.files[0], "r") as hf_in:
                self.roi_step=hf_in['/demodSpec/roiDec'][0]
                self.first_chan = hf_in['/header/channels'][0]
                self.last_chan = hf_in['/header/channels'][-1]
                ap = self.acquisition_params #shorthand reference
                ap["roi_step"]=hf_in['/demodSpec/roiDec'][0]
                ap["gps_status"]=hf_in['/monitoring/Gps/gpsStatus'][()]
                ap["gauge_length"]=hf_in['/header/gaugeLength'][()]
                ap["dx"]=hf_in['/header/dx'][()]
                
                # Calculate overlap using the newly updated dictionary
                ap["overlap"] = self.roi_step * ap["dx"] / ap["gauge_length"]
        else:
            print(f'Local HDF5 not found. Searching raw data in {experiment_path}')
            time_offset = self.datetime_start# - datetime.timedelta(seconds=10)
            if not self.check_data_access(experiment_path, time_offset):
                print(f"Skipping event {event} due to missing directories.")
                self.files = []
                return self.files, 0, 0, 0
           
           # If check passes, proceed to raw data metadata extraction 
            self.get_roi_step(experiment_path, time_offset)

        return self.files, self.roi_step, self.first_chan, self.last_chan

    def get_roi_step(self, path, datetime_start):
        """
        Extracts ROI and acquisition metadata from DAS files.
        Updates self.acquisition_params directly.
        """
        # Call simpledas using parameters stored in the class
        files, chIndex, samples = simpledas.find_DAS_files(
            path,
            start=datetime_start,
            duration=datetime.timedelta(hours=1),
            show_header_info=self.exec_params.get("verbose"),
            load_file_from_start=True
        )

        if len(files) == 0:
            self.files = []
            self.roi_step = 0
            self.last_chan = 0
            self.first_chan = 0
        else:
            self.files = files
            with h5py.File(self.files[0], "r") as hf_in:
                # Update individual attributes
                self.first_chan = hf_in['/header/channels'][0]
                self.last_chan = hf_in['/header/channels'][-1]
                self.roi_step = hf_in['/demodSpec/roiDec'][0]

                # Update the shared acquisition dictionary
                ap = self.acquisition_params # Shorthand reference
                ap["roi_step"] = self.roi_step
                ap["gps_status"] = hf_in['/monitoring/Gps/gpsStatus'][()]
                ap["gauge_lenght"] = hf_in['/header/gaugeLength'][()]
                ap["dx"] = hf_in['/header/dx'][()]
                ap["original_sample_rate"] = 1.0 / hf_in['/header/dt'][()]
                ap["sensitivity"] = hf_in['/header/sensitivities'][0][0]
                ap["sensitivityUnits"] = hf_in['/header/sensitivityUnits'][0].decode('utf-8')
                
                # Calculate overlap
                ap["overlap"] = ap["roi_step"] * ap["dx"] / ap["gauge_lenght"]

        return self.files, self.roi_step, self.first_chan, self.last_chan

    def calculate_trim_times(self, event, station):
        """
        Calculates figure size, start time, and duration for the event.
        Stores results in self.figsize, self.datetime_start, and self.duration.
        """
        ap = self.acquisition_params
        event_info = sources.get(event, {})
        event_type = event_info.get("channel_ranges")

        print(f'Processing event {event}, of the type {event_type}')
        print('Calculating trim times and figure sizes...')

        # Determine clock offset based on GPS status stored in the class
        if ap.get("gps_status"):
            clock_offset = 0
        else:
            # Note: We assume clock_offset was passed into global_params 
            # and stored in self at __init__
            clock_offset = self.path_params.get("clock_offset", 0) 

        # Logic for Seismic vs Other types
        if event_type.startswith('seismic'):
            self.figsize = (10, 3)
            # Assuming get_travel_times is an external helper
            arrivals_p, arrivals_s = get_travel_times(
                event, 
                self.get_current_params(), # Helper to package params if needed
                self.station_coordinates[station]["latitude"], 
                self.station_coordinates[station]["longitude"]
            )
            
            # Calculate start time with offset
            base_time = UTCDateTime(event_info.get("start_time"))
            trim_time = base_time + arrivals_p[0].time - event_info.get("window_in") + datetime.timedelta(seconds=clock_offset)
            print(f'Time offset correction of {clock_offset}s applied.')
        else:
            self.figsize = (10, 8)
            trim_time = UTCDateTime(event_info.get("start_time")) - event_info.get("window_in")
            print("Time offset not corrected.")

        # Store results in the class instance
        self.datetime_start = trim_time.datetime
        self.duration = datetime.timedelta(seconds=event_info.get("window_out") + event_info.get("window_in"))

        print(f'Datetime start: {self.datetime_start}')
        return self.figsize, self.datetime_start, self.duration

    def load_dfdas_file(self, event, datetime_start, duration, channels):
        """
        Loads the actual DAS data into self.dfdas. 
        Uses the results from locate_event_data if they exist.
        """
        # Accessing class attributes
        ep = self.exec_params
        pp = self.path_params
        ap = self.acquisition_params
        
        event_type = sources.get(event, {}).get("channel_ranges")
        event_mode = sources.get(event, {}).get("mode")

        is_special_type = event_type in ['spectrogram', 'whales', 'spectrogram_currents']
        #local_hdf5 = f'{pp.get("events_path")}/{event}.hdf5'
        # replace spaces with underscores in event name for filename
        local_hdf5 = f'{pp.get("events_path")}/{event.replace(" ", "_")}.hdf5'

        # 1. Logic to decide WHERE to load from
        if is_special_type or event_mode == "time_lapse":
            self.files, ch_idx, samples = simpledas.find_DAS_files(
                pp.get("experiment_path"), channels=channels, 
                start=datetime_start, duration=duration, load_file_from_start=False
            )
            self.dfdas = simpledas.load_DAS_files(self.files, ch_idx, samples, integrate=False)
        else:
            if os.path.exists(local_hdf5):
                try:
                    self.files = [local_hdf5]
                    # This avoids channel re-numbering
                    ch_idx, samples = simpledas.get_data_indexes(self.files[0])
                    self.dfdas = simpledas.load_DAS_files(self.files, ch_idx, samples, integrate=False)
                except ValueError:
                    # Fallback to experiment path if local HDF5 fails
                    self.files, ch_idx, samples = simpledas.find_DAS_files(
                        pp.get("experiment_path"), channels=channels, 
                        start=datetime_start, duration=duration, load_file_from_start=False
                    )
                    self.dfdas = simpledas.load_DAS_files(self.files, ch_idx, samples, integrate=False)
            else:
                self.files, ch_idx, samples = simpledas.find_DAS_files(
                    pp.get("experiment_path"), channels=channels, 
                    start=datetime_start, duration=duration, load_file_from_start=False
                )
                self.dfdas = simpledas.load_DAS_files(self.files, ch_idx, samples, integrate=False)

        # 2. Sanity check using acquisition_params (updated by previous methods)
        if sources.get(event, {}).get("GPS") and ap.get('gps_status') != 0:
            print("Event defined as having locked GPS, but file header indicates otherwise.\nClock offset should be calculated.")

        if ep.get("verbose"):
            print(f'chIndex: {ch_idx}')
            print(f'columns: {self.dfdas.columns}')

        # 3. Store Metadata
        self.filemeta = simpledas.get_filemeta(self.files[0], 2)

        # 4. Save if required
        if ep.get("save_DFDAS") and event_mode != "time_lapse":
            filename_out = simpledas.save_to_DAS_file(
                self.dfdas, local_hdf5, "processed", **self.filemeta
            )
            print(f'Window for event {event} saved to {filename_out[0]}')

        return self.files, self.dfdas, self.filemeta
    

    def save_dfdas_file(self, params=None):
        """
        Saves self.dfdas to an HDF5 file using self.filemeta.
        Automatically constructs the path if 'filename' is not in params.
        """
        if self.dfdas is None:
            print("No data in memory (self.dfdas) to save.")
            return

        # 1. Determine the filename
        # Check if 'filename' was passed in the process_chain dictionary
        p = params if isinstance(params, dict) else {}
        filename = p.get("filename")

        if not filename:
            # Fallback: Construct filename from class attributes
            pp = self.path_params
            event_safe = self.event.replace(" ", "_")
            # Uses the suffix we set in the time_lapse loop
            suffix = getattr(self, 'filename_suffix', "")
            
            filename = os.path.join(
                pp.get("events_path"), 
                f"{event_safe}{suffix}.hdf5"
            )

        # 2. Execute save using class attributes
        try:
            filename_out = simpledas.save_to_DAS_file(
                self.dfdas, 
                filename, 
                "processed", 
                **self.filemeta
            )
            print(f"Data successfully saved to: {filename_out[0]}")
        except Exception as e:
            print(f"Error saving DFDAS file: {e}")

    def calculate_channels(self, event, time_lapse=False):
        """
        Calculates the channels array based on ROI and file headers.
        Uses attributes stored during locate_event_data().
        """
        # Determine source dictionary based on time_lapse flag
        data_source = time_lapses if time_lapse else sources
        event_channel_ranges = data_source.get(event, {}).get("channel_ranges")
        
        if not event_channel_ranges:
            print(f"WARNING: 'channel_ranges' not specified for event '{event}'. Skipping channel calculation.")
            self.channels = np.array([])
            return self.channels, [], [], [] #This will signal an error upstream

        # Get ranges from the global channel_ranges dict
        ranges = channel_ranges.get(event_channel_ranges, {})
        self.min_channel = ranges.get("channel_min", [])
        self.max_channel = ranges.get("channel_max", [])
        self.channel_step = ranges.get("channel_step", [])
        
        temp_channels = []
        
        # Use self.roi_step and self.last_chan stored from previous methods
        for min_ch, max_ch, step_ch in zip(self.min_channel, self.max_channel, self.channel_step):
            top = (max_ch + 1) * self.roi_step if (max_ch + 1) < self.last_chan else self.last_chan
            temp_channels.extend(np.arange(min_ch * self.roi_step, top, step_ch * self.roi_step))
        
        self.channels = np.array(temp_channels)
        
        # Adjustment for non-zero first channel
        if self.first_chan != 0 and self.first_chan < self.roi_step:
            adjustment = self.first_chan - self.roi_step
            print(f'Adjusting channels: {self.channels[0]} -> {self.channels[0] + adjustment}')
            self.channels = self.channels + adjustment
            
        return self.channels, self.min_channel, self.max_channel, self.channel_step

    def dfdas_to_csv(self, params=None):
        """
        Saves the decimated self.dfdas directly to CSV.
        Uses 'csv_path' and appends the timelapse suffix.
        """
        if self.dfdas is None:
            print("No data to save.")
            return

        pp = self.path_params

        # 1. Setup path
        csv_dir = pp.get("csv_out_path")
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # 2. Build filename
        event_safe = self.event.replace(" ", "_")
        filename = f"{event_safe}{self.filename_suffix}.csv"
        full_path = os.path.join(csv_dir, filename)

        # 3. Export
        print(f"»»» Saving CSV format to: {full_path}")
        # index=True includes the timestamps from the 't' axis created in decimation
        self.dfdas.to_csv(full_path, index=True, header=True)


    def dfdas_to_mseed(self,event,write=False,format=None,dType=float,decimate=False,filename=None):
        """
        Converts the stored self.dfdas (Pandas) into an ObsPy Stream object.
        Uses class attributes for metadata and configuration.
        """

        print(f'params: event:{event} write:{write} format:{format} dType:{dType} decimate:{decimate} filename:{filename}')
        if self.dfdas is None:
            print("No data loaded in self.dfdas. Run load_dfdas_file() first.")
            return None
        else:
            print("Converting to ObsPy Stream")

        # Short aliases for cleaner code
        ep, ap, pp, th = self.exec_params, self.acquisition_params, self.path_params, self.trace_header

        self.mseed_stream=Stream()
        for channel in self.dfdas.columns[:]:
            tr = Trace()
            print(f"DEBUG: Current meta keys: {list(self.dfdas.meta.keys())}")
            tr.data = self.dfdas[channel].to_numpy().astype(dType)  # Convert to dType. default is float.
            tr.stats.starttime = UTCDateTime(self.dfdas.meta["time"])
            tr.stats.sampling_rate = 1/self.dfdas.meta["dt"]

            station_code = str(int(channel*ap.get("dx"))).zfill(5)
            if ep.get("encode_station_name"):
                tr.stats['decoded_station'] = station_code
                tr.stats.station = encode_station_name(th.get("station_prefix"),station_code,self.get_current_params())
            else:
                tr.stats.station = station_code
            tr.stats.network = th['network']
            tr.stats.location = th['location']
            tr.stats.mseed = th['mseed']
            tr.stats.channel = th['channel']
            tr.stats.distance = int(channel*self.dfdas.meta["dx"])
            lat, long, ele = get_coordinates(channel, self.get_current_params(),roi_channel=False)
            
            if ep.get("degrade_coordinates"):
                lat,long=degrade_coordinates(lat,long,precision=ep.get("precision"),error_metres=ep.get("error_metres"))
            
            tr.stats.coordinates = {'latitude': lat, 'longitude': long, 'elevation': ele}
            tr.stats.paz= AttribDict({'sensitivity': ap["sensitivity"]})
            # Append the trace to the Stream
            self.mseed_stream.append(tr)

        if decimate:
            self.mseed_stream=decimate_obspy(self.mseed_stream,self.get_current_params())

        if ep.get("stationXML"):
            station_xml_creation(self.mseed_stream,self.get_current_params())   

        if write in ['stream', True]:
            mseed_filename = filename if filename else f'{event}_{self.mseed_stream[0].stats.sampling_rate}Hz.mseed'
            full_path = os.path.join(pp.get("MSEED_path"), mseed_filename)
            self.mseed_stream.write(full_path, format='MSEED')
            print(f'Full stream written to {full_path}')

        elif write == 'channels':
            for tr in self.mseed_stream:
                net = tr.stats.network  # Network code
                sta=tr.stats.station
                loc = tr.stats.location or ""  # Location code (or empty string if not provided)
                chan = tr.stats.channel  # Channel code
                qual= tr.stats.mseed # Data quality flag
                if ep.get("julian_date"):
                    formatted_time=f'{tr.stats.starttime.year:04d}.{tr.stats.starttime.julday:03d}'
                else:
                    formatted_time = tr.stats.starttime.strftime('%Y%m%dT%H%M%S')

                mseed_filename=f'{net}.{sta}.{loc}.{chan}.{qual}.{formatted_time}.mseed'
                mseed_path=os.path.join(pp.get("MSEED_path"),f'{tr.stats.starttime.year:04d}.{tr.stats.starttime.julday:03d}')
            
                if not os.path.exists(mseed_path):
                    os.makedirs(mseed_path)
            
                full_path=os.path.join(mseed_path,mseed_filename)
                tr.write(full_path, format='MSEED',reclen=512)#,encoding='STEIM1')
                print(f'wrote file {full_path} julian_date={ep.get("julian_date")}')

        elif not write:
            print("Stream created in memory. No files written.")

        return self.mseed_stream
    
    def decimate_dfdas(self, factors=None):
        """
        Decimates self.dfdas based on the decimation factors provided in configuration.
        Updates self.dfdas and its metadata in-place.
        """
        if self.dfdas is None:
            print("Data not found in memory. Attempting to load before decimation...")
            return False
        
        # If factors are passed via process_chain, use them; 
        # otherwise, fall back to global_params
        if factors is None:
            fp = self.exec_params.get('freq_params', {})
            factors = fp.get("decimation_factor", [])
        
        for decimation in factors:
            print(f'Decimating at a factor of {decimation}')
            
            # 1. Capture current dimensions
            nt_in = self.dfdas.shape[0]
            
            # 2. Perform Resampling
            # resample_poly includes an anti-aliasing filter automatically
            sig_decimated = sps.resample_poly(
                self.dfdas, up=1, down=decimation, axis=0, padtype='edge'
            )
            
            # 3. Calculate new timing metadata
            nt_out = sig_decimated.shape[0]
            dt_out = self.dfdas.meta['dt'] * (nt_in / nt_out)
            tstart = self.dfdas.meta['time'] # + datetime.timedelta(seconds=0)
            
            # Use your helper to create the new index
            t = simpledas.create_time_axis(tstart, nt_out, dt_out)
            
            # 4. Update metadata and re-wrap as a DASDataFrame
            meta_out = self.dfdas.meta.copy()
            meta_out.update(dt=dt_out, time=tstart)
            
            # Overwrite the class attribute with the new decimated version
            self.dfdas = simpledas.DASDataFrame(
                sig_decimated, 
                index=t, 
                columns=self.dfdas.columns, 
                meta=meta_out
            )
            
            print(f"New sampling rate: {1/dt_out} Hz")
            # CRITICAL: Clear the cached ObsPy stream because the underlying 
            # data (sampling rate/length) has changed.
            self.mseed_stream = None 

        return self.dfdas

    def plot_spectrogram(self,freq_type="no_filter",suffix=""):
        ep = self.exec_params
        pp = self.path_params
        sfp = self.exec_params.get('spectrogram_freq_params', {})

        if self.mseed_stream is None:
            print("No ObsPy Stream found in memory. Attempting to create from self.dfdas...")
            self.dfdas_to_mseed(self.event, write=False, format=None, dType=float, decimate=False)

        trace = self.mseed_stream[0].copy()  # Work with a copy to avoid modifying the original

        if freq_type in sfp:
            fmin = sfp[freq_type]["fmin"]
            fmax = sfp[freq_type]["fmax"]
            if fmax == "nyquist":
                fmax=trace.stats.sampling_rate * 0.5
        else:
            fmin=0.01
            fmax=trace.stats.sampling_rate * 0.5

        if fmax>trace.stats.sampling_rate * 0.5:
            fmax=trace.stats.sampling_rate * 0.5

        fmax=40

        trace.filter('bandpass',freqmin=fmin,freqmax=fmax, corners=4, zerophase=True)    

        fig = plt.figure(figsize=(20, 10))
        ax1 = fig.add_axes([0.1, 1.1, 0.7, 0.2])  # [left, bottom, width, height]
        if freq_type != "whales":
            cmap='coolwarm'
            ax2 = fig.add_axes([0.1, 0.7, 0.7, 0.3]) #low freq
            ax3 = fig.add_axes([0.1, 0.1, 0.7, 0.6]) #high freq
        else:
            cmap='viridis'
            ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.8]) #low freq

        ax4 = fig.add_axes([0.83, 0.1, 0.03, 0.9])

        # Make time vector
        t = np.arange(trace.stats.npts) / trace.stats.sampling_rate
        t_hours = t / 3600

        # Plot waveform (top subfigure)
        ax1.plot(t, trace.data, 'k')
        ax1.set_xlim(t[0], t[-1])

        # Plot spectrogram - Low frequencies (bottom subfigure)
        spec_high_freq = ax2.specgram(trace.data, Fs=trace.stats.sampling_rate, cmap=cmap, NFFT=256, noverlap=128)
        plt.colorbar(spec_high_freq[3], cax=ax4)

        # Plot spectrogram - High frequencies (middle subfigure)
        if freq_type != "whales":
            #spec_low_freq = ax3.specgram(trace.data, Fs=trace.stats.sampling_rate, cmap=cmap, NFFT=1024, noverlap=512)
            ax3.imshow(spec_high_freq[3].get_array(), aspect='auto', extent=spec_high_freq[3].get_extent(), origin='lower', cmap=cmap)
            plt.colorbar(spec_high_freq[3], cax=ax4)

        # Set y-axis scale to logarithmic

        yticks = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
        #ax3.set_ylim(bottom=0.01)  # Set lower limit for logarithmic scale
        if freq_type != "whales":
            ax3.set_yscale('log')
            ax3.set_ylim(bottom=fmin)  # Set lower limit for logarithmic scale
            ax3.set_ylim(top=1)  # Set upper limit for logarithmic scale
            ax3.set_yticks(yticks)
            ax3.spines['top'].set_visible(False)
            ax3.set_yticklabels(yticks)
            ax3.set_xlabel(f'Time (s)')
        else:
            ax1.set_xlabel('Time (s)')

        ax2.set_xticks([])
        ax2.set_ylim(bottom=1)  # Set lower limit for linear scale
        ax2.set_ylim(top=fmax)  # Set lower limit for linear scale
        ax2.spines['bottom'].set_visible(False)
        # Set the x-axis of ax3 to hours
        ax1.set_xticks([])
        ax1.set_ylabel('Amplitude')
        ax2.set_ylabel(f'Frequency (Hz)')
        ax4.set_ylabel('Amplitude (dB)')

        if suffix:
            suffix = f"_{suffix}"
        filename=os.path.join(pp.get("figures_path"), f'{self.event}_fmin{fmin}_single_channel_spectrogram_dist-{trace.stats.distance}_{int((t[-1]+1)/3600)}h{suffix}')
        print("saving figure to ",filename)
        distance_km = trace.stats.distance / 1000
        fig.suptitle(f'Spectrogram for channel at {distance_km:.3f} km', y=1.0)
        fig.savefig(filename+'.pdf',dpi=600, format='pdf', bbox_inches='tight', pad_inches=0.1)
        fig.savefig(filename+'.png',dpi=300, format='png')
        plt.show()
        plt.close()  

        return

    def plot_envelope(self, params=None):
        """
        Calculates and saves the signal envelope plot.
        Supports overrides for cmap, vmin, and vmax via params.
        """
        if self.dfdas is None:
            print("No data in self.dfdas to plot.")
            return

        # 1. Setup local references and shorthand
        ep = self.exec_params
        pp = self.path_params
        ap = self.acquisition_params
        
        # Ensure params is a dict even if None/list was passed
        p = params if isinstance(params, dict) else {}

        # 2. Determine Plotting Parameters (Override logic)
        # It checks 'p' first, then 'ep', then provides a hard default
        cmap = p.get("envelope_cmap", ep.get("envelope_cmap", "viridis"))
        vmin = p.get("envelope_vmin", ep.get("envelope_vmin", .7))
        vmax = p.get("envelope_vmax", ep.get("envelope_vmax", 2))

        print(f"»»» Running envelope (Cmap: {cmap}, Vmin: {vmin}, Vmax: {vmax})")

        # 3. Check/Generate mseed_stream
        if getattr(self, 'mseed_stream', None) is None:
            self.dfdas_to_mseed(self.event, write=False, decimate=False)
        
        data = np.array([tr.data for tr in self.mseed_stream])

        # 4. Calculate Envelope Logic
        if ep.get("fkfilt") == True:
            en = abs(sps.hilbert(data.real, axis=1))
        else:
            en = abs(sps.hilbert(data, axis=1))
        
        nns = self.dfdas.meta["dimensionSizes"][0]
        mdn = np.tile(np.median(en, axis=1), (nns, 1)).T
        enmd = en / abs(mdn)
        
        # 5. Plotting
        fig = plt.figure(figsize=(4, 6))
        
        dist_min = (ap["dx"] * self.roi_step * self.min_channel[0]) / 1000
        dist_max = (ap["dx"] * self.roi_step * self.max_channel[0]) / 1000
        time_max = self.dfdas.meta["dt"] * nns

        plt.imshow(
            enmd.T, aspect='auto', origin='lower', norm="log",
            extent=[dist_min, dist_max, 0, time_max],
            cmap=cmap, vmin=vmin, vmax=vmax
        )
        
        plt.xlabel('Distance (km)')
        plt.ylabel('Time (s)')
        plt.title(f"Start time: {self.dfdas.meta['time']}")
        plt.tight_layout()

        # 6. Save logic
        save_path = os.path.join(pp.get("figures_path"), "Envelopes")
        if not os.path.exists(save_path): os.makedirs(save_path)
        
        filename = os.path.join(save_path, f"env_{self.event.replace(' ', '_')}")
        fig.savefig(f"{filename}.pdf", dpi=300, format='pdf', bbox_inches='tight')
        plt.close(fig)
        print(f"Envelope plot saved.")


    def check_data_access(self, experiment_path, datetime_start):
        """
        Verifies that the experiment path and the date-specific 
        subfolder exist before attempting to read files.
        """
        print(f"Checking data access in {experiment_path} for date {datetime_start.strftime('%Y-%m-%d')}")
        # 1. Check base path
        if not os.path.exists(experiment_path):
            print(f"ERROR: Base path does not exist: {experiment_path}")
            return False

        # 2. Check date-specific subfolder (SimpleDAS standard: path/YYYYMMDD)
        date_str = datetime_start.strftime('%Y%m%d')
        date_path = os.path.join(experiment_path, date_str)
        
        if not os.path.exists(date_path):
            print(f"ERROR: Date folder missing: {date_path}")
            print("Check if the drive is mounted or if the event date is correct.")
            return False

        # 3. Check for data type subfolder (e.g., 'dphi')
        dphi_path = os.path.join(date_path, 'dphi')
        if not os.path.exists(dphi_path):
             print(f"WARNING: 'dphi' folder not found in {date_path}. SimpleDAS might fail.")
             return False
        
        return True

def get_travel_times(event,global_params,rec_lat,rec_lon):
    exec_params = global_params['exec_params']
    sources = global_params['sources']
    
    #calculate theoretical arrival time
    source_latitude = sources.get(event, {}).get("latitude")
    source_longitude = sources.get(event, {}).get("longitude")
    source_depth = sources.get(event, {}).get("depth")
    i91 = TauPyModel(model="iasp91")
    arrivals_p = i91.get_travel_times_geo(source_depth_in_km=source_depth, receiver_latitude_in_deg=rec_lat,\
                                              receiver_longitude_in_deg=rec_lon, source_latitude_in_deg=source_latitude,\
                                              source_longitude_in_deg=source_longitude,phase_list=('ttp',), ray_param_tol=0.1)
    arrivals_s = i91.get_travel_times_geo(source_depth_in_km=source_depth, receiver_latitude_in_deg=rec_lat,\
                                              receiver_longitude_in_deg=rec_lon, source_latitude_in_deg=source_latitude,\
                                              source_longitude_in_deg=source_longitude,phase_list=('tts',), ray_param_tol=0.1)
    for arr in arrivals_p:
        arr.time=round(arr.time, 3)

    for arr in arrivals_s:
        arr.time=round(arr.time, 3)
        
    if exec_params.get("verbose"):
        print(arrivals_p,arrivals_s)

    return arrivals_p, arrivals_s

def get_coordinates(channel, global_params,roi_channel=False):
    """
    Get coordinates (latitude, longitude, elevation) based on the provided channel

    Parameters:
    - channel (int): The channel number for which coordinates are needed.
    - csv_path (str): The path to the CSV file.
    - csv_DAS (str): The name of the CSV file.

    Returns:
    Tuple (float, float, float): A tuple containing latitude, longitude, and elevation.
    """
    ep, pp = global_params['exec_params'], global_params['path_params']
    
    if ep.get("verbose", False) == 2:
        print(f"Getting coordinates for channel {channel} from {pp['csv_path']}{pp['csv_DAS']}")
        
    df = pd.read_csv(os.path.join(pp['csv_path'],pp['csv_DAS']))

    if roi_channel:
        filtered_df = df.loc[df['ROI_CHANNEL'] == channel]
    else:
        filtered_df = df.loc[df['CHANNEL'] == channel]
    
    if len(filtered_df) == 0:
        lat=32.64441
        lon=-16.94396
        ele=20
    else:
        lat=filtered_df['LATITUDE'].values[0]
        lon=filtered_df['LONGITUDE'].values[0]
        ele=round(filtered_df['ALTITUDE'].values[0],0)
    
    return lat,lon,ele


def encode_station_name(prefix,distance,global_params):
    ep=global_params.get("exec_params")   

    distance_m=int(distance)
    code_length = 5 - len(prefix)  # Calculate dynamic length
    factor=10 ** (5-code_length)
    converted_distance = distance_m // factor
    code = f"{prefix}{converted_distance:0{code_length}d}"

    if ep.get("verbose"):
        print(f'Encoded station: name: {code} - distance={distance} code_lenght={code_length} division_factor={factor}')
    return code


def station_xml_creation(st,global_params):
    ap, pp, ep  = global_params['acquisition_params'] , global_params['path_params'], global_params['exec_params']
    fp, th, sp = global_params['freq_params'], global_params['trace_header'], global_params['stationxml_params']
    
    
    #get filter params
    a,b=get_cheby2_coeffs(st[0].stats.sampling_rate*0.5,50)
    for tr in st:
        for coord in ["latitude","longitude","elevation"]:
            if coord not in tr.stats.coordinates:
                print(f'Station {tr.stats.station} has no {coord} field!\nStationXML file not created.')
                raise KeyError(f"Missing '{coord}' in tr.stats.coordinates")
                return

    response_stages=[]
    dummy_response_stage=[]
    
    response_stages=[PolesZerosResponseStage(stage_sequence_number=1,
                                             name="Gain",
                                             stage_gain=1,
                                             stage_gain_frequency=1.0,
                                             input_units="counts",
                                             output_units="counts",
                                             input_units_description=ap["sensitivityUnits"],
                                             output_units_description=ap["sensitivityUnits"],
                                             normalization_factor=1,
                                             normalization_frequency=0,
                                             pz_transfer_function_type="LAPLACE (RADIANS/SECOND)",
                                             zeros=[],
                                             poles=[])
                    ]

    for i in range(len(fp.get("decimation_factor"))):
    # Extract coefficients and parameters for the current stage
        decimation_factor = fp["decimation_factor"][i]
        input_sampling_rate = sp["input_sampling_rate"][i]
        a_coefficients = sp["filter_a_coefficients"][i].tolist()
        b_coefficients = sp["filter_b_coefficients"][i].tolist()

        # Create a CoefficientsTypeResponseStage object
        dummy_response_stage = CoefficientsTypeResponseStage(
            stage_sequence_number=i + 2,  # Stage sequence starts at 1
            name=f"Low-pass Chebishev filter stage + Decimation step {i + 1}. Decimation factor: {decimation_factor}",
            cf_transfer_function_type="DIGITAL",
            stage_gain_frequency=1.0,  # Frequency at which the gain is defined
            stage_gain=1,
            input_units="counts",
            output_units="counts",
            input_units_description=ap["sensitivityUnits"],
            output_units_description=ap["sensitivityUnits"],
            decimation_factor=decimation_factor,  # Set decimation factor
            decimation_input_sample_rate=input_sampling_rate,  # Input sample rate
            decimation_offset=0,
            decimation_delay=0,
            decimation_correction=0,
            denominator=a_coefficients,  # Denominator (a) coefficients
            numerator=b_coefficients,  # Numerator (b) coefficients
        )
        response_stages.append(dummy_response_stage)
    
    last_stage=len(response_stages)+1
    dummy_response_stage=CoefficientsTypeResponseStage(stage_sequence_number=last_stage,
                                  name="Sensitivity",
                                  cf_transfer_function_type="DIGITAL",
                                  numerator=[],
                                  denominator=[],
                                  decimation_factor=1,
                                  decimation_correction=0,
                                  decimation_delay=0,
                                  decimation_offset=0,
                                  decimation_input_sample_rate=ap.get("original_sample_rate")/math.prod(fp["decimation_factor"]),
                                  stage_gain=ap["sensitivity"],
                                  stage_gain_frequency=1.0,
                                  input_units="counts",
                                  output_units="counts",
                                  input_units_description=ap["sensitivityUnits"],
                                  output_units_description=ap["sensitivityUnits"],
                                  )

    response_stages.append(dummy_response_stage)

    response=Response(
    resource_id="OptoDAS header",
    instrument_sensitivity=InstrumentSensitivity(
        value=ap["sensitivity"],
        frequency=1.0,
        input_units="counts",
        output_units="counts",
        output_units_description="strain per meter",
        input_units_description=ap["sensitivityUnits"]+" phase difference expressed in radians per strain per meter",
        frequency_range_start=0.001,
        frequency_range_end=2000.0,
        frequency_range_db_variation=0,
        ),
        response_stages=response_stages)
    
    sensor=Equipment(
        type="DAS",
        description="OptoDAS",
        manufacturer="ASN",
        serial_number="44",
        installation_date=UTCDateTime(*th.get("net_starttime")),
        resource_id="OptoDAS_44"
        )
    data_logger=Equipment(
        type="DAS",
        description="OptoDAS",
        manufacturer="ASN",
        serial_number="44",
        installation_date=UTCDateTime(*th.get("net_starttime")),
        resource_id="OptoDAS_44"
        )
    pre_amplifier=Equipment(
        type="DAS",
        description="OptoDAS",
        manufacturer="ASN",
        serial_number="44",
        installation_date=UTCDateTime(*th.get("net_starttime")),
        resource_id="OptoDAS_44"
        )
    
    operator=[
        Operator(
            agency="ARDITI",
            contacts=[
                Person(
                    names=["Afonso Loureiro"],
                    agencies=["ARDITI, Funchal, Portugal",
                              "Instituto Dom Luiz, Lisboa, Portugal"],
                    emails=["maloureiro@fc.ul.pt"])],
                    website="www.arditi.pt"
                )
            ]

    inv=Inventory(
        networks=[],
        source=th.get("inventory_source"),
    )

    net=Network(
        code=st[0].stats.network,
        stations=[],
        description=th.get("net_description"),
        start_date=UTCDateTime(ap.get("start_date")),
        end_date=UTCDateTime(ap.get("end_date")),
        total_number_of_stations=th.get("net_no_stations"),
        selected_number_of_stations=len(st),
    )

    for tr in st:
        station_code=tr.stats.station
        if ep.get("encode_station_name"):
            das_channel = tr.stats['decoded_station']
        else:
            das_channel = tr.stats.station
    
        sta=Station(
                code=station_code,
                latitude=tr.stats.coordinates["latitude"],
                longitude=tr.stats.coordinates["longitude"],
                elevation=tr.stats.coordinates["elevation"],
                creation_date=UTCDateTime(*th.get("net_starttime")),
                start_date=UTCDateTime(ap.get("start_date")),
                end_date=UTCDateTime(ap.get("end_date")),
                site=Site(name=f'{th.get("sta_name_prefix")} {tr.stats.channel} channel no.{str(das_channel).zfill(5)}'),
                total_number_of_channels=1,
        )
        sta.operators=operator

        azimuth,dip=get_azimuth_dip(int(tr.stats.distance/ap.get("dx")+1),global_params,roi_channel=False)
        cha=Channel(code="HSF",
            location_code=th.get("location"),
            latitude=tr.stats.coordinates["latitude"],
            longitude=tr.stats.coordinates["longitude"],
            elevation=tr.stats.coordinates["elevation"],
            start_date=UTCDateTime(ap.get("start_date")),
            end_date=UTCDateTime(ap.get("end_date")),
            sample_rate=tr.stats.sampling_rate,
            depth=0,
            azimuth=azimuth,
            dip=dip
        )
        cha.response=response
        cha.equipments=[sensor,data_logger, pre_amplifier]
        cha.sensor=sensor
        cha.data_logger=data_logger
        cha.pre_amplifier=pre_amplifier
        sta.channels.append(cha)
        net.stations.append(sta)

    inv.networks.append(net)

    file=os.path.join(pp.get("MSEED_path"),f'RESP.{th.get("network")}.HSF.xml')
    inv.write(file, format="stationxml", validate=True)

    if ep.get("verbose"):
        print(f'StationXML file written to: {file}')

    if ep.get("verbose", False) == 2:
        print(inv)
        inv[0][-1][0].response.plot(min_freq=0.01,unwrap_phase=True)

    return

def degrade_coordinates(lat, lon, precision=3, error_metres=200):
    """
    Degrades precision and adds a random spatial displacement (error).
    """
    # 1. Calculate the degree offset for Latitude
    # 1 degree lat ≈ 111,111 meters
    lat_offset = error_metres / 111111.0
    
    # 2. Calculate the degree offset for Longitude
    # 1 degree lon ≈ 111,111 * cos(latitude) meters
    lon_offset = error_metres / (111111.0 * np.cos(np.radians(lat)))
    
    # 3. Apply a random shift within the error range
    # This creates a random displacement in any direction up to the error_meters
    random_lat_shift = np.random.uniform(-lat_offset, lat_offset)
    random_lon_shift = np.random.uniform(-lon_offset, lon_offset)
    
    # 4. Apply shift and then round for precision
    degraded_lat = round(lat + random_lat_shift, precision)
    degraded_lon = round(lon + random_lon_shift, precision)
    
    return degraded_lat, degraded_lon

def decimate_obspy(st,global_params):
    ep, fp, sp = global_params['exec_params'] , global_params['freq_params'], global_params['stationxml_params']

    for decimation in fp.get("decimation_factor"):
        print(f'Decimation factor: {decimation}')
        new_nyquist = st[0].stats.sampling_rate / 2.0 / decimation
        b,a=get_cheby2_coeffs(st[0].stats.sampling_rate * 0.5,new_nyquist)
        sp["input_sampling_rate"].append(st[0].stats.sampling_rate)
        sp["filter_a_coefficients"].append(a)
        sp["filter_b_coefficients"].append(b)
        for tr in st:
            zerophase_chebyshev_lowpass_filter(tr, new_nyquist)
        st.decimate(factor=decimation, no_filter=True)
        if ep.get("verbose"):
            print(st[0].stats.sampling_rate)
    return st

def get_cheby2_coeffs(nyquist, freqmax):
    """
    Calculates stable Chebyshev Type II coefficients for the current data.
    Ensures order <= 12 for numerical stability.
    """
    
    # rp - maximum ripple of passband, rs - attenuation of stopband
    rp, rs, order = 1, 96, 1e99
    # stop band frequency
    ws = freqmax / nyquist
    # pass band frequency
    wp = ws

    while True:
        if order <= 12:
            break
        wp *= 0.99
        order, wn = signal.cheb2ord(wp, ws, rp, rs, analog=0)

    b, a = signal.cheby2(order, rs, wn, btype="low", analog=0, output="ba")
    return b,a

def zerophase_chebyshev_lowpass_filter(trace, freqmax):
        """
        Custom Chebychev type two zerophase lowpass filter useful for
        decimation filtering.
        This filter is stable up to a reduction in frequency with a factor of
        10. If more reduction is desired, simply decimate in steps.
        Partly based on a filter in ObsPy.
        :param trace: The trace to be filtered.
        :param freqmax: The desired lowpass frequency.
        Will be replaced once ObsPy has a proper decimation filter.
        This code is from LASIF repository (Lion Krischer).
        """
        b, a = get_cheby2_coeffs(trace.stats.sampling_rate * 0.5, freqmax)

        # Apply twice to get rid of the phase distortion.
        trace.data = signal.filtfilt(b, a, trace.data)


def get_azimuth_dip(channel, global_params,roi_channel=False):
    """
    Get azimuth and dip based on the provided channel

    Parameters:
    - channel (int): The channel number for which coordinates are needed.
    - csv_path (str): The path to the CSV file.
    - csv_DAS (str): The name of the CSV file.

    Returns:
    Tuple (float, float): A tuple containing azimuth and dip.
    """
    ep, pp = global_params['exec_params'], global_params['path_params']

    if ep.get("verbose", False) == 2:
        print(f"Getting azimuth and dip for channel {channel} from {pp['csv_path']}{pp['csv_DAS']}")
        
    df = pd.read_csv(os.path.join(pp['csv_path'],pp['csv_DAS']))

    if roi_channel:
        filtered_df = df.loc[df['ROI_CHANNEL'] == channel]
    else:
        filtered_df = df.loc[df['CHANNEL'] == channel]
    
    if len(filtered_df) == 0:
        azi=0
        dip=0
    else:
        azi=filtered_df['AZIMUTH'].values[0]
        dip=filtered_df['DIP'].values[0]
    
    if azi<0:
        azi+=360

    return azi,dip

def get_data_from_S3(bucket_name, endpoint_url, starttime, endtime, local_path, unsigned=False):
    # Local Imports
    import boto3
    import os
    from botocore.config import Config
    from botocore import UNSIGNED

    # 1. Multi-day Guard: Warn and exit if start and end are on different days
    if starttime.date() != endtime.date():
        print(f"WARNING: starttime ({starttime.date()}) and endtime ({endtime.date()}) "
              "are on different days. This function only processes single-day requests.")
        return False

    # 2. Setup S3 Resource
    if unsigned:
        s3_res = boto3.resource('s3', endpoint_url=endpoint_url, config=Config(signature_version=UNSIGNED))
    else:
        s3_res = boto3.resource('s3', endpoint_url=endpoint_url)

    bucket = s3_res.Bucket(bucket_name)

    try:
        prefix = starttime.strftime('%Y%m%d/dphi/%H')
        dir_structure = starttime.strftime('%Y%m%d/dphi/')
        h5start = starttime.strftime('%Y%m%d/dphi/%H%M%S.h5')
        h5end = endtime.strftime('%Y%m%d/dphi/%H%M%S.h5')
        
        files_to_download = []
        last_seen_key = None
        
        # Check if we should skip the buffer file (Midnight check)
        is_midnight = (starttime.hour == 0 and starttime.minute == 0 and starttime.second == 0)

        for obj in bucket.objects.filter(Prefix=prefix):
            if obj.key > h5end:
                break
            
            if h5start <= obj.key <= h5end:
                # Add buffer file ONLY if not midnight AND it's the first file found
                if not files_to_download and last_seen_key and not is_midnight:
                    files_to_download.append(last_seen_key)
                
                files_to_download.append(obj.key)
            
            last_seen_key = obj.key

        # 3. Execution
        if not files_to_download:
            print("No files found for the specified time range.")
            return True

        target_dir = os.path.join(local_path, dir_structure)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for key in files_to_download:
            target = os.path.join(target_dir, os.path.basename(key))
            print(f"Downloading: {key} to {target}")
            bucket.download_file(key, target)

        print(f"Successfully downloaded {len(files_to_download)} files.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


