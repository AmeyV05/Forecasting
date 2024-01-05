#!/bin/sh
###script to test for pre-process with Tim.
## Input is a series of order numbers and their corresponding index from the order.csv file

import os 
import sys
import numpy as np
import pandas as pd
import processing
import time
# import importlib
def get_in_out(reg_order_series):
    #definining initial parameters
    fileloc='../../Raw_data_van_Tim/BISAS Data Ruw/'
    regionvec=['Rotterdam']
    vestig_vec=[3]
    for i in range(len(regionvec)):
            # region='Rotterdam'
        region=regionvec[i]
        #rotterdam code is 3 
        # vestiging_code=3
        vestiging_code=vestig_vec[i]
        proc_data_path=r'C:\Users\Amey.RISE3D\OneDrive - RISE3D\Documents\BUKO_forecasting\Modelling\processed_data'
        start_year=2010
        end_year=2022
        ##Reading order file for vestiging/region order numbers and getting only order numbers within that region
        #and within the above date range.
        order_file=fileloc+'order_edited.csv'

        # reg_order_series,vestiging_series=processing.get_order_numbers(order_file,vestiging_code,start_year,end_year)
        print('Order reading for vestiging and date done.' )
        artikel_code_vec=['AHEK','J16-90','PB6090','TB80120G','A01-80-(30)']
        # artikel_code_vec=['PB6090']
        # artikel_code='AHEK'
        for artikel_code in artikel_code_vec:
            st=time.time()
            ### now reading the two files belwo to get the indate and end date along with aantal huur and aantal retour.
            orderfile=fileloc+'bestel_processed.csv'
            bon='bestel'
            indate_vec,aantal_vec,in_order_vec=processing.get_date_art_number(orderfile,reg_order_series,artikel_code,bon)
            orderfile=fileloc+'retour_processed.csv'
            bon='retour'
            enddate_vec,aantal_retour_vec,end_order_vec=processing.get_date_art_number(orderfile,reg_order_series,artikel_code,bon)
            print('Done reading bestel and retour')
            ### saving in a csv formate.
            ### saving in a csv formate.  
            #two files with in and end order.
            data_dict_in={'Ing_Order':in_order_vec,'Ing_Datum':indate_vec,'Ing_Aantal':aantal_vec}
            data_dict_end={'End_Order':end_order_vec,'End_Datum':enddate_vec,'Ret_Aantal':aantal_retour_vec}
            df_processed_in=pd.DataFrame.from_dict(data_dict_in)
            file=os.path.join(proc_data_path,region,artikel_code+'_ing_'+str(start_year)+'_test.csv')
            df_processed_in.to_csv(file)
            df_processed_end=pd.DataFrame.from_dict(data_dict_end)
            file=os.path.join(proc_data_path,region,artikel_code+'_end_'+str(start_year)+'_test.csv')
            df_processed_end.to_csv(file)
            print('Csv file created')
            et=time.time()
            print('Time required is: '+str(et-st) )