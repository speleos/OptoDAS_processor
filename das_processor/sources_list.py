sources={         
"MSEED_20231028-30_A": # hourly mseed files from 2023-10-28 to 2023-10-30, decimated to 250 Hz and saved as individual channels and single file
	{"start_time":'2024-08-04 00:00:00.0', "magnitude": 2.3   , "latitude": 31.51 , "longitude": -16.21 , "depth": 0.0 ,
	"type":'seismic' , "window_in": 0 , "local": True , "GPS": True, "channel_ranges": 'mseed_A', 
    "DAS_data_path": '/mnt/data/S3-test' , "mseed_output_path": '/mnt/data/02_MSEED/hourly_mseed' ,
	"mode": 'time_lapse' ,
    "end_time":'2022-10-31 00:00:00.0',
	"window_duration": 3600,
    'process_chain':[
		{"operation":'decimate_dfdas', "params":{"factors": [2]}},
        {"operation":'dfdas_to_mseed', "params":{"write": 'stream'}},
        {"operation":'dfdas_to_mseed', "params":{"write": 'channels'}},
		]
    },
    
"Get-S3-data": # download data from 3X.2023 network
	{"start_time": "2023-10-28 00:00:00" ,
	"end_time": "2023-10-31 00:00:00" ,
    "mode": 's3_download' ,
    "DAS_data_path": '/mnt/data/S3-test/', 
    "s3_bucket": 'gc.3x2023', "endpoint_url": 'https://s3.gfz-potsdam.de/',"unsigned": True,} ,
}


channel_ranges={
    "mseed_A": {"channel_min": [200] ,
                "channel_max": [4000] ,
                "channel_step": [20]},
	
	"mseed_B": {"channel_min": [4020] ,
                "channel_max": [8000] ,
                "channel_step": [20]},
    
	"mseed_C": {"channel_min": [8020] ,
                "channel_max": [11293] ,
                "channel_step": [20]},
	
	"seismic": {"channel_min": [450] ,
                "channel_max": [11293] ,
                "channel_step": [1]},

    "seismic5": {"channel_min": [1000] ,
                "channel_max": [11283] ,
                "channel_step": [5]},
   
    "coastal": {"channel_min": [450] ,
                "channel_max": [2500] ,
                "channel_step": [1]},

    "land": {"channel_min": [0] ,
              "channel_max": [800] ,
              "channel_step": [1]},
    
    "spectrogram": {"channel_min": [200,1200,2200,3200,4200,5200,6200,7200,8200,9200,10200,11200] ,
                "channel_max":     [305,1205,2205,3205,4205,5205,6205,7205,8205,9205,10205,11205] ,
                "channel_step":    [10, 1,  ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1   ,1    ,1]},
    
    "whale_envelopes": {"channel_min": [1900] ,
                "channel_max": [8000] , 
                "channel_step": [1]},
}
