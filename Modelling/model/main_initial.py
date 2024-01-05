import os 
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import processing
sns.set_theme(context="notebook")

fileloc='../../Raw_data_van_Tim/BISAS Data Ruw/'
file=fileloc+'retourbonregels.csv'
df=pd.read_csv(file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='warn')


orderfile=fileloc+'order.csv'
df=pd.read_csv(orderfile,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='warn')

#let us start with region  and article details
region_file=fileloc+'vestiging.csv'
df_r=pd.read_csv(region_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='warn')
#rotterdam code is 3 
vestiging_code=3
artikel_file=fileloc+'artikel.csv'
df_art=pd.read_csv(artikel_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='warn')
df_art.head()
#let us consider artikel Dranghek
# artikel_code='DRANGHEK'
# artikel_code='991'
artikel_code='BUISPOOT'

start_year=2015
end_year=2016
order_file=fileloc+'order.csv'
reg_order_series,vestiging_series=processing.get_order_numbers(order_file,vestiging_code,start_year,end_year)
print(len(reg_order_series))
(bestel_art_nos_vec,quant_bestel_art_vec,retour_art_nos_vec,manco_art_nos_vec,bestel_b_number_vec,order_number_vec,indate_vec,bestel_b_regel_number_vec)=processing.get_all_data(reg_order_series,artikel_code,0,10)

(enddate_vec,art_retour_vec)=processing.get_enddate(bestel_b_regel_number_vec,artikel_code)

print(bestel_b_regel_number_vec)
print(indate_vec)
year_time_series=pd.date_range(start="01-01-2015",end="01-01-2016",freq='M')

net_art_month_vec=[]
for month in year_time_series.month:
    print(month)
    net_art_month=processing.calculate_net_articles(month,quant_bestel_art_vec,bestel_art_nos_vec,indate_vec,enddate_vec,retour_art_nos_vec)
    net_art_month_vec=np.append(net_art_month_vec,net_art_month)
 
print(net_art_month_vec)
fig=plt.figure()
plt.plot(year_time_series.month,net_art_month_vec)
fig.savefig(r'C:\Users\Amey\Documents\BUKO_forecasting\Results\Month_plot_test_2.jpg')

## Note that the articles per month weren't being correctr because the retour was taken from the Aantal retour column of bestelbonregelks.