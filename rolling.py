import statsmodels.api as sm
import numpy as np
import pandas as pd


def rolling_reg( X, y, rolling_index ,window_size):

    ## rollin_index: the index of X and y to roll the regression
    ## window_size: parameter of exp weight.

    ## return: a dict which maps rolling_index to corresponding revalued regression models



    res= {}

    for b in rolling_index:
        tmpX= X.iloc[ X.index< b]
        tmpy= y.iloc[ y.index<b ]
        l = tmpy.shape[0]
        a= list(range( l,0, -1))
        w= [ np.exp(-1* x/window_size) for x in a]

        wls= sm.WLS(  exog= tmpX, endog= tmpy, weights= w )
        wls_res= wls.fit()
        res[b]= wls_res


    return (res)


def rolling_forecast( X, rolling_model):

    # rolling_forecast extracts the most recent revalued model from rolling_model dict and returns the forecast

    ## X: pd.DataFrame with date 'yyyy-mm-dd' as index, the variable matrix

    ## rolling_model: dict mapping date to the rolling revalued model



    pred_list= []
    for key, val in rolling_model.items():
        tmpX= X.iloc[ X.index>=  key]
        pred_list.append( [tmpX.shape[0], pd.Series( val.predict( tmpX), index= tmpX.index, name= 'y_cap')])

    t= pred_list
    pred_list= sorted(t, key= lambda x: x[0], reverse= True)
    res= pred_list[0][1]
    for val in pred_list:
        res.loc[val[1].index]= val[1].tolist()

    return(res)


def rolling_forecasting2(X, params ):
    start_date= params.index[0]
    tmpX= X.loc[ X.index>= start_date]
    tmpZ= pd.DataFrame( [0]*tmpX.shape[0], columns=['to_be_deleted'] , index= tmpX.index )
    params_expanded= pd.concat( [tmpZ, params], axis= 1  , join= 'outer')
    del params_expanded['to_be_deleted']
    params_expanded.fillna( method= 'ffill', inplace= True)

    params_expanded= params_expanded[X.columns]

    res= np.sum( tmpX.values * params_expanded.values, axis= 1)
    res= pd.Series( res, index= params_expanded.index)
    return ((res, params_expanded))



