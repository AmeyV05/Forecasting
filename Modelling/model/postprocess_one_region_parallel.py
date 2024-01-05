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
# region='Rotterdam'
# # region='Amsterdam'
# # 
# artikel_code_vec=['PB6090']
vestig_vec=[3,6,9,8,4,7,1,5]
regionvec=['Beverwijk']
vestiging_code=1
# num_cores = multiprocessing.cpu_count()


vestig_region={'3':'Rotterdam','6':'Den Haag','9':'Amsterdam','8': 'Assen','4':'Utrecht','7': 'Eindhoven','1': 'Beverwijk', '5':'Zwolle'}
artikel_code_vec=['C02-80','AHEK','J16-90','PB6090','TB80120G','A01-80-(30)']
# artikel_code_vec=['J16-90']
num_cores=6
inputs = tqdm(artikel_code_vec)

region=vestig_region[str(vestiging_code)]  
start_year=2007
def parallel_func(artikel_code):
# artikel_code='AHEK'
    # artikel_code_vec=['AHEK','J16-90','PB6090','TB80120G','A01-80-(30)']
 
    start_year=2007
    # for artikel_code in artikel_code_vec:
    dirname=os.path.dirname(os.getcwd())
    file_loc=os.path.join(dirname,'processed_data',region)
    in_file=os.path.join(file_loc,artikel_code+'_ing_'+str(start_year)+'.csv')
    end_file=os.path.join(file_loc,artikel_code+'_end_'+str(start_year)+'.csv')
    print(in_file)
    df_in=pd.read_csv(in_file,header=0,sep=',',on_bad_lines='warn')
    print(df_in.keys())
    df_end=pd.read_csv(end_file,header=0,sep=',',on_bad_lines='warn')
    print(df_end.keys())
    #requires in put df_in and df_end
    in_date=df_in['Ing_Datum']
    in_aantal=df_in['Ing_Aantal']
    in_order=df_in['Ing_Order']
    #issue index is where date is a nan. we remove those indices.
    in_date,in_aantal,in_order=processing.rem_issue_dates(in_date,in_aantal,in_order)
    #change nan in aantal to zero
    (in_nanindex,in_aantal)=processing.make_nanindex_to_zero(in_aantal)
    ##end
    end_date=df_end['End_Datum']
    end_aantal=df_end['Ret_Aantal']
    end_order=df_end['End_Order']
    end_date,end_aantal,end_order=processing.rem_issue_dates(end_date,end_aantal,end_order)
    #change nan in aantal to zero
    (end_nanindex,end_aantal)=processing.make_nanindex_to_zero(end_aantal)

    # doing two things
    # 1. adding 1 extra day to end date
    # 2 finding orders missing in bestel and retour bns and adding 14 daysto them
    (in_order,in_aantal,in_date,end_order,end_aantal,end_date)=processing.getting_merged_series(in_order,in_aantal,in_date,end_order,end_aantal,end_date)
    
    # proc_data_path=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_forecasting\Modelling\processed_data'
    # (year_time_series,net_art_month_year_vec)=processing.get_month_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year)
    # month_dict={'Date':year_time_series,'Net_month_art':net_art_month_year_vec}
    # df_month=pd.DataFrame.from_dict(month_dict)
    # file=os.path.join(file_loc,artikel_code+'_month'+str(start_year)+'.csv')
    # df_month.to_csv(file)

    # (year_week_time_series,net_art_week_year_vec)=processing.get_week_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year)
    # week_dict={'Date':year_week_time_series,'Net_week_art':net_art_week_year_vec[:-1]}
    # df_week=pd.DataFrame.from_dict(week_dict)
    # file=os.path.join(file_loc,artikel_code+'_week'+str(start_year)+'.csv')
    # df_week.to_csv(file)
    (year_daily_time_series,net_art_daily_vec)=processing.get_day_ts(in_date,end_date,end_aantal,in_aantal,start_year)
    day_dict={'Date':year_daily_time_series,'Net_daily_art':net_art_daily_vec}
    df_day=pd.DataFrame.from_dict(day_dict)
    file=os.path.join(file_loc,artikel_code+'_day'+str(start_year)+'.csv')
    df_day.to_csv(file)
        
    return(region)
        
if __name__ == "__main__":
    processed_list = Parallel(n_jobs=num_cores)(delayed(parallel_func)(i) for i in inputs)