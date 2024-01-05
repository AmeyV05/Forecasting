import os 
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import processing
import importlib


regionvec=['Rotterdam','Den Haag', 'Amsterdam', 'Assen', 'Utrecht', 'Eindhoven', 'Beverwijk', 'Zwolle']
# vestig_vec=[6,9,8,4,7,1,5,3]
# vestig_vec=[7]
vestig_vec=[6,9,8,4,7,5,1,3]
# vestig_vec=[1]
vestig_region={'3':'Rotterdam','6':'Den Haag','9':'Amsterdam','8': 'Assen','4':'Utrecht','7': 'Eindhoven','1': 'Beverwijk', '5':'Zwolle'}


importlib.reload(processing)
for vestiging_code in vestig_vec[:]:
    # vestiging_code=3
    region=vestig_region[str(vestiging_code)]
    # artikel_code_vec=['AHEK']
    # artikel_code_vec=['PB6090']
    start_year=2007
    artikel_code_vec=['J16-90','PB6090','TB80120G','A01-80-(30)','AHEK','C02-80']
    # artikel_code_vec=['C02-80']    
    for artikel_code in artikel_code_vec:
        # artikel_code= 'TB80120G'
        # region='Rotterdam'p
        # region='Den Haag'|
        # file_loc=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_Forecasting\Modelling\processed_data'
        dirname=os.path.dirname(os.getcwd())
        file_loc=os.path.join(dirname,'processed_data')
        file_loc=file_loc+ "/" + region
        day_file=os.path.join(file_loc,artikel_code+'_day'+str(start_year)+'.csv')
        df_day=pd.read_csv(day_file,header=0,sep=',',on_bad_lines='warn')
        print(df_day.keys())
        day_ts=df_day['Net_daily_art']
        year_month_ts=df_day['Date']
        # results_fileloc=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_Forecasting\Results'+"/"+region
        results_fileloc='../../Results/'+region
        filename=os.path.join(results_fileloc,artikel_code+'_day'+str(start_year)+'.jpg')
        typ='day'
        processing.plot_ts_daily(year_month_ts,day_ts,artikel_code,region,filename,typ)
    