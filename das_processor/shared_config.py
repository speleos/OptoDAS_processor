path_params={
    "coords_path": './05_Coords/',
    "coords_DAS": 'coords.csv',
    "coords_DAS_lowres": 'ELLALink_public_coords.csv',
    
    "MSEED_path": './02_miniSEED/DAS/',
    "csv_out_path": './03_CSV/',

    "DAS_data_path": './01_RAW_DATA/',
    "experiment_path": './01_RAW_DATA/',

    "events_path": './02_Events/',
    
    "mseed_land_stations": './02_miniSEED/Stations/all-stations.mseed',
    "hdf5_headers_example": '/mnt/D2A/DAS/OptoDAS_SN44/26OCT-02NOV/20231027/dphi/125959.hdf5',
    "JSON_template": '/mnt/D2A/DAS/DAS-RCN_example.json',
    "figures_path": './04_Figures/'
}

freq_params={
    "clim_min": .6E19,
    "clim_max": 0.2E19,
    "filt_freq_min": 0,
    "filt_freq_max": 55,
    "decimation_factor": [8], #[5]
    "fk_vmax": 99999,
    "land_station_min_freq": 1.,
    "land_station_max_freq": 50.,
    "nfft_spectrum_vs_channel": 2048,
    "noverlap_spectrum_vs_channel": 1024,
    "window_type_spectrum_vs_channel": 'hann',  
}

acquisition_params={
    "roi_step": 5, #defaults for OptoDAS
    "gauge_length": 10,
    "dx": 1,
    "overlap": 0.5,
    "gps_status": 6, #default is 6=no GPS. 0=GPS locked.
    "sensitivity": 1,
    "sensitivityUnits": "rad/(strain*m)",
    "original_sample_rate": 500,
    "start_date": "2023,10,26,10,0,0",
    "end_date": "2023,11,03,12,00,0",
}

fk_params={
    "vmin": 1400,
    "vmax": 1600,
    "xint": 1,
    "xmin": 0,
    "tint": 1,
    "tmin": 0,
    "blur": 10,
    "wavdir": 'both',
}

stationxml_params={
    "input_sampling_rate": [],
    "filter_a_coefficients": [],
    "filter_b_coefficients": [],
}

first_channel_proc=0
last_channel_proc=11292 # 11380
channel_proc_step=1
bad_channels=range(11293,11380,1)


#RMS calculations
rms_params={
    "min_freq": 1.0 / 10.0,
    "max_freq": 50.0,
    "low_pass_max_freq": 5.0,
    "max_freq_array_response": 10.0,
    "min_freq_array_response": .1,
    "freq_step_array_response": 0.05,
    "num_points": 110,
    "num_windows": 3,
    "window_duration": 1200,
    "bandwidth_ratio": 0.1,
    "TeCVA_RMS_window": 50,
    "beamforming_window": 30,
    "beamforming_arrival_window": 5,
    "beamforming_filter": [ 1/10, 5 ],
    "normalisation_strategy": "std", # "std" or "rms"
    "array_response_min_freq": 1/60,
    "array_response_max_freq": 50,
}

spec_freq_params={
            "full":{"fmin": 0.01,
                    "fmax": "nyquist",
                   },
            "highpass_20sec":{"fmin": 0.05,
                    "fmax": "nyquist",
                   },
            "whales":{"fmin": 1,
                    "fmax": 40,
                   },
            }

station_coordinates = {
    "PMAR": {"latitude": 32.72, "longitude": -16.91, "channels": "HH*"},
    "PMPST": {"latitude": 33.08, "longitude": -16.33, "channels": "HH*"},
    "PMPS": {"latitude": 33.06, "longitude": -16.33, "channels": "HN*"},
    "PMOZ": {"latitude": 32.82, "longitude": -17.20, "channels": "HN*"},
    "FUL": {"latitude": 32.65, "longitude": -16.89, "channels": "SH*"},
    "FIMU":{"latitude": 32.29856, "longitude": -16.62694},
}

trace_header={
        "network": '3X',
        "location": '',
        "mseed":'D',
        "channel":'HSF',
        "net_description": "GeoLAB DAS cable. 57 km-long dark fibre starting at the Praia Formosa CLS, managed by ARDITI.",
        "net_starttime": [2023,10,26],
        "net_no_stations": 11293, # load this value later
        "sta_name_prefix": "GeoLAB fibre. DAS",
        "inventory_source": "maloureiro@fc.ul.pt",
        "station_prefix": "G", #"GLB", # the number of letters in the station name prefix will change the precision of the number code.
}

clock_offset=150

propagation_velocity=5000

first_bad_channel=11293
