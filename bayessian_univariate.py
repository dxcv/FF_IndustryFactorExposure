import numpy as np
import pandas as pd


def gaussian_conj(prior_mean, prior_var, lh_var, x, N):
    # bayessian gaussian conjugate

    post_mean = (prior_mean / prior_var + np.sum(x) / lh_var) / (1 / prior_var + N / lh_var)
    post_var = 1 / (1 / prior_var + N / lh_var)

    return ([post_mean, post_var])


def gaussian_smooth(prior_mean, prior_var, X):
    ## X, df.DataFrame, has two columns, first is obs, second is variance

    post_m = []
    post_v = []

    prior_m = prior_mean
    prior_v = prior_var

    for x in X.values:
        [prior_m, prior_v] = gaussian_conj(prior_mean=prior_m, prior_var=prior_v, lh_var=x[1], x=x[0], N=1)
        post_m.append(prior_m)
        post_v.append(prior_v)

    post_m = pd.Series(post_m, index=X.index)
    post_v = pd.Series(post_v, index=X.index)

    return ([post_m, post_v])
