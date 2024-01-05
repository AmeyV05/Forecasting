#script for forcasting functions

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

import statsmodels.api as sm

from statsmodels import stats


def compute_coeff_trend_seasonality(result):
    variance_resid=np.var(result.resid)
    variance_ses=np.var(result.resid+result.seasonal)
    variance_tre=np.var(result.resid+result.trend)
    Fsm=1-(variance_resid/variance_ses)
    Fst=1-(variance_resid/variance_tre)
    print(Fsm)
    print(Fst)

def get_data_series(region,artikel_code,dirname,start_series,end_series):
    start_year=2007
    file_loc=dirname+'Modelling/processed_data/'
    file_loc=file_loc+region
    week_file=os.path.join(file_loc,artikel_code+'_week'+str(start_year)+'.csv')
    df_day=pd.read_csv(week_file,header=0,sep=',',on_bad_lines='warn')
    # print(df_day.keys())
    week_ts=df_day['Net_week_art']
    timevec=df_day['Date']
    week_ts.index=pd.to_datetime(timevec.values)
    ##getting the training_ts
    nyears=int(3)
    #start 
    start=int((start_series-start_year)*52-3)
    end_int=int(end_series-start_series+1)
    train_ts=week_ts[start:start+52*end_int+4]
# print(train_ts.index)
    return(week_ts,train_ts)

def plot_mod_obs(obs,mod,resid,fname):
    # plt.rcParams["figure.figsize"] = [8, 4]
    plt.rcParams["figure.autolayout"] = True
    fig,ax=plt.subplots(1, 1, figsize=(20, 8))
    ax.plot(obs,linewidth=2.0,color='red',linestyle=':',label='Observed')
    ax.plot(mod,linewidth=1.5,color='green',label='Model')
    ax.plot(mod+resid,linewidth=1.0,color='green',alpha=0.7)
    ax.plot(mod-resid,linewidth=1.0,color='green',alpha=0.7)
    ax.legend()
    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['font.size']=18
    ax.grid(b=True, which='major', color='k', linestyle='--')
    ax.grid(which='minor', color='k', linestyle=':', alpha=0.2)
    plt.tight_layout()
    fig.savefig(fname,dpi=250)
    

def create_fcast_csv(forecast,resid,fname,artikel_data_loc):
    forecast=forecast.round()
    max_fcast=forecast+resid
    min_fcast=forecast-resid
    data={'Net_Artikels':forecast,'Max':max_fcast,'Min':min_fcast}
    df=pd.DataFrame(data,columns=['Net_Artikels','Max','Min'])
    fnameloc=os.path.join(artikel_data_loc,fname)
    pd.Series.to_csv(df,fnameloc)
    print('Saving done')