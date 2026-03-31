sources={ "version": 2.0 ,
         
"GEOFON_MSEED_20240804-08_A":
	{"start_time":'2024-08-03 08:30:00.0', "magnitude": 2.3   , "latitude": 31.51 , "longitude": -16.21 , "depth": 0.0 ,
	"type":'seismic' , "window_in": 0 , "window_out": 3600 , "local": True , "GPS": True, "channel_ranges": 'mseed_IRIS_1', 
    "DAS_data_path": '/mnt/DOMLUIZ/DATA_dphi' , "mseed_output_path": '/mnt/DOMLUIZ/02_MSEED/daily_mseed' ,
	"mode": 'time_lapse' ,
    "end_time":'2024-08-16 00:00:00.0',
	"window_duration": 86400,
    'process_chain':[
		{"operation":'decimate_dfdas', "params":{"factors": [2]}},
        {"operation":'dfdas_to_mseed', "params":{"write": 'channels'}},
		]
    },
    
"Get-S3-data":
	{"start_time": "2023-10-29 19:09:25" ,
	"end_time": "2023-10-29 19:09:45" ,
    "mode": 's3_download' ,
    "DAS_data_path": '/tmp/S3-test/', 
    "s3_bucket": 'gc.3x2023', "endpoint_url": 'https://s3.gfz-potsdam.de/',"unsigned": True,} ,

"TEST-MSEED":
	{"start_time": "2023-10-29 19:09:25" ,
	"end_time": "2023-10-29 19:09:45" ,
    "window_in": 0 , "window_out": 0 , "local": True , "GPS": True, "channel_ranges": 'mseed_IRIS_1',
    "mode": 'seismic' ,
    "DAS_data_path": '/tmp/S3-test/', "mseed_output_path": '/tmp/S3-test/',
    'process_chain':[
        {"operation":'dfdas_to_mseed', "params":{"write": 'channels'}},
        {"operation":'dfdas_to_mseed', "params":{"write": 'stream'}},
		]
    } ,
}

channel_ranges={
    "seismic": {"channel_min": [450] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [1]},#10

    "seismic5": {"channel_min": [1000] ,
                "channel_max": [11283] ,    #[11293] ,
                "channel_step": [5]},


    "seismic_spectrum": {"channel_min": [450] ,
                        "channel_max": [4000] ,    #[11293] ,
                        "channel_step": [1]},#10
    
    "coherence": {"channel_min": [450,650,850,1050,1250,1450,1650,1850,2050,2250,2450,2650,2850,3050,3250,3450,3650,3850,4050,4250,4450,
                                  4650,4850,5050,5250,5450,5650,5850,6050,6250,6450,6650,6850,7050,7250,7450,7650,7850,8050,8250,8450,
                                  8650,8850,9050,9250,9450,9650,9850,10050,10250,10450,10650,10850,11050],
                  "channel_max": [650,850,1050,1250,1450,1650,1850,2050,2250,2450,2650,2850,3050,3250,3450,3650,3850,4050,4250,4450,4650,
                                  4850,5050,5250,5450,5650,5850,6050,6250,6450,6650,6850,7050,7250,7450,7650,7850,8050,8250,8450,8650,
                                  8850,9050,9250,9450,9650,9850,10050,10250,10450,10650,10850,11050,11250],
                  "channel_step": [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
                                   2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]},
    "coastal": {"channel_min": [450] ,
                "channel_max": [2500] ,
                "channel_step": [1]},

    "land": {"channel_min": [0] ,
              "channel_max": [800] ,
              "channel_step": [1]},
    
    "spectrogram": {"channel_min": [200,1200,2200,3200,4200,5200,6200,7200,8200,9200,10200,11200] ,
                "channel_max":     [305,1205,2205,3205,4205,5205,6205,7205,8205,9205,10205,11205] ,    #[11293] ,
                "channel_step":    [10,  1,   1,1,1,1,1,1,1,1,1,1]},#10

    "spectrogram_currents": {"channel_min": [3000] ,
                "channel_max": [3005] ,    #[11293] ,
                "channel_step": [1]},#10

    "blue_whale": {"channel_min": [3400] ,
                "channel_max": [3600] ,    #[11293] ,
                "channel_step": [20]},#10
    
    "whale_envelopes_R1": {"channel_min": [2000] ,
                "channel_max": [4000] ,    #[11293] ,
                "channel_step": [1]},#10
}
