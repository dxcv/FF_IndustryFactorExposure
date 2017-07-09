from statsmodels.tsa.ar_model import AR
import pandas as pd
import numpy as np
from numpy.linalg import inv

def OU_fitting ( series ):

    # series: pd.Series, indexed by date

    # return the fitted OU process model params.



    ar_model = AR( endog= series).fit(maxlag= 1)
    [b,a]= ar_model.params.tolist()
    resid_std= np.std( ar_model.resid )

    lam= - np.log(a)
    mu= b/(1-a)
    sigma= resid_std* np.sqrt( -2* np.log(a)/(1-a*a))

    res= {'ar_model': ar_model,
          'lam':lam,
          'mu':mu,
          'sigma': sigma}
    return (res)


def forecasting_variance(X, new_x, err_std):

    XTX_inv= inv(np.dot( X.T, X))
    res= np.dot( np.dot( new_x, XTX_inv), new_x)+1
    res= res* err_std*err_std

    return res



def OU_smoothing( series ,est_date ):

    # series, pd.DataFrame, indexed by date, column value and column std
    # break_date, the date by which data is used to fit OU process

    # return a pd.Series starting from est_date containing the OU smoothed observation

    tmp_series= series.loc[ series.index< est_date]
    OU_fitted= OU_fitting(tmp_series['value'])
    [alpha, theta]= OU_fitted['ar_model'].params.tolist()

    last_obs_by_est= tmp_series['value'].tolist()[-1]
    OU_latest_pred= alpha+ theta* last_obs_by_est
    OU_latest_pred_variance= forecasting_variance( X=OU_fitted['ar_model'].X,
                                                   new_x= [1, last_obs_by_est],
                                                   err_std= np.std( OU_fitted['ar_model'].resid))
    OU_pred= []
    OU_pred_variance= []
    obs=[]
    obs_variance= []
    OU_smoothed_obs=[]
    tmp_series2= series.loc[ series.index>= est_date]

    for d in tmp_series2.index:
        OU_pred_variance.append(OU_latest_pred_variance)
        OU_pred.append(OU_latest_pred)
        obs_std= tmp_series2['std'].loc[ d]
        val = tmp_series2['value'].loc[d]
        obs.append(val)
        obs_variance.append(obs_std* obs_std)

        w= np.array([1/ OU_latest_pred_variance, 1/ (obs_std*obs_std) ])
        w= w/ np.sum(w)


        smoothed_obs=  np.dot( w, np.array([OU_latest_pred, val]))
        OU_smoothed_obs.append( smoothed_obs)


        OU_latest_pred= alpha+ theta* smoothed_obs
        OU_latest_pred_variance= forecasting_variance( X=OU_fitted['ar_model'].X,
                                                       new_x=[1, smoothed_obs],
                                                       err_std=np.std( OU_fitted['ar_model'].resid))


    to_return= pd.DataFrame([ OU_pred, OU_pred_variance, obs, obs_variance, OU_smoothed_obs] ).T
    to_return.columns= ['OU_1period_pred', 'OU_1period_pred_variance',
                        'obs', 'obs_variance', 'OU_smoothed_obs']
    to_return.index= tmp_series2.index



    res1= {'OU_fitted': OU_fitted,
           'OU_smoothed_res': to_return}

    return( res1)



