time_lapses={
    "snr_calculation_300":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-11-30 13:30:00.0', "end_time":'2024-11-30 13:45:00.0',
                          "magnitude": '0', "window_duration": 300, "local": True, "type": 'snr_calculation'},
    
    "snr_calculation_1800_b":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-12-04 00:00:00.0', "end_time":'2024-12-05 00:00:00.0',
                          "magnitude": '0', "window_duration": 1800, "local": True, "type": 'snr_calculation', 'process_chain':['snr_calculation']},

    "mseed_generation_iris0":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-26 10:00:00.0', "end_time":'2023-10-26 10:05:00.0',
                          "magnitude": '0', "window_duration": 300, "local": True, "type": 'mseed_IRIS'},
    
    "envelopes_R1":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-29 04:52:29.0', "end_time":'2023-10-29 04:55:29.0',
                          "magnitude": '0', "window_duration": 30, "local": True, "type": 'whale_envelopes_R1', 'process_chain':['plot_envelopes']},

    "envelopes1":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-12-02 22:45:00.0', "end_time":'2024-12-06 00:00:00.0',
                          "magnitude": '0', "window_duration": 300, "local": True, "type": 'whale_envelopes', 'process_chain':['plot_envelopes']},
    
    "envelopes2":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-12-03 00:00:00.0', "end_time":'2024-12-03 06:00:00.0',
                          "magnitude": '0', "window_duration": 300, "local": True, "type": 'whale_envelopes', 'process_chain':['plot_envelopes']},
    
    "envelopes3":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-12-03 06:00:00.0', "end_time":'2024-12-03 12:00:00.0',
                          "magnitude": '0', "window_duration": 300, "local": True, "type": 'whale_envelopes', 'process_chain':['plot_envelopes']},
    
    "mseed_generation":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2024-11-30 13:30:00.0', "end_time":'2024-12-01 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*10.5, "local": True, "type": 'mseed_IRIS', 'process_chain':['mseed_time_lapse']},

    "mseed_generation_a":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-26 10:00:00.0', "end_time":'2023-10-27 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*14, "local": True, "type": 'mseed_EIDA', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_b":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-27 00:00:00.0', "end_time":'2023-11-03 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*24, "local": True, "type": 'mseed_EIDA', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_c":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-03 00:00:00.0', "end_time":'2023-11-03 12:00:00.0',
                          "magnitude": '0', "window_duration": 3600*12, "local": True, "type": 'mseed_EIDA', 'process_chain':['mseed_time_lapse']},
    
    "mseed_generation_iris1_1":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-26 10:00:00.0', "end_time":'2023-10-27 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*14, "local": True, "type": 'mseed_IRIS_1', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris1_2":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-26 10:00:00.0', "end_time":'2023-10-27 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*14, "local": True, "type": 'mseed_IRIS_2', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris1_3":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-26 10:00:00.0', "end_time":'2023-10-27 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*14, "local": True, "type": 'mseed_IRIS_3', 'process_chain':['mseed_time_lapse']},
    
    "mseed_generation_iris2_1":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-01 00:00:00.0', "end_time":'2023-11-03 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*24, "local": True, "type": 'mseed_IRIS_1', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris2_2":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-10-28 00:00:00.0', "end_time":'2023-10-29 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*24, "local": True, "type": 'mseed_IRIS_2', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris2_3":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-01 00:00:00.0', "end_time":'2023-11-03 00:00:00.0',
                          "magnitude": '0', "window_duration": 3600*24, "local": True, "type": 'mseed_IRIS_3', 'process_chain':['mseed_time_lapse']},

    "mseed_generation_iris3_1":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-03 00:00:00.0', "end_time":'2023-11-03 12:00:00.0',
                          "magnitude": '0', "window_duration": 3600*12, "local": True, "type": 'mseed_IRIS_1', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris3_2":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-03 00:00:00.0', "end_time":'2023-11-03 12:00:00.0',
                          "magnitude": '0', "window_duration": 3600*12, "local": True, "type": 'mseed_IRIS_2', 'process_chain':['mseed_time_lapse']},
    "mseed_generation_iris3_3":{"latitude": 32.47, "longitude": -16.43, "depth": 0, "start_time":'2023-11-03 00:00:00.0', "end_time":'2023-11-03 12:00:00.0',
                          "magnitude": '0', "window_duration": 3600*12, "local": True, "type": 'mseed_IRIS_3', 'process_chain':['mseed_time_lapse']},
}

sources={   "04DEC2024_0830":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 08:30:00',
                   "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_0835":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 08:35:00',
                     "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_0840":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 08:40:00',
                     "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_0845":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 08:45:00',
                     "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_0850":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 08:50:00',
                     "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},
            
            "04DEC2024_1830":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 18:30:00',
                        "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},
            
            "04DEC2024_1835":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 18:35:00',
                        "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},
            
            "04DEC2024_1840":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 18:40:00',
                        "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_1845":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 18:45:00',
                        "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},

            "04DEC2024_1850":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2024-12-04 18:50:00',
                        "magnitude": '0', "window_in": 0, "window_out": 300, "local": True, "type": 'whale_envelopes'},


    "31OCT23_1233_Chile7200": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                "window_in": 3600, "window_out": 3600, "local": False, "magnitude": 6.7, "type": 'broadband_test_zoom'},
    "31OCT23_1233_Chile7200B": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                "window_in": 1600, "window_out": 4600, "local": False, "magnitude": 6.7, "type": 'seismic_broadband_test'},

    "31OCT23_1233_Chile7200C": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                "window_in": 1600, "window_out": 4600, "local": False, "magnitude": 6.7, "type": 'seismic_broadband_test'},

    "31OCT23_1233_Chile7200D": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                "window_in": 2600, "window_out": 3600, "local": False, "magnitude": 6.7, "type": 'seismic_broadband_test'},


    "whales_2025MAR17_a":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-03-17 13:00:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 900, "local": True, "type": 'blue_whale'},
    "whales_2025MAR17_b":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-03-17 13:15:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 900, "local": True, "type": 'blue_whale'},
    "whales_2025MAR17_c":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-03-17 13:30:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 900, "local": True, "type": 'blue_whale'},
    "whales_2025MAR17_d":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-03-17 13:55:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 900, "local": True, "type": 'blue_whale'},

    "nsd_2023OCT27":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-10-27 15:20:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 3600, "local": True, "type": 'nsd'},

    "blue_whale2":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-10-29 04:50:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 900, "local": True, "type": 'blue_whale'},

    "ship_scrub":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-11-02 17:00:00.0',
                          "magnitude": '0', "window_in": 0, "window_out": 3600*6, "local": True, "type": 'ship_scrub'},

    "madalia_world":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-10-29 17:00:00.0',
                          "magnitude": '0', "window_in": 0, "window_out": 600, "local": True, "type": 'madalia_world'},

    "spectrum_20251031":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-10-31 01:53:00.0',
                          "magnitude": '0', "window_in": 0, "window_out": 180, "local": True, "type": 'seismic_spectrum', 'GPS': True},
    "spectrum_20251031b":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-10-31 01:56:00.0',
                          "magnitude": '0', "window_in": 0, "window_out": 180, "local": True, "type": 'seismic_spectrum', 'GPS': True},
    "spectrum_20251031c":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2025-10-31 01:59:00.0',
                          "magnitude": '0', "window_in": 0, "window_out": 180, "local": True, "type": 'seedlink', 'GPS': True},

    "03NOV23":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-11-03 00:00:00.0',
                          "magnitude": '2.7', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},
    
    "27OCT23_solution_a":{"latitude": 32.47, "longitude": -16.43, "depth": 20, "time":'2023-10-27 14:21:02.0',
                          "magnitude": '2.7', "window_in": 60, "window_out": 300, "local": True, "type": 'seismic'},
    
    "27OCT23_solution_b":{"latitude": 32.447 , "longitude": -16.3940, "depth": 4.3, "time":'2023-10-27 14:21:01.50',
                          "magnitude": '2.7', "window_in": 60, "window_out": 300, "local": True, "type": 'seismic'},

    "27OCT23_solution_c":{"latitude": 32.447 , "longitude": -16.3940, "depth": 4.3, "time":'2023-10-27 14:21:01.50',
                          "magnitude": '2.7', "window_in": 60, "window_out": 300, "local": True, "type": 'seismic'},



    "20250924T221910":{"latitude": 32.61 , "longitude": -16.28, "depth": 10.0, "time":'2025-09-24 22:19:10', 'GPS': True,
                          "magnitude": '4.0', "window_in": 30, "window_out": 300, "local": True, "type": 'seismic',
                          'process_chain':['save_DFDAS','plot_section']},
    "20250924T221910a":{"latitude": 32.61 , "longitude": -16.28, "depth": 10.0, "time":'2025-09-24 22:19:10', 'GPS': True,
                          "magnitude": '4.0', "window_in": 10, "window_out": 200, "local": True, "type": 'seismic',
                          'process_chain':['save_DFDAS','plot_section']},
    "20250924T221910b":{"latitude": 32.61 , "longitude": -16.28, "depth": 10.0, "time":'2025-09-24 22:19:10', 'GPS': True,
                          "magnitude": '4.0', "window_in": 60, "window_out": 600, "local": True, "type": 'seismic',
                          'process_chain':['save_DFDAS','plot_section']},
    "20250924T221912a":{"latitude": 32.69 , "longitude": -16.33, "depth": 10.0, "time":'2025-09-24 22:19:12', 'GPS': True,
                          "magnitude": '4.0', "window_in": 60, "window_out": 60, "local": True, "type": 'seismic',
                          'process_chain':['save_DFDAS','low_pass','plot_section']},
    "20250924T221915a":{"latitude": 32.52 , "longitude": -16.40, "depth": 16.0, "time":'2025-09-24 22:19:15', 'GPS': True,
                          "magnitude": '4.0', "window_in": 5, "window_out": 40, "local": True, "type": 'seismic',
                          'process_chain':['save_DFDAS','low_pass','plot_section']},



    "27OCT23_SUSANA":{"latitude": 32.49 , "longitude": -16.240, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
                          "magnitude": '2.7', "window_in": 60, "window_out": 300, "local": True, "type": 'seismic'},
    
    "27OCT23_derrick":{"latitude": 32.49 , "longitude": -16.240, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
                          "magnitude": '2.7', "window_in": 0, "window_out": 10, "local": True, "type": 'seismic_zoom'},

    "27OCT23_paper":{"latitude": 32.49 , "longitude": -16.240, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
                          "magnitude": '2.7', "window_in": 5, "window_out": 55, "local": True, "type": 'seismic_zoom'},

    "27OCT23_ZOOM":{"latitude": 32.49 , "longitude": -16.240, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
                          "magnitude": '2.7', "window_in": 5, "window_out": 45, "local": True, "type": 'seismic'},

    "DN27OCT23":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
                 "magnitude": '2.7', "window_in": 60, "window_out": 300, "local": True, "type": 'seismic'},
    
    "29OCT23":{"latitude": 34.35 , "longitude": -16.43, "depth": 10, "time":'2023-10-29 00:25:34.0',
               "magnitude": '2.4', "window_in": 20, "window_out": 70, "local": True, "type": 'seismic'},
    
    "26OCT23_1605_Komandorskiye_Ostrova_Region": {"latitude": 56.05, "longitude": 164.75, "depth": 2.0, "time": '2023-10-26T16:05:11',
                                                  "window_in": 120, "window_out": 1800, "local": False,"magnitude": 5.9, "type": 'seismic'},
    
    "26OCT23_1900_Democratic_Republic_of_Congo": {"latitude": -7.3, "longitude": 27.93, "depth": 15.0, "time": '2023-10-26T19:00:26',
                                                  "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.4, "type": 'seismic'},
    
    "27OCT23_0302_Tonga_Islands": {"latitude": -17.58, "longitude": -173.77, "depth": 35.0, "time": '2023-10-27T03:02:24',
                                   "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.6, "type": 'seismic'},
    
    "28OCT23_0433_Fiji_Islands_Region": {"latitude": -20.120, "longitude": -176.39, "depth": 215.0, "time": '2023-10-28T04:33:30',
                                         "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.5, "type": 'seismic'},
    
    "28OCT23_0531_Solomon_Islands": {"latitude": -10.22, "longitude": 161.30, "depth": 69.0, "time": '2023-10-28T05:31:58',
                                     "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.5, "type": 'seismic'},
    
    "28OCT23_0955_Vanuatu_Islands": {"latitude": -13.11, "longitude": 167.06, "depth": 201.0, "time": '2023-10-28T09:55:28',
                                     "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.6, "type": 'seismic'},
    
    "29OCT23_0432_Vanuatu_Islands": {"latitude": -19.42, "longitude": 168.76, "depth": 80.0, "time": '2023-10-29T04:32:08',
                                     "window_in": 120, "window_out": 1800, "local": False, "magnitude": 6.0, "type": 'seismic'},
    
    "29OCT23_1357_Northern_Mid-Atlantic_Ridge": {"latitude": 43.94, "longitude": -28.38, "depth": 10.0, "time": '2023-10-29T13:57:41',
                                                 "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.1, "type": 'seismic'},
    
    "30OCT23_1557_Jamaica_Region": {"latitude": 18.08, "longitude": -76.58, "depth": 10.0, "time": '2023-10-30T15:57:21',
                                    "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.4, "type": 'seismic'},
    
    "31OCT23_0546_Fiji": {"latitude": -2.95, "longitude": 141.89, "depth": 29.0, "time": '2023-10-31T05:46:46',
                                                  "window_in": 600, "window_out": 3600, "local": False,"magnitude": 4.9, "type": 'seismic5'},
  
    "31OCT23_0608_South_of_Java": {"latitude": -10.23, "longitude": 108.30, "depth": 10.0, "time": '2023-10-31T06:08:17',
                                                  "window_in": 300, "window_out": 1800, "local": False,"magnitude": 4.4, "type": 'seismic'},
    
    "31OCT23_0658_New_Britain_PNG": {"latitude": -5.71, "longitude": 148.73, "depth": 145.7, "time": '2023-10-31T06:58:32',
                                                  "window_in": 300, "window_out": 1800, "local": False,"magnitude": 4.1, "type": 'seismic'},
    
    "31OCT23_0720_Chiapas": {"latitude": 17.1, "longitude": -92.62, "depth": 210.1, "time": '2023-10-31T06:58:32',
                                                  "window_in": 300, "window_out": 1800, "local": False,"magnitude": 4.0, "type": 'seismic'},
  
    "31OCT23_1110_Fiji_Islands_Region": {"latitude": -17.62, "longitude": -179.03, "depth": 552.0, "time": '2023-10-31T11:10:56',
                                         "window_in": 120, "window_out": 1800, "local": False, "magnitude": 6.5, "type": 'seismic'},
    
    "31OCT23_1233_Near_Coast_of_Central_Chile": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                                 "window_in": 120, "window_out": 2400, "local": False, "magnitude": 6.7, "type": 'seismic'},

    "31OCT23_1233_Chile": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                                                 "window_in": 300, "window_out": 3300, "local": False, "magnitude": 6.7, "type": 'seismic'},

    "01NOV23_0515_Canaries": {"latitude": 29.38, "longitude": -17.86, "depth": 0.0, "time": '2023-11-01T05:15:45',
                              "window_in": 30, "window_out": 180, "local": True, "magnitude": 2, "type": 'seismic'},
    
    "01NOV23_1015_Fiji_Islands_Region": {"latitude": -15.52, "longitude": -177.52, "depth": 410.0, "time": '2023-11-01T10:15:43',
                                         "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.1, "type": 'seismic'},
    
    "01NOV23_1251_Andaman_Islands_India_Region": {"latitude": 10.93, "longitude": 93.06, "depth": 94.0, "time": '2023-11-01T12:51:15',
                                                  "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.1, "type": 'seismic'},
    
    "01NOV23_2104_Timor_Region": {"latitude": -10.06, "longitude": 123.75, "depth": 51.0, "time": '2023-11-01T21:04:48',
                                  "window_in": 120, "window_out": 1800, "local": False, "magnitude": 6.1, "type": 'seismic'},
    
    "02NOV23_0709_Northern_Mid-Atlantic_Ridge": {"latitude": 10.26, "longitude": -40.94, "depth": 10.0, "time": '2023-11-02T07:09:41',
                                                 "window_in": 120, "window_out": 1800, "local": False, "magnitude": 5.1, "type": 'seismic'},
    
    "28JUN2024_0536_Near_Coast_Peru": {"latitude": -15.81, "longitude": -74.44, "depth": 24.0, "time": '2024-06-28T05:36:37',
                                            "window_in": 120, "window_out": 1800, "local": False, "magnitude": 7.2, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "29JUN2024_0705_Near_Coast_Peru": {"latitude": -16.05, "longitude": -74.56, "depth": 18.0, "time": '2024-06-29T07:05:33',
                                            "window_in": 120, "window_out": 1800, "local": False, "magnitude": 6.1, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "23JUN24_0357_Near_Coast_Venezuela": {"latitude": 10.58 , "longitude": -62.51, "depth": 10.0, "time": '2024-06-23T03:57:52', "magnitude": 6.0,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},

    "24JUN24_0803_Vanuatu":                { "latitude": -14.61,  "longitude": 167.25 , "depth": 157.0, "time": '2024-06-24T08:03:38',   "magnitude": 6.3,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "07JUL24_2001_Bonin_Islands":          { "latitude": 26.89 ,  "longitude": 138.83 , "depth": 571.0, "time": '2024-07-07T20:01:14',   "magnitude": 6.2,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "10JUL24_0455_South_of_Africa":        { "latitude": -53.30,  "longitude": 25.36  , "depth": 4.0  , "time": '2024-07-10T04:55:42',   "magnitude": 6.6,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "11JUL24_0213_Mindanao":               { "latitude": 6.09  ,  "longitude": 123.16 , "depth": 628.0, "time": '2024-07-11T02:13:18',   "magnitude": 7.1,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "11JUL24_1508_Vancouver_Island":       { "latitude": 48.81 ,  "longitude": -128.72,  "depth": 10.0, "time": '2024-07-11T15:08:48',   "magnitude": 6.4,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "19JUL24_0150_Chile-Argentina_Border": { "latitude": -23.12,  "longitude": -67.87 , "depth": 126.0, "time": '2024-07-19T01:50:46',   "magnitude": 7.3,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},
    
    "19JUL24_0313_Aleutian_Islands":       { "latitude": 52.13 ,  "longitude": -170.93,  "depth": 42.0, "time": '2024-07-19T03:13:48',   "magnitude": 6.0,
                                           "window_in": 120, "window_out": 1800, "local": False, "type": 'seismic',
                                           "MSEED_file": 'JUN-JUL2024_Package_1725357421353.mseed', "GPS": True},

    "currents_26":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-26 14:00:00',
                   "magnitude": '0', "window_in": 0, "window_out": 3600*2.5, "local": True, "type": 'spectrogram_currents'},
    
    "spectro26":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-26 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*12, "local": True, "type": 'spectrogram'},
    
    "blue_whale":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-29 01:50:00',
                   "magnitude": '0', "window_in": 0, "window_out": 3600*6, "local": True, "type": 'blue_whale'},

    "whales27_zoom":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-27 14:30:00',
                   "magnitude": '0', "window_in": 0, "window_out": 3600, "local": True, "type": 'whales_zoom'},
    
    "whales27_30":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-27 14:15:00',
                   "magnitude": '0', "window_in": 0, "window_out": 3600, "local": True, "type": 'whales_zoom'},
    
    "spectro27":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-27 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},
    
    "spectro28":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-28 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},

    "spectro29":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-29 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},

    "spectro30":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-30 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},

    "spectro31":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-10-31 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},
    
    "spectro01":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-11-01 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},

    "spectro02":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-11-02 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*24, "local": True, "type": 'spectrogram'},
    
    "spectro03":{"latitude": 32.4339 , "longitude": -16.274, "depth": 4.0, "time":'2023-11-03 00:00:00',
                 "magnitude": '0', "window_in": 0, "window_out": 3600*10, "local": True, "type": 'spectrogram'},
    
    "broadband": {"latitude": -28.75, "longitude": -71.57, "depth": 41.0, "time": '2023-10-31T12:33:44',
                        "window_in": 120, "window_out": 3600, "local": False, "magnitude": 6.7, "type": 'seismic'},

    "waves":{"latitude": 32.72 , "longitude": -16.91, "depth": 0, "time":'2023-10-27 13:02:30.0',
             "window_in": 0, "window_out": 8400, "local": True, "type": 'coastal'},
    
    "LAND":{"latitude": 32.49 , "longitude": -16.240, "depth": 4.0, "time":'2023-10-27 14:20:59.73',
            "magnitude": '2.9', "window_in": 0, "window_out": 3600, "local": True, "type": 'land'},
}

channel_ranges={
    "broadband_test_zoom": {"channel_min": [7000] ,
                "channel_max": [8500] ,    #[11293] ,
                "channel_step": [1]},#10

    "seismic_broadband_test": {"channel_min": [5000] ,
                "channel_max": [8500] ,    #[11293] ,
                "channel_step": [1]},#10

    "seismic": {"channel_min": [450] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [1]},#10

    "seismic5": {"channel_min": [1000] ,
                "channel_max": [11283] ,    #[11293] ,
                "channel_step": [5]},


    "seismic_spectrum": {"channel_min": [450] ,
                        "channel_max": [4000] ,    #[11293] ,
                        "channel_step": [1]},#10
    
    "lowpass": {"channel_min": [3000] ,
                "channel_max": [10000] ,    #[11293] ,
                "channel_step": [100]},#10
    
    "internal_tides": {"channel_min": [500] ,
                "channel_max": [11000] ,    #[11293] ,
                "channel_step": [100]},#10
    
    "seismic_zoom": {"channel_min": [6500] ,
                "channel_max": [7000] ,
                "channel_step": [10]},

    "seedlink": {"channel_min": [392] ,
                "channel_max": [11283] ,
                "channel_step": [392]},

    "matthew_internal_waves": {"channel_min": [1125] ,
                "channel_max": [3083] ,
                "channel_step": [1]},

    "MUSIC": {"channel_min": [2000,3000,4000] ,
              "channel_max": [2100,3100,4100] ,
              "channel_step": [10,10,5]},
    "seismic_BEAM": {"channel_min": [4000] ,
             "channel_max": [4500] ,
             "channel_step": [100]},
    "nsd": {"channel_min": [0],
             "channel_max": [450],
             "channel_step": [1]},
    "seismic_BEAM_multiple": {"channel_min": [5250,1000,2000,3000,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,5640],
                      "channel_max": [5750,1500,2500,3500,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11200,5680],
                      "channel_step": [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,1]},
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
    "madalia_world": {"channel_min": [300] ,
                "channel_max": [2500] ,
                "channel_step": [1]},
    "land": {"channel_min": [0] ,
              "channel_max": [800] ,
              "channel_step": [1]},
    "tecva": {"channel_min": [500] ,
              "channel_max": [11293] ,
              "channel_step": [500]},
    "spectrogram": {"channel_min": [200,1200,2200,3200,4200,5200,6200,7200,8200,9200,10200,11200] ,
                "channel_max":     [305,1205,2205,3205,4205,5205,6205,7205,8205,9205,10205,11205] ,    #[11293] ,
                "channel_step":    [10,  1,   1,1,1,1,1,1,1,1,1,1]},#10
    "spectrogram_currents": {"channel_min": [3000] ,
                "channel_max": [3005] ,    #[11293] ,
                "channel_step": [1]},#10
    "whales": {"channel_min": [8204] ,
                "channel_max": [8204] ,    #[11293] ,
                "channel_step": [1]},#10
    "blue_whale": {"channel_min": [3400] ,
                "channel_max": [3600] ,    #[11293] ,
                "channel_step": [20]},#10
    "ship_scrub": {"channel_min": [700] ,
                "channel_max": [1000] ,    #[11293] ,
                "channel_step": [5]},#10
    "whale_envelopes": {"channel_min": [2000] ,
                "channel_max": [8000] ,    #[11293] ,
                "channel_step": [1]},#10
    "whale_envelopes_R1": {"channel_min": [2000] ,
                "channel_max": [4000] ,    #[11293] ,
                "channel_step": [1]},#10
    "whales_zoom": {"channel_min": [8190] ,
                "channel_max": [8215] ,    #[11293] ,
                "channel_step": [1]},#10
    "snr_calculation": {"channel_min": [700] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [1]},#10
    "mseed_EIDA": {"channel_min": [200] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [800]},#10
    "mseed_IRIS": {"channel_min": [200] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [20]},#10
    "mseed_IRIS_1": {"channel_min": [200] ,
                "channel_max": [4000] ,    #[11293] ,
                "channel_step": [20]},#10
    "mseed_IRIS_2": {"channel_min": [4020] ,
                "channel_max": [8000] ,    #[11293] ,
                "channel_step": [20]},#10
    "mseed_IRIS_3": {"channel_min": [8020] ,
                "channel_max": [11293] ,    #[11293] ,
                "channel_step": [20]},#10
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

path_params={
    "csv_path": '/mnt/D2A/DAS/ELLALink/',
    "csv_out_path": '/mnt/SUBMERSE/ECHO/CSV/',
    "csv_SNR_path": '/mnt/D2A/DAS/SNR/',
    "csv_DAS": 'roi_chan_lat_long_depth_dist_azim_dip_5m_17OCT2024.csv',
    #"csv_DAS": 'roi-chan_chan_lat_long_depth_5m.csv',
    "csv_DAS_lowres": 'ELLALink_public_coords.csv',
    "csv_RMS": 'channels_RMS.csv',
    #"MSEED_path": '/mnt/D2A/DAS/MSEED',
    "MSEED_path": '/mnt/D2A/DAS/MSEED/tmp',
    #"MSEED_path": '/mnt/DOMLUIZ/02_MSEED/daily_mseed',

    "SGY_path": '/mnt/D2A/DAS/SGY',
    "pickle_path": '/mnt/D2A/DAS/pickles',
    #"DAS_data_path": '/mnt/D2A/DAS/OptoDAS_SN44/DATA_dphi/20231027/dphi/',
    #"DAS_data_path": '/mnt/SUBMERSE/DATA_dphi/',
    "DAS_data_path": '/mnt/INESCTEC/',
    
    #"experiment_path": '/media/loureiro/SUBMERSE 2/DATA_dphi/',
    #"experiment_path": '/mnt/SUBMERSE/DATA_dphi',
    "experiment_path": '/mnt/INESCTEC/',
    #"experiment_path": '/mnt/DOMLUIZ/DATA_dphi',
    #"experiment_path": '/mnt/D2A/DAS/OptoDAS_SN44/26OCT-02NOV',

    #"events_path": '/mnt/D2A/DAS/OptoDAS_SN44/DATA_dphi/events',
    #"events_path": '/mnt/SUBMERSE/Events/ECHO/BOZZI/',
    "events_path": '/mnt/SUBMERSE/Events/ECHO/',
    
    #"mseed_land_stations": '/mnt/D2A/DAS/CEIDA/OptoDAS_02NOV2023/global-local_events_26OCT2023-02NOV2023.mseed',
    "mseed_land_stations": '/mnt/D2A/DAS/CEIDA/27OCT2023_all-stations.mseed',
    #"mseed_land_stations": '/mnt/D2A/DAS/CEIDA/Package_1719918501081.mseed',
    "xdas_path": '/mnt/SUBMERSE/XDAS',
    "hdf5_headers_example": '/mnt/D2A/DAS/OptoDAS_SN44/26OCT-02NOV/20231027/dphi/125959.hdf5',
    "JSON_template": '/mnt/D2A/DAS/DAS-RCN_example.json',
    "figures_path": '/mnt/D2A/DAS/figures/'
}

station_coordinates = {
    #"PMAR": {"latitude": 32.72, "longitude": -16.91, "channels": "SH*"},
    "PMAR": {"latitude": 32.72, "longitude": -16.91, "channels": "HH*"},
    "PMPST": {"latitude": 33.08, "longitude": -16.33, "channels": "HH*"},
   # "PMPST": {"latitude": 33.08, "longitude": -16.33, "channels": "HN*"},
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

beamforming_kwargs = dict(
    # slowness grid: X min, X max, Y min, Y max, Slow Step
    sll_x=-3.0, slm_x=3.0, sll_y=-3.0, slm_y=3.0, sl_s=0.1,
    # sliding window properties
    win_len=1.0, win_frac=0.010,
    # frequency properties
    frqlow=1.0, frqhigh=10.0, prewhiten=0,
    # restrict output
    semb_thres=-1e9, vel_thres=-1e9, timestamp='mlabday'
)

clock_offset=150
#clock_offset=0

propagation_velocity=5000

first_bad_channel=11293