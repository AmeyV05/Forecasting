#!/bin/sh
#%%
import os 
import sys
import numpy as np
import pandas as pd
import processing
import time
# import importlib
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm
# print(multiprocessing.cpu_count())

#%%
#definining initial parameters
fileloc='../../Raw_data_van_Tim/BISAS Data Ruw/'
regionvec=['Rotterdam','Den Haag', 'Amsterdam', 'Assen', 'Utrecht', 'Eindhoven', 'Beverwijk', 'Zwolle']
# vestig_vec=[3,6,9,8,4,7,1,5]
# vestig_vec=[6,9,8,4,7,5]
vestig_vec=[1,3]
# num_cores = multiprocessing.cpu_count()
num_cores=2
inputs = tqdm(vestig_vec)

vestig_region={'3':'Rotterdam','6':'Den Haag','9':'Amsterdam','8': 'Assen','4':'Utrecht','7': 'Eindhoven','1': 'Beverwijk', '5':'Zwolle'}

def parallel_func(vestiging_code):
  
  # for i in range(len(regionvec)):
        # region='Rotterdam'
    region=vestig_region[str(vestiging_code)]   
      #rotterdam code is 3 
    # vestiging_code=3
    # vestiging_code=vestig_vec[i]
    dirname=os.path.dirname(os.getcwd())
    proc_data_path=os.path.join(dirname,'processed_data')
    os.makedirs(proc_data_path+'/'+region, exist_ok=True)
    start_year=2007
    end_year=2022
    ##Reading order file for vestiging/region order numbers and getting only order numbers within that region
    #and within the above date range.
    order_file=fileloc+'order_edited.csv'

    reg_order_series,vestiging_series=processing.get_order_numbers(order_file,vestiging_code,start_year,end_year)
    print('Order reading for vestiging and date done.' )
    artikel_code_vec=['J16-90','PB6090','TB80120G','A01-80-(30)','C02-80','AHEK']
    # artikel_code_vec=['C02-80']
    # artikel_code_vec=['PB6090']
    # artikel_code='AHEK
    for artikel_code in artikel_code_vec:
        st=time.time()
        ### now reading the two files belwo to get the indate and end date along with aantal huur and aantal retour.
        orderfile=fileloc+'bestel_processed.csv'
        bon='bestel'
        indate_vec,aantal_vec,in_order_vec=processing.get_date_art_number(orderfile,reg_order_series,artikel_code,bon,start_year,end_year)
        orderfile=fileloc+'retour_processed.csv'
        bon='retour'
        enddate_vec,aantal_retour_vec,end_order_vec=processing.get_date_art_number(orderfile,reg_order_series,artikel_code,bon,start_year,end_year)
        print('Done reading bestel and retour')
        ### saving in a csv formate.
        ### saving in a csv formate.  
        #two files with in and end order.
        data_dict_in={'Ing_Order':in_order_vec,'Ing_Datum':indate_vec,'Ing_Aantal':aantal_vec}
        data_dict_end={'End_Order':end_order_vec,'End_Datum':enddate_vec,'Ret_Aantal':aantal_retour_vec}
        df_processed_in=pd.DataFrame.from_dict(data_dict_in)
        file=os.path.join(proc_data_path,region,artikel_code+'_ing_'+str(start_year)+'.csv')
        df_processed_in.to_csv(file)
        df_processed_end=pd.DataFrame.from_dict(data_dict_end)
        file=os.path.join(proc_data_path,region,artikel_code+'_end_'+str(start_year)+'.csv')
        df_processed_end.to_csv(file)
        print('Csv file created')
        et=time.time()
        print('Time required is: '+str(et-st) )
    return(region)
          
if __name__ == "__main__":
    processed_list = Parallel(n_jobs=num_cores)(delayed(parallel_func)(i) for i in inputs)