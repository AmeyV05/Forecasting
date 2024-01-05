import os 
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_theme(context="notebook")
from matplotlib import dates as mdates
import matplotlib
import pandas as pd
matplotlib.rcParams.update({'font.size': 18,'axes.labelsize':18,'legend.fontsize':16})


fileloc='../../Raw_data_van_Tim/BISAS Data Ruw/'

def get_year_from_datestr_format(datestr,format='%d/%m/%Y'):
    dt_obj=datetime.datetime.strptime(datestr,format)
    return(dt_obj.year)

def get_date_ind(order_date_series,start_year,end_year):
    date_ind=[]
    previous_dates=[]
    for date in order_date_series:
            # print(date)
        if type(date)==str:
            year=get_year_from_datestr_format(date,format='%d-%m-%Y')    
        #     print(year)
            if (date in previous_dates)==False:
                # print(date)
                if (year>=start_year) and (year<end_year):

                    loc=order_date_series.loc[order_date_series==date].index
                    # print(loc)
                    date_ind=np.append(date_ind,loc)
                    previous_dates=np.append(previous_dates,date)
                    # print(date)
    return(date_ind)

def get_order_numbers(order_file,region_code,start_year,end_year):
    # df_order=pd.read_csv(order_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='skip')
    # df_order=pd.read_csv(order_file,header=0,sep=';',on_bad_lines='warn')
    df_order=pd.read_csv(order_file,header=0,sep=',',on_bad_lines='warn')
    vestiging_series=pd.Series(df_order['Vestiging'])
    order_series=pd.Series(df_order['Code'])
    # order_date_series=pd.Series(df_order['Datum'])

    #getting index of region code and the order numbers corresponding to hat.
    reg_index=vestiging_series[vestiging_series==region_code].index
    order_series=order_series[reg_index]
    vestiging_series=vestiging_series[reg_index]
    # order_date_series=order_date_series[reg_index]
    #date.
    #update 23_11 remove date issue
    # start_year=2015
    # end_year=2016
    # date_ind=get_date_ind(order_date_series,start_year,end_year)
    # order_series=order_series[date_ind]
    # vestiging_series=vestiging_series[date_ind]
    order_series=order_series.rename('Order')
    return(order_series,vestiging_series)


def get_artikel_details_bestel_b_regels(bestel_no,artikel_code):
    bestelbonregels_file=fileloc+'bestelbonregels.csv'
    df_bestel_b_regel=pd.read_csv(bestelbonregels_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep="\s*[;]\s*",on_bad_lines='skip',engine='python')  
    #gettting the indices corresponding to bestel bon number
    bestel_b_regel_no_series=pd.Series(df_bestel_b_regel['Code'])
    bestel_b_no_series=pd.Series(df_bestel_b_regel['Bestelbon'])
    bbr_bestel_no_index=bestel_b_no_series[bestel_b_no_series==bestel_no].index
    # bbr_bestel_no_index=[bestel_b_no_series==bestel_no][0]
    #gettting the bb regel no series with bb no index in the file.
    bestel_b_regel_no_series=bestel_b_regel_no_series[bbr_bestel_no_index]
    #checking for artikel
    bestel_b_regel_art_series=pd.Series(df_bestel_b_regel['Artikel'])
    bestel_b_regel_art_quantity_series=pd.Series(df_bestel_b_regel['Aantal'])
    bestel_b_regel_art_quantity_retour_series=pd.Series(df_bestel_b_regel['Aantal Retour'])
    bestel_b_regel_art_quantity_manco_series=pd.Series(df_bestel_b_regel['Aantal manco'])
    #getting all articles for that order number and bestel bon number.
    bestel_b_regel_art_series=bestel_b_regel_art_series[bbr_bestel_no_index]
    print('Artikles in this bestel number are:'+str(bestel_b_regel_art_series))
    print('Number of Artikels in this bestel number are:'+str(len(bestel_b_regel_art_series)))
    bestel_b_regel_art_quantity_series=bestel_b_regel_art_quantity_series[bbr_bestel_no_index] 
    bestel_b_regel_art_quantity_retour_series=bestel_b_regel_art_quantity_retour_series[bbr_bestel_no_index]     
    bestel_b_regel_art_quantity_manco_series=bestel_b_regel_art_quantity_manco_series[bbr_bestel_no_index]
    #getting the artikle number and comparing to our standard.
    bestel_b_regel_art_index=bestel_b_regel_art_series[bestel_b_regel_art_series==artikel_code].index
    if bestel_b_regel_art_index.empty == True:
        print('No artikel of this type in bestel number:'+str(bestel_no))
        art_exist=False
        bestel_art_nos=[]
        bestel_b_regel_no=[]
        retour_art_nos=[]
        manco_art_nos=[]
    else:
        #number of artikels
        bestel_art_nos=bestel_b_regel_art_quantity_series[bestel_b_regel_art_index]
        retour_art_nos=bestel_b_regel_art_quantity_retour_series[bestel_b_regel_art_index]
        manco_art_nos=bestel_b_regel_art_quantity_manco_series[bestel_b_regel_art_index]
        print('Number of Artikels of type '+str(artikel_code)+' in this bestel number are:' +str(bestel_art_nos.values))
        art_exist=True
        bestel_b_regel_no=bestel_b_regel_no_series[bestel_b_regel_art_index]
    return(bestel_art_nos,retour_art_nos,manco_art_nos,art_exist,bestel_b_regel_no)


def get_enddate(bestel_b_regel_number_vec,artikel_code):
    #now comparing to return bon regels and return regels to get the time 
    enddate_vec=[]
    art_retour_vec=[]
    for i in range(len(bestel_b_regel_number_vec[:])):
        bbr_regel=int(bestel_b_regel_number_vec[i])
        retourbonregels_file=fileloc+'retourbonregels.csv'
        df_retour_b_regel=pd.read_csv(retourbonregels_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='skip')  
        retour_b_regel_br_series=pd.Series(df_retour_b_regel['Bestelbonregel'])
        retour_b_regel_brindex=retour_b_regel_br_series[retour_b_regel_br_series==bbr_regel].index
        print(retour_b_regel_brindex)
        if retour_b_regel_brindex.empty==True:
            print('Alert no retour bon corresponding to bestelbon regel:'+str(bbr_regel))
            art_retour_vec=np.append(art_retour_vec,0)
            enddate_vec=np.append(enddate_vec,0)
            continue
        retour_b_regel_rb_series=pd.Series(df_retour_b_regel['Retourbon'])
        retour_b_regel_rb=retour_b_regel_rb_series[retour_b_regel_brindex]
        print('Corresponding retour bon is:'+str(retour_b_regel_rb))
        #artikel and aantal
        retour_b_regel_art_series=pd.Series(df_retour_b_regel['Artikel'])
        retour_b_regel_art_series=retour_b_regel_art_series[retour_b_regel_brindex]
        retour_b_regel_art_quant_series=pd.Series(df_retour_b_regel['Aantal Retour'])
        retour_b_regel_art_quant_series=retour_b_regel_art_quant_series[retour_b_regel_brindex]
        retour_b_regel_art_index=retour_b_regel_art_series[retour_b_regel_art_series==artikel_code].index
        if retour_b_regel_art_index.empty == True:
            print('No artikel of this type in retourbon regel:'+str(bbr_regel))
            art_retour_vec=np.append(art_retour_vec,0)
            enddate_vec=np.append(enddate_vec,0)
            continue
        #number of artikels
        retour_b_regel_art_nos=retour_b_regel_art_quant_series[retour_b_regel_art_index]
        art_retour_vec=np.append(art_retour_vec,retour_b_regel_art_nos)

        ## getting the return date from the retourbon
        retourbon_file=fileloc+'retourbon.csv'
        df_retour_b=pd.read_csv(retourbon_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='skip')  
        #retour bon
        retour_b_no_series=pd.Series(df_retour_b['Code'])
        retour_b_no_index=retour_b_no_series[retour_b_no_series==retour_b_regel_rb.values[0]].index
        end_date_series=pd.Series(df_retour_b['Einddatum huur'])
        enddate_vec=np.append(enddate_vec,end_date_series[retour_b_no_index].values)
    return(enddate_vec,art_retour_vec)


def get_all_data(reg_order_series,artikel_code,s,e):
    bestel_art_nos_vec=[]
    quant_bestel_art_vec=[]
    retour_art_nos_vec=[]
    manco_art_nos_vec=[]
    bestel_b_number_vec=[]
    order_number_vec=[]
    indate_vec=[]
    bestel_b_regel_number_vec=[]
    s=int(s)
    e=int(e)
    
    for order_no in reg_order_series[s:e]:
        print('Checking for order number:'+str(order_no))
        #getting bestelbon code and in date.
        bestelbon_file=fileloc+'bestelbon.csv'
        df_bestel_b=pd.read_csv(bestelbon_file,skip_blank_lines=True,header=0,encoding='ascii',encoding_errors='backslashreplace',sep=';',on_bad_lines='skip')  
        bestel_b_orderseries=pd.Series(df_bestel_b['Order'])
        #comparing to order
        bestel_b_orderindex=bestel_b_orderseries[bestel_b_orderseries==order_no].index
        # bestel_b_orderindex=[bestel_b_orderseries==order_no][0]
        indate_series=pd.Series(df_bestel_b['Ingangdatum huur'])
        order_indate=indate_series[bestel_b_orderindex]
        bestel_b_no_series=pd.Series(df_bestel_b['Code'])
        bestel_b_no_series=bestel_b_no_series[bestel_b_orderindex]
        print('The Bestel bon numbers in this order are:'+str(bestel_b_no_series.values))
        print('Length of the bestel number series is:'+str(len(bestel_b_no_series)))
        for bestel_no in bestel_b_no_series:
            #getting article details from bestel bon regels
            (bestel_art_nos,retour_art_nos,manco_art_nos,art_exist,bestel_b_regel_no)=get_artikel_details_bestel_b_regels(bestel_no,artikel_code)
            if art_exist==False:
                continue
            #getting _start date of huur
            indate_val_bestel_no=order_indate[bestel_b_no_series==bestel_no].values[0]
            bestel_art_nos_vec=np.append(bestel_art_nos_vec,bestel_art_nos.values)
            quant_bestel_art_vec=np.append(quant_bestel_art_vec,len(bestel_art_nos.values))
            retour_art_nos_vec=np.append(retour_art_nos_vec,retour_art_nos.values)
            manco_art_nos_vec=np.append(manco_art_nos_vec,manco_art_nos)
            bestel_b_number_vec=np.append(bestel_b_number_vec,bestel_no)
            order_number_vec=np.append(order_number_vec,order_no)
            indate_vec=np.append(indate_vec,indate_val_bestel_no)
            bestel_b_regel_number_vec=np.append(bestel_b_regel_number_vec,bestel_b_regel_no)
    return(bestel_art_nos_vec,quant_bestel_art_vec,retour_art_nos_vec,manco_art_nos_vec,bestel_b_number_vec,order_number_vec,indate_vec,bestel_b_regel_number_vec)

import datetime
def get_month_from_datestr(datestr):
    format='%d-%m-%Y'
    dt_obj=datetime.datetime.strptime(datestr,format)
    return(dt_obj.month)

def get_year_from_datestr(datestr):
    format='%d-%m-%Y'
    dt_obj=datetime.datetime.strptime(datestr,format)
    return(dt_obj.year)

def get_week_from_datestr(datestr):
    format='%d-%m-%Y'
    dt_obj=datetime.datetime.strptime(datestr,format)
    return(dt_obj.isocalendar().week)

def get_art_quant(quant_bestel_art_vec,art_nos_vec,i):
    #could be either bester or retour art_nos_vec
    quant=quant_bestel_art_vec[i]
    # print(quant)
    if i==0:
        quantsum_prev=0
    else:
        quantsum_prev=np.sum(quant_bestel_art_vec[0:i])
    art_nos_month_i=np.sum(art_nos_vec[int(quantsum_prev):int(quantsum_prev+quant)])
    return(art_nos_month_i)

def calculate_net_articles(month,quant_bestel_art_vec,bestel_art_nos_vec,indate_vec,enddate_vec,retour_art_nos_vec):
    best_art_nos_month=0
    reto_art_nos_month=0
    for i in range(len(indate_vec)):
        indate=indate_vec[i]
        month_indate=get_month_from_datestr(indate)
        if month_indate==month:
            best_art_nos_month_i=get_art_quant(quant_bestel_art_vec,bestel_art_nos_vec,i)
            best_art_nos_month+=best_art_nos_month_i
    for i in range(len(enddate_vec)):    
        enddate=enddate_vec[i]
        month_enddate=get_month_from_datestr(enddate)        
        if month_enddate==month:
            # ret_art_nos_month_i=get_art_quant(quant_bestel_art_vec,retour_art_nos_vec,i)
            reto_art_nos_month_i=retour_art_nos_vec[i]
            reto_art_nos_month+=reto_art_nos_month_i

    net_art_month=best_art_nos_month-reto_art_nos_month
    return(net_art_month)


# def get_common_index(order_series_artikel,reg_order_series):
#     df1=pd.DataFrame(order_series_artikel)
#     common_index=[]
#     for elem in reg_order_series:
#         # print(elem)
#         indi=df1[df1['Order']==int(elem)].index
#         # if len(indi)!=0:
#         #     # print(indi)
#         common_index=np.append(common_index,indi)
#     return(common_index)

def get_common_index(reg_order_series,order_series_artikel):
    intersect=pd.Series(list(set(order_series_artikel.values).intersection(set(reg_order_series))))
    intersect=intersect.rename('Order')
    ind=[]
    for elem in intersect:
        indi=order_series_artikel[order_series_artikel==elem].index
        ind=np.append(ind,indi)
    return(ind)

def get_date_art_number(orderfile,reg_order_series,artikel_code,bon,start_year,end_year):
    reg_order_series=reg_order_series.values.astype(int)
    df_alldata=pd.read_csv(orderfile,header=0,sep=',',on_bad_lines='warn')
    df_alldata.head()
    #gettting indices with the type of artikel.
    artikel_all_series=df_alldata['Artikel']
    artikel_index=artikel_all_series[artikel_all_series.values==artikel_code].index
    order_series_artikel=df_alldata['Order'][artikel_index]
    order_series_artikel=order_series_artikel.astype('int')
    order_series_artikel=order_series_artikel.astype('object')
    if bon=='bestel':
        order_series_date=df_alldata['Ingangdatum huur'][artikel_index]
        aantal_vec=df_alldata['Aantal'][artikel_index]
        date_ind=get_date_ind(order_series_date,start_year,end_year)
        order_series_artikel=order_series_artikel[date_ind]
        order_series_date=order_series_date[date_ind]
        aantal_vec=aantal_vec[date_ind]
        common_index=get_common_index(reg_order_series,order_series_artikel)
        order_series_date=order_series_date[common_index]
        aantal_vec=aantal_vec[common_index]
        net_order_series=order_series_artikel[common_index]

        # aantal_manco_vec=np.array(df_alldata[df_alldata.columns[7]][artikel_index])
        # # aantal_manco_vec=np.where(np.isnan(aantal_manco_vec)==True,0,aantal_manco_vec)
        # for i in  range(len(aantal_manco_vec)):
        #     aantal_manco_vec[i] = aantal_manco_vec[i].replace(' ', '')
    else:
        order_series_date=df_alldata['Einddatum huur'][artikel_index]
        aantal_vec=df_alldata['Aantal Retour'][artikel_index]
        date_ind=get_date_ind(order_series_date,start_year,end_year)
        order_series_artikel=order_series_artikel[date_ind]
        order_series_date=order_series_date[date_ind]
        aantal_vec=aantal_vec[date_ind]
        common_index=get_common_index(reg_order_series,order_series_artikel)
        order_series_date=order_series_date[common_index]
        aantal_vec=aantal_vec[common_index]
        net_order_series=order_series_artikel[common_index]
        
    return(order_series_date,aantal_vec,net_order_series)

def get_issue_dates(date_vec):
    issue_index=[]
    for i in range(len(date_vec.values)):
        date=date_vec.values[i]
        if type(date)==str:
            continue
        else:
            # print(date)
            # print(i)
            issue_index=np.append(issue_index,i)
    return(issue_index)

def make_nanindex_to_zero(aantal_vec):
    nanindex=np.where(np.isnan(aantal_vec.values)==True)[0]
    # print(nanindex)
    #these should be set to zero as there is no data about them.
    aantal_vec.values[nanindex]=0
    return(nanindex,aantal_vec)

def rem_issue_dates(date,aantal,order):
    #takes in series of date, aantal and order
    #removes dates with nan values
    issue_index=get_issue_dates(date)
    date=date.drop(issue_index)
    aantal=aantal.drop(issue_index)
    order=order.drop(issue_index)
    return(date,aantal,order)

def get_end_date_aantal(date,aantal,index,typ):
    inter_in_date=date[index]
    # print(inter_in_date)
    inter_in_date=datetime.datetime.strptime(inter_in_date,'%d-%m-%Y')
    if typ=='Bestel':
        inter_en_date=inter_in_date+datetime.timedelta(days=14)
    else:
        inter_en_date=inter_in_date+datetime.timedelta(days=-14)
    inter_en_date=inter_en_date.strftime('%d-%m-%Y')
    # print(inter_en_date)
    # end_date_int=ind_date.shift(14,ind_date)
    inter_in_aantal=aantal[index]
    return(inter_in_aantal,inter_en_date)

def get_add_date_aantal_vec(intersect_in,in_order,in_date,in_aantal,typ):
    in_order_counts=in_order.value_counts(sort=False)
    in_order_index=pd.Index(in_order)
    in_order_indexval=pd.Index(in_order.index)

    end_add_aantal=[]
    end_add_date=[]
    end_add_order=[]
    val_counts=in_order_counts[intersect_in]
    
    if intersect_in.size!=0:
        # 
        for i in range(len(intersect_in[:])):
            # print(in_order_index.get_loc(intersect_in[i]))
            in_int_ind=(in_order_index.get_loc(intersect_in[i]))
            in_int_ind=in_order_indexval[in_int_ind]
            # print(intersect_in[i])
            # print(in_order[in_int_ind])
            #gettgin end date and end aantal based on in date and aantal
            # print(in_int_ind)
            if type(in_int_ind)==np.int64 or type(in_int_ind)==int:
                # 1 in date for that order number:
                (i_aantal,i_end_date)=get_end_date_aantal(in_date,in_aantal,in_int_ind,typ)
                end_add_aantal=np.append(end_add_aantal,i_aantal)
                end_add_date=np.append(end_add_date,i_end_date)
                end_add_order=np.append(end_add_order,intersect_in[i])
            else:
                # print(in_int_ind)
                for ind in in_int_ind:
                        (i_aantal,i_end_date)=get_end_date_aantal(in_date,in_aantal,ind,typ)
                        end_add_aantal=np.append(end_add_aantal,i_aantal)
                        end_add_date=np.append(end_add_date,i_end_date)
                        end_add_order=np.append(end_add_order,intersect_in[i])
                    
        print('Verifying sum of value  counts:' +str(val_counts.sum()))
        print('Length of add_date='+str(len(end_add_date)))
    
        #     print('no')    
        #     print(in_order_counts[intersect_in[i]])
    return(end_add_date,end_add_aantal,end_add_order)

def getting_merged_series(in_order,in_aantal,in_date,end_order,end_aantal,end_date):
    intersect=pd.Series(list(set(in_order).intersection(set(end_order))))
    intersect_in=pd.Series(list(set(in_order).symmetric_difference(set(intersect))))
    intersect_end=pd.Series(list(set(end_order).symmetric_difference(set(intersect))))
    end_add_date,end_add_aantal,end_add_order=get_add_date_aantal_vec(intersect_in,in_order,in_date,in_aantal,'Bestel')
    in_add_date,in_add_aantal,in_add_order=get_add_date_aantal_vec(intersect_end,end_order,end_date,end_aantal,'Retour')
    end_date_all=pd.concat([end_date,pd.Series(end_add_date)])
    in_date_all=pd.concat([in_date,pd.Series(in_add_date)])
    end_order_all=pd.concat([end_order,pd.Series(end_add_order)])
    in_order_all=pd.concat([in_order,pd.Series(in_add_order)])
    end_aantal_all=pd.concat([end_aantal,pd.Series(end_add_aantal)])
    in_aantal_all=pd.concat([in_aantal,pd.Series(in_add_aantal)])
    #verify merged files
    intersect_test=pd.Series(list(set(in_order_all).symmetric_difference(set(end_order_all))))
    print('Missing order numbers still after addtion are: '+str(intersect_test))
    ## adding one day to end date to not include it in availabe itemsend_date_all=pd.to_datetime(end_date_all,format='%d-%m-%Y')
    end_date_all=pd.to_datetime(end_date_all,format='%d-%m-%Y')
    end_date_all=end_date_all+datetime.timedelta(days=1)
    end_date_all=end_date_all.dt.strftime('%d-%m-%Y')
    return(in_order_all,in_aantal_all,in_date_all,end_order_all,end_aantal_all,end_date_all)
##compute weekly net article is not correct. it should be peak for that week or month so chane needed.,
# def compute_monthly_net_article(month,year,indate_vec,enddate_vec,aantal_retour_vec,aantal_vec):
#     net_art=0
#     for i in range(len(indate_vec)):
#         indate=indate_vec.values[i]
#         # print()
#         if type(indate)==str:
#             month_indate=get_month_from_datestr(indate)
#             year_indate=get_year_from_datestr(indate)
#             if (month_indate==month) & (year_indate==year):
#             # print(i)
#                 net_art+=aantal_vec.values[i]
#         # else:
#         #     print(indate)
#     in_art=net_art
#     net_art=0
#     for i in range(len(enddate_vec)):    
#         enddate=enddate_vec.values[i]
#         if type(enddate)==str:
#             month_enddate=get_month_from_datestr(enddate)     
#             year_enddate=get_year_from_datestr(enddate)   
#             if (month_enddate==month) & (year_indate==year):
#                 net_art+=(aantal_retour_vec.values[i])
#     net_art=in_art-net_art
#     return(net_art)
# ## update on 9_11 when we changed the net_art month from 0 to previous month value
# def get_month_ts(indate_vec,enddate_vec,aantal_retour_vec,aantal_vec,start_year):
#     #getting a time series of a year long data for each month based on 
#     start_date="01-01-"+str(start_year)
#     year_time_series=pd.date_range(start=start_date,end="01-01-2022",freq='M')
#     net_art_month_year_vec=[]
#     net_art=0
#     for year in year_time_series.year[0::12]:
#         print(year)
#         for month in year_time_series.month[:12]:
#             # print(month)
#             net_art_month=compute_monthly_net_article(month,year,indate_vec,enddate_vec,aantal_retour_vec,aantal_vec)
#             net_art=net_art+net_art_month
#             net_art_month_year_vec=np.append(net_art_month_year_vec,net_art)
#     return(year_time_series,net_art_month_year_vec)

# 
# def compute_weekly_net_article(week,year,indate_vec,enddate_vec,aantal_retour_vec,aantal_vec,net_art):
#     # net_art=0
#     for i in range(len(indate_vec)):
#         indate=indate_vec.values[i]
#         # print()
#         if type(indate)==str:
#             week_indate=get_week_from_datestr(indate)
#             year_indate=get_year_from_datestr(indate)
#             if (week_indate==week) & (year_indate==year):
#             # print(i)
#                 net_art+=aantal_vec.values[i]
#         # else:
#         #     print(indate)
#     for i in range(len(enddate_vec)):    
#         enddate=enddate_vec.values[i]
#         if type(enddate)==str:
#             week_enddate=get_week_from_datestr(enddate)     
#             year_enddate=get_year_from_datestr(enddate)   
#             if (week_enddate==week) & (year_indate==year):
#                 net_art+=(-aantal_retour_vec.values[i])
#     return(net_art)

# def get_week_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year):
#     #getting a time series of a year long data for each month based on 
#     start_date="01-01-"+str(start_year)
#     year_weekly_time_series=pd.date_range(start=start_date,end="01-01-2022",freq='W')
#     year_week=year_weekly_time_series.isocalendar().week
#     if year_week[0]==0:
#         year_weekly_time_series=year_weekly_time_series
#     else:
#         year_weekly_time_series=year_weekly_time_series[1:]
        
#     net_art_week_year_vec=[]
#     net_art=0
#     weekvec=np.arange(0,53)+1
    
#     for year in year_weekly_time_series.year[0::53]:
#         print(year)
#         for week in weekvec:      
#             #removing issue with leap year
#             if (year==2015) or (year==2020) or (year==2009):
#                 print(week)
#                 net_art_week=compute_weekly_net_article(week,year,in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,net_art)
#                 net_art=net_art_week
#                 net_art_week_year_vec=np.append(net_art_week_year_vec,net_art_week)
#             else:
#                 if week==53:
#                     continue
#                 else:
#                     print(week)
#                     net_art_week=compute_weekly_net_article(week,year,in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,net_art)
#                     net_art=net_art_week
#                     net_art_week_year_vec=np.append(net_art_week_year_vec,net_art_week)
#     return(year_weekly_time_series,net_art_week_year_vec)  

def get_week_ts(day_ts,year_day_ts,start_year):
    yr_ts=pd.to_datetime(year_day_ts)
    week_ts=yr_ts.dt.isocalendar().week
    year_ts=yr_ts.dt.year
        #getting a time series of a year long data for each month based on 
    start_date="01-01-"+str(start_year)
    year_weekly_time_series=pd.date_range(start=start_date,end="01-01-2022",freq='W')
    year_week=year_weekly_time_series.isocalendar().week
    if year_week[0]==0:
        year_weekly_time_series=year_weekly_time_series
    else:
        year_weekly_time_series=year_weekly_time_series[1:]      
    max_art_week_year_vec=[]
    weekvec=np.arange(0,53)+1  
    for year in year_weekly_time_series.year[0::53]:
        print(year)
        for week in weekvec:      
            #removing issue with leap year
            if (year==2015) or (year==2020) or (year==2009):
                print(week)
                weekindex=np.where(np.logical_and((year_ts.values==year),(week_ts.values==week)))[0]
                art_week=day_ts[weekindex]
                max_art_week=np.max(art_week)
                max_art_week_year_vec=np.append(max_art_week_year_vec,max_art_week)
            else:
                if week==53:
                    continue
                else:
                    print(week)
                    weekindex=np.where(np.logical_and((year_ts.values==year),(week_ts.values==week)))[0]
                    art_week=day_ts[weekindex]
                    max_art_week=np.max(art_week)
                    max_art_week_year_vec=np.append(max_art_week_year_vec,max_art_week)
    return(year_weekly_time_series,max_art_week_year_vec)

def get_month_ts(day_ts,year_day_ts,start_year):
    yr_ts=pd.to_datetime(year_day_ts)
    month_ts=yr_ts.dt.month
    year_ts=yr_ts.dt.year
    #getting a time series of a year long data for each month based on 
    start_date="01-01-"+str(start_year)
    year_time_series=pd.date_range(start=start_date,end="01-01-2022",freq='M')
    max_art_month_year_vec=[]
    for year in year_time_series.year[0::12]:
        print(year)
        for month in year_time_series.month[:12]:
            # print(month)
            # print(week)
            monthindex=np.where(np.logical_and((year_ts.values==year),(month_ts.values==month)))[0]
            art_month=day_ts[monthindex]
            max_art_month=np.max(art_month)
            max_art_month_year_vec=np.append(max_art_month_year_vec,max_art_month)
    return(year_time_series,max_art_month_year_vec) 

def get_week_ts_updated(day_ts,year_day_ts,start_year,end_year):
    yr_ts=pd.to_datetime(year_day_ts)
    week_ts=yr_ts.dt.isocalendar().week
    year_ts=yr_ts.dt.year
        #getting a time series of a year long data for each month based on 
    start_date="01-01-"+str(start_year)
    end_date="01-01-"+str(end_year)
    year_weekly_time_series=pd.date_range(start=start_date,end=end_date,freq='W')
    year_week=year_weekly_time_series.isocalendar().week
    if year_week[0]==0:
        year_weekly_time_series=year_weekly_time_series
    else:
        year_weekly_time_series=year_weekly_time_series[1:]      
    max_art_week_year_vec=[]
    weekvec=np.arange(0,53)+1  
    for year in year_weekly_time_series.year[0::53]:
        print(year)
        for week in weekvec:      
            #removing issue with leap year
            if (year==2015) or (year==2020) or (year==2009):
                print(week)
                weekindex=np.where(np.logical_and((year_ts.values==year),(week_ts.values==week)))[0]
                art_week=day_ts[weekindex]
                max_art_week=np.max(art_week)
                max_art_week_year_vec=np.append(max_art_week_year_vec,max_art_week)
            else:
                if week==53:
                    continue
                else:
                    print(week)
                    weekindex=np.where(np.logical_and((year_ts.values==year),(week_ts.values==week)))[0]
                    art_week=day_ts[weekindex]
                    max_art_week=np.max(art_week)
                    max_art_week_year_vec=np.append(max_art_week_year_vec,max_art_week)
    return(year_weekly_time_series,max_art_week_year_vec)

def compute_daily_net_article(date,indate_vec,enddate_vec,aantal_retour_vec,aantal_vec):
    net_art=0
    for i in range(len(indate_vec)):
        indate=indate_vec.values[i]
        # print()
        if type(indate)==str:
            format='%d-%m-%Y'
            dt_obj=datetime.datetime.strptime((indate),format)
            if dt_obj==date:
                print(dt_obj)
                net_art+=aantal_vec.values[i]
        # else:
        #     print(indate)
    in_art=net_art
    net_art=0
    for i in range(len(enddate_vec)):    
        enddate=enddate_vec.values[i]
        if type(enddate)==str:
            format='%d-%m-%Y'
            dt_obj=datetime.datetime.strptime(enddate,format)
            if dt_obj==date:
                net_art+=(aantal_retour_vec.values[i])
    net_art=in_art-net_art
    return(net_art)

def get_day_ts(in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec,start_year):
    #getting a time series of a year long data for each month based on 
    start_date="01-01-"+str(start_year)
    year_daily_time_series=pd.date_range(start=start_date,end="01-01-2022",freq='D')
    net_art_daily_vec=[]
    net_art_current=0
    for date in year_daily_time_series:
        print(date)
        net_art_daily=compute_daily_net_article(date,in_date_vec,end_date_vec,end_aantal_vec,in_aantal_vec)
        net_art_daily=net_art_daily+net_art_current
        net_art_daily_vec=np.append(net_art_daily_vec,net_art_daily)
        net_art_current=net_art_daily
    return(year_daily_time_series,net_art_daily_vec)    
        

def plot_ts(year_ts,value_ts,artikel_code,region,filename,typ):
    fig,ax=plt.subplots(1, 1, figsize=(30, 8))
    ax.plot(year_ts,value_ts)
    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['font.size']=18
    # setting font sizeto 30

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=12, maxticks=20))
    ax.tick_params(axis='both',labelsize=16)
    plt.tight_layout()
    if typ=='month':
        fig.suptitle('Time series for monthly average of '+artikel_code+' for '+region)
    else:
        fig.suptitle('Time series for weekly average of '+artikel_code+' for '+region)
    fig.savefig(filename)      
    
    
   
def plot_ts_monthly(year_ts,value_ts,artikel_code,region,filename,typ):
    year_ts=pd.to_datetime(year_ts.values)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    monthsFmt = mdates.DateFormatter('%B')
    yearsFmt = mdates.DateFormatter('%Y')
    plt.rcParams["figure.figsize"] = [30, 8]
    plt.rcParams["figure.autolayout"] = True
    fig,ax=plt.subplots(1, 1, figsize=(50, 8))
    ax.plot(year_ts,value_ts,linewidth=1.5)
    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['font.size']=18
    # setting font sizeto 30
    # setting font sizeto 30
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(monthsFmt)
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=12, maxticks=20))
    ax.tick_params(axis='both',labelsize=16)
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90,fontsize=9)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,fontweight='bold')
    plt.tight_layout()
    plt.yticks(fontweight='bold')
    ax.grid(b=True, which='major', color='k', linestyle='--')
    ax.grid(which='minor', color='k', linestyle=':', alpha=0.2)
    if typ=='month':
        fig.suptitle('Time series for monthly average of '+artikel_code+' for '+region)
    else:
        fig.suptitle('Time series for weekly average of '+artikel_code+' for '+region)
    plt.tight_layout()
    fig.savefig(filename,dpi=400) 
           
def plot_ts_weekly(year_ts,value_ts,artikel_code,region,filename,typ):
    year_ts=pd.to_datetime(year_ts.values)
    # year_ts=year_ts.isocalendar().week
    years = mdates.YearLocator()
    weeks=mdates.WeekdayLocator()
    months=mdates.MonthLocator()
    weeksFmt = mdates.DateFormatter('%U')
    yearsFmt = mdates.DateFormatter('%Y')
    plt.rcParams["figure.figsize"] = [30, 8]
    plt.rcParams["figure.autolayout"] = True
    fig,ax=plt.subplots(1, 1, figsize=(50, 8))
    ax.plot(year_ts,value_ts,linewidth=1.5)
    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['font.size']=18
    # setting font sizeto 30
    # setting font sizeto 30
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(weeksFmt)
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=12, maxticks=20))
    ax.tick_params(axis='both',labelsize=16)
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,fontweight='bold')

    plt.yticks(fontweight='bold')
    ax.grid(b=True, which='major', color='k', linestyle='--')
    ax.grid(which='minor', color='k', linestyle=':', alpha=0.2)

    if typ=='month':
        fig.suptitle('Time series for monthly average of '+artikel_code+' for '+region)
    else:
        fig.suptitle('Time series for weekly average of '+artikel_code+' for '+region)
    plt.tight_layout()
    fig.savefig(filename,dpi=400)
           
def plot_ts_daily(year_ts,value_ts,artikel_code,region,filename,typ):
    year_ts=pd.to_datetime(year_ts.values)
    # year_ts=year_ts.isocalendar().week
    years = mdates.YearLocator()
    weeks=mdates.WeekdayLocator()
    months=mdates.MonthLocator()
    weeksFmt = mdates.DateFormatter('%U')
    yearsFmt = mdates.DateFormatter('%Y')
    plt.rcParams["figure.figsize"] = [30, 8]
    plt.rcParams["figure.autolayout"] = True
    fig,ax=plt.subplots(1, 1, figsize=(50, 8))
    ax.plot(year_ts,value_ts,linewidth=1.5)
    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['font.size']=18
    # setting font sizeto 30
    # setting font sizeto 30
    ax.xaxis.set_minor_locator(months)
    ax.xaxis.set_minor_formatter(weeksFmt)
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=12, maxticks=20))
    ax.tick_params(axis='both',labelsize=16)
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)

    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,fontweight='bold')

    plt.yticks(fontweight='bold')
    ax.grid(b=True, which='major', color='k', linestyle='--')
    ax.grid(which='minor', color='k', linestyle=':', alpha=0.2)

    if typ=='day':
        fig.suptitle('Daily time series of '+artikel_code+' for '+region)
    else:
        fig.suptitle('Time series for weekly average of '+artikel_code+' for '+region)
    plt.tight_layout()
    fig.savefig(filename)
    plt.close()
