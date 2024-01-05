#!/bin/sh

import os 
import sys
import numpy as np
import pandas as pd
import processing
import importlib
from matplotlib import dates as mdates
import matplotlib
import pandas as pd
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

#reading ingang and eind data
# artikel_code='AHEK'
# artikel_code= 'TB80120G'
region='Rotterdam'
# # region='Amsterdam'
# # 
# artikel_code_vec=['PB6090']
regionvec=['Rotterdam','Den Haag', 'Amsterdam', 'Assen', 'Utrecht', 'Eindhoven', 'Beverwijk', 'Zwolle']
# vestig_vec=[3,6,9,8,4,7,1,5]
vestig_vec=[3,6,9,8,4,7,5,1]
# num_cores = multiprocessing.cpu_count()
num_cores=8
inputs = tqdm(vestig_vec)

vestig_region={'3':'Rotterdam','6':'Den Haag','9':'Amsterdam','8': 'Assen','4':'Utrecht','7': 'Eindhoven','1': 'Beverwijk', '5':'Zwolle'}


start_year=2007
def parallel_func(vestiging_code):
# artikel_code='AHEK'
    artikel_code_vec=['AHEK','J16-90','PB6090','TB80120G','A01-80-(30)','C02-80']
    # artikel_code_vec=['PB6090','TB80120G','A01-80-(30)']
    region=vestig_region[str(vestiging_code)]   
    start_year=2007
    for artikel_code in artikel_code_vec:
        dirname=os.path.dirname(os.getcwd())
        file_loc=os.path.join(dirname,'processed_data',region)
        day_file=os.path.join(file_loc,artikel_code+'_day'+str(start_year)+'.csv')
        df_day=pd.read_csv(day_file,header=0,sep=',',on_bad_lines='warn')
        print(df_day.keys())
        day_ts=df_day['Net_daily_art']
        year_day_ts=df_day['Date']
        # proc_data_path=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_forecasting\Modelling\processed_data'
        (year_time_series,net_art_month_year_vec)=processing.get_month_ts(day_ts,year_day_ts,start_year)
        month_dict={'Date':year_time_series,'Net_month_art':net_art_month_year_vec}
        df_month=pd.DataFrame.from_dict(month_dict)
        file=os.path.join(file_loc,artikel_code+'_month'+str(start_year)+'.csv')
        df_month.to_csv(file)


        (year_week_time_series,net_art_week_year_vec)=processing.get_week_ts(day_ts,year_day_ts,start_year)
        # print('length: '+str(len(year_week_time_series)))
        # print('length: '+str(len(net_art_week_year_vec)))
        week_dict={'Date':year_week_time_series,'Net_week_art':net_art_week_year_vec[:-2]}
        df_week=pd.DataFrame.from_dict(week_dict)
        file=os.path.join(file_loc,artikel_code+'_week'+str(start_year)+'.csv')
        df_week.to_csv(file)
        
    return(region)
        
if __name__ == "__main__":
    processed_list = Parallel(n_jobs=num_cores)(delayed(parallel_func)(i) for i in inputs)