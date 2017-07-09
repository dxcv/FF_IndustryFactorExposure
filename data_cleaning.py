
import pandas as pd
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

# os.chdir('/Users/Eric/FF_IndustryFactorExposure')

start_date= '1986-12-31'
end_date= '2017-03-31'
df_dic= {}

tmp= pd.read_csv('FF_Research6Factors.csv')
tmp['DATE'] = pd.to_datetime( tmp['DATE'].astype(str), format='%Y%m')
tmp.set_index(keys='DATE', inplace=True)
tmp.index.name= None
tmp= tmp.iloc[ np.logical_and(tmp.index> start_date, tmp.index< end_date) ]
df_dic['factor_ret']= tmp



tmp= pd.read_csv('12_Industry_Portfolios_Ret_MktCapWeighted.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype(str), format= '%Y%m')
tmp.set_index(keys='DATE', inplace= True)
tmp.index.name= None
tmp= tmp.iloc[np.logical_and( tmp.index> start_date, tmp.index< end_date) ]
df_dic['industry_ret']= tmp

tmp= pd.read_csv('12_Industry_Portfolios_Ret_EqualWeighted.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype( str), format= '%Y%m')
tmp.set_index(keys= 'DATE', inplace= True)
tmp.index.name= None
tmp= tmp.iloc[ np.logical_and( tmp.index> start_date, tmp.index< end_date) ]
df_dic['industry_ret_ew']= tmp

tmp= pd.read_csv('12_Industry_Portfolios_IndustryCapWeightedBook2Mkt.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype( str), format= '%Y')
tmp.set_index(keys='DATE', inplace= True)
tmp.index.name = None
tmp= tmp.iloc[ np.logical_and( tmp.index> start_date, tmp.index< end_date) ]
tmp= tmp.join(df_dic['factor_ret']['MOM'], how= 'right')
del tmp['MOM']
tmp.fillna( method= 'ffill', inplace= True )
df_dic[ 'industry_avgBM']= tmp

tmp= pd.read_csv( '12_Industry_Portfolios_IndustryBook2Mkt.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype( str), format= '%Y')
tmp.set_index(keys= 'DATE', inplace= True)
tmp.index.name = None
tmp= tmp.iloc[np.logical_and( tmp.index> start_date, tmp.index< end_date)]
tmp= tmp.join( df_dic['factor_ret']['MOM'], how= 'right')
del tmp['MOM']
tmp.fillna( method= 'ffill', inplace= True)
df_dic['industry_BM']= tmp


tmp= pd.read_csv('12_Industry_Portfolios_ComponentsCount.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype( str), format= '%Y%m')
tmp.set_index( keys= 'DATE', inplace= True )
tmp.index.name= None
tmp= tmp.iloc[ np.logical_and(tmp.index> start_date, tmp.index< end_date) ]
df_dic['industry_compCount']= tmp

tmp= pd.read_csv('12_Industry_Portfolios_AvgMktCap.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype( str), format= '%Y%m')
tmp.set_index( keys= 'DATE', inplace= True)
tmp.index.name =None
tmp= tmp.iloc[ np.logical_and( tmp.index> start_date, tmp.index< end_date) ]
df_dic[ 'industry_avgMktCap']= tmp

tmp= pd.read_csv('FF_Research4Factors.csv')
tmp['DATE']= pd.to_datetime( tmp['DATE'].astype(str), format= '%Y%m')
tmp.set_index(keys= 'DATE', inplace= True)
tmp.index.name= None
tmp= tmp.iloc[ np.logical_and( tmp.index> start_date, tmp.index< end_date) ]
df_dic['factor_ret4']= tmp




pickle.dump(df_dic , open('df_dic.p', 'wb'))