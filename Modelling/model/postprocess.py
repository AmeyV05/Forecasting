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

#reading ingang and eind data
# artikel_code='AHEK'
# artikel_code= 'TB80120G'
region='Rotterdam'
# region='Amsterdam'
# artikel_code_vec=['AHEK','J16-90','PB6090','TB80120G','A01-80-(30)']
artikel_code_vec=['PB6090']
start_year=2010
# artikel_code='AHEK'
for artikel_code in artikel_code_vec:
    file_loc=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_forecasting\Modelling\processed_data'
    file_loc=file_loc+ "/" + region
    in_file=os.path.join(file_loc,artikel_code+'_ing_'+str(start_year)+'.csv')
    end_file=os.path.join(file_loc,artikel_code+'_end_'+str(start_year)+'.csv')
    print(in_file)
    df_in=pd.read_csv(in_file,header=0,sep=',',on_bad_lines='warn')
    print(df_in.keys())
    df_end=pd.read_csv(end_file,header=0,sep=',',on_bad_lines='warn')
    print(df_end.keys())

    in_date_vec=df_in['Ing_Datum']
    in_aantal_vec=df_in['Ing_Aantal']
    issue_index=processing.get_issue_dates(in_date_vec)
    (in_nanindex,in_aantal_vec)=processing.make_nanindex_to_zero(in_aantal_vec)
    print(in_aantal_vec[in_nanindex])
    end_date_vec=df_end['End_Datum']
    end_aantal_vec=df_end['Ret_Aantal']
    end_issue_index=processing.get_issue_dates(end_date_vec)
    (end_nanindex,end_aantal_vec)=processing.make_nanindex_to_zero(end_aantal_vec)
    print(end_aantal_vec[end_nanindex])
    # proc_data_path=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_forecasting\Modelling\processed_data'
    (year_time_series,net_art_month_year_vec)=processing.get_month_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year)
    month_dict={'Date':year_time_series,'Net_month_art':net_art_month_year_vec}
    df_month=pd.DataFrame.from_dict(month_dict)
    file=os.path.join(file_loc,artikel_code+'_month'+str(start_year)+'.csv')
    df_month.to_csv(file)

    (year_week_time_series,net_art_week_year_vec)=processing.get_week_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year)
    week_dict={'Date':year_week_time_series,'Net_week_art':net_art_week_year_vec[:-1]}
    df_week=pd.DataFrame.from_dict(week_dict)
    file=os.path.join(file_loc,artikel_code+'_week'+str(start_year)+'.csv')
    df_week.to_csv(file)