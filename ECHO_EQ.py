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
