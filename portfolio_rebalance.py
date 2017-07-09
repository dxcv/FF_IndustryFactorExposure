

def rebalance(ret_data, target_weight, rebalance_date):

    ## rebalance compute the return series of a portfolio tracking a target_weight

    # ret_data, DataFrame with shape N*k, return of the k assets in N periods, indexed by date
    # target_weight, list of size k, the desired weight of k assets
    # rebalance_date, list of size m, sorted date when rebalancing happens.

    # return a DataFrame of portfolio return, val and weight ,
    # starting from the first rebalance_date to the last date of ret_data.
    # the value of a date is the value at the end of date.


    import numpy as np
    import itertools as it
    import pandas as pd

    ret= [0]
    value= [1]
    weight= [[target_weight]]
    tmp= ret_data.iloc[ ret_data.index >= rebalance_date[0]]
    i=0
    for d in tmp.index:
        w= np.array(weight[i])
        if ( d in rebalance_date) :
            w= np.array( target_weight)

        asset_ret= np.array( tmp.loc[d].tolist())
        r= np.dot( w, asset_ret)
        ret.append(r)
        value.append(value[i]* (1+ r))
        new_w= [ x*(1+y) for (x,y) in list(it.zip_longest(w, asset_ret)) ]
        new_w= np.array(new_w)/ np.sum(new_w)
        new_w= new_w.tolist()
        weight.append(new_w)

        i=i+1

    ret= ret[1:]
    value= value[1:]
    weight= weight[1:]

    return ( pd.DataFrame( {'ret': ret,
                            'value': value,
                            'weight': weight}, index= tmp.index))


def ret2val( ret_series):

    import pandas as pd

    val= [1]
    i=0
    for d in ret_series.index:
       val.append(val[i]* (1+ ret_series[d]))
       i+=1

    val= val[1:]
    return (pd.Series( {'val': val}, index= ret_series.index ))
