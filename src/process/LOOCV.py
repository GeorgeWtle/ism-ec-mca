from init.const import *
from init.lib import *
from init.func import *

from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS, pr_trend_JJAS_SA, pr_change_JJAS_SA

# MCA between pr_trend_JJAS and pr_change_JJAS
# LEFT FIELD X
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over EISM
# RIGHT FIELD Y
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over EISM

X, Y, HM_X_SA, HM_X_init, HT_pr_change_JJAS_SA, HT_Y_init, PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS,
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y
)

warnings.filterwarnings("ignore")

M = 5 # number of mode considered
MCA_only = True # no need to get the HM & HT maps

N = len(pr_change_JJAS_SA.time) # number of models

error2_list = [ [] for _ in range(M) ] # store the squarred error

Y_hat_list = []
Y_c_LOOCV_list = []

weights = np.sqrt(np.cos(np.deg2rad(pr_trend_JJAS_SA.lat)))

print("Perform LOOCV:")
for model in range (N):
    print(f"--- remove model {model} / {N-1}    ", end = "\r")

    pr_change_JJAS_SA_1 = pr_change_JJAS_SA.drop_sel(time = model) # remove one model
    # pr_change_JJAS_SA_1 = pr_change_JJAS_SA # * if you want to keep all models
    
    X, Y, PC, EOF, _, _, _, _, _, _ = comp_HM_HT(
        pr_trend_JJAS.drop_sel(time = model), pr_change_JJAS.drop_sel(time = model), # do the MCA without a model
        # pr_trend_JJAS, pr_change_JJAS, # * if you want to keep all models
        box_X = box_X, mask_X = mask_X, mval_X = mval_X,
        box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y,
        MCA_only = MCA_only,
        M = M
    )

    EC_a_label = [f"a{i}" for i in range (M)]
    EC_a_df = pd.DataFrame(
        [PC["a"].isel(mode = i).values for i in range (M)],
        index = EC_a_label
    ).T # contains M ECs as columns

    gamma_ds = qr_multiple_reg(pr_change_JJAS_SA_1, EC_a_df) # get all heterogeneous maps and associated r2, pval
    
    # gamma_ds = [
    #    \gamma_1,                                              using 1 mode
    #    \gamma_1, \gamma_2,                                    using 2 mode
    #    \gamma_1, \gamma_2, \gamma_3,                          using 3 mode    
    #    \gamma_1, \gamma_2, \gamma_3, \gamma_4,                using 4 mode
    #    \gamma_1, \gamma_2, \gamma_3, \gamma_4, \gamma_5       using 5 mode
    # ]

    if box_X is not None:
        X_box = crop(pr_trend_JJAS, box = box_X) # croped field
        X_O_SA = X_box.copy(deep = True)
    if mask_X is not None:
        X_box_masked = mask(X_box, crop(mask_X, box = box_X), mval_X) # croped and masked field
        X_O_SA = X_box_masked.copy(deep = True)
            
    X_O_SA = X_O_SA.isel(time = model) # use the removed model as a pseudo obs

    # !
    mca = xMCA(X, Y)
    mca.apply_coslat()
    mca.solve()

    eofs = mca.eofs(n = M)
    u, v = eofs["left"], eofs["right"]
    pcs = mca.pcs(n = M, scaling = "eigen")
    a, b = pcs["left"], pcs["right"]

    Y_hat_ctd_list = []
    Y_c_list = []
    
    for m in range (M):
        gamma_da = gamma_ds.isel(nb_of_mode = m)["slope"]
        Y_hat_ctd_m = xr.zeros_like(pr_change_JJAS_SA_1.isel(time = 0)).drop_vars("time")
        Y_c_m = xr.zeros_like(pr_change_JJAS_SA_1)
        for i in range(m+1):
            a_i = ((EOF["u"].isel(mode = i).fillna(0) * (X_O_SA - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) # project one data point
            a_i_c = ((EOF["u"].isel(mode = i).fillna(0) * (X_O_SA - X).fillna(0)) * weights).sum(dim = ["lon", "lat"]) # project one data point
            gamma_i = gamma_da.sel(coef = f"a{i}")
            Y_hat_ctd_m += gamma_i * (a_i / ((EOF["u"].isel(mode = i).fillna(0) * (X - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time"))
            Y_c_m += gamma_i * (a_i_c / ((EOF["u"].isel(mode = i).fillna(0) * (X - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time"))
        Y_hat_ctd_list.append(Y_hat_ctd_m.copy(deep=True))
        Y_c_list.append(Y_c_m.copy(deep=True))

    Y_hat_ctd_LOOCV = xr.concat(Y_hat_ctd_list, dim="nb_of_mode")
    Y_hat_ctd_LOOCV = Y_hat_ctd_LOOCV.assign_coords(nb_of_mode=range(1, M+1))
    Y_c_LOOCV = xr.concat(Y_c_list, dim="nb_of_mode")
    Y_c_LOOCV = Y_c_LOOCV.assign_coords(nb_of_mode=range(1, M+1))
    Y_c_LOOCV = pr_change_JJAS_SA_1 + Y_c_LOOCV
    Y_c_LOOCV_list.append(Y_c_LOOCV)
    
    Y_hat = pr_change_JJAS_SA_1.mean(dim = "time") + Y_hat_ctd_LOOCV
    Y_hat_list.append(Y_hat)

    for nb_of_mode in range (M) :
        error = Y_hat.isel(nb_of_mode = nb_of_mode) - pr_change_JJAS_SA.isel(time = model)
        error2 = error **2
        error2_list[nb_of_mode].append(error2)
    
error2 = xr.concat(
    [xr.concat(error2_m, dim = "time") for error2_m in error2_list], dim = "nb_of_mode"
)
MSE = error2.mean(dim = "time")
Y_hat_LOOCV = xr.concat(Y_hat_list, dim="time") # contains all estimation; # ? seem like Y_estimation.var(dim = "time") reduces to the var variable
Y_c_LOOCV = xr.concat(Y_c_LOOCV_list, dim="left_out") # contains all estimation; # ? seem like Y_estimation.var(dim = "time") reduces to the var variable

###################

pr_change_JJAS_SA_1 = pr_change_JJAS_SA # * if you want to keep all models

X, Y, PC, EOF, _, _, _, _, _, _ = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS, # * if you want to keep all models
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y,
    MCA_only = MCA_only,
    M = M
)

EC_label = [f"a{i}" for i in range (M)]
EC_df = pd.DataFrame(
    [PC["a"].isel(mode = i).values for i in range (M)],
    index = EC_label
).T # contains M ECs as columns

gamma_ds = qr_multiple_reg(pr_change_JJAS_SA_1, EC_df) # get all heterogeneous maps

# gamma_ds = [
#    \gamma_1,                                              using 1 mode
#    \gamma_1, \gamma_2,                                    using 2 mode
#    \gamma_1, \gamma_2, \gamma_3,                          using 3 mode    
#    \gamma_1, \gamma_2, \gamma_3, \gamma_4,                using 4 mode
#    \gamma_1, \gamma_2, \gamma_3, \gamma_4, \gamma_5       using 5 mode
# ]

Y_hat_ctd_list = []

for m in range (M):
    gamma_da = gamma_ds.isel(nb_of_mode = m)["slope"]
    Y_hat_ctd_m = xr.zeros_like(pr_change_JJAS_SA_1)
    for i in range(m+1):
        a_i = PC["a"].isel(mode = i)
        gamma_i = gamma_da.sel(coef = f"a{i}")
        Y_hat_ctd_m += gamma_i * a_i
    Y_hat_ctd_list.append(Y_hat_ctd_m.copy(deep=True))

Y_hat_ctd = xr.concat(Y_hat_ctd_list, dim="nb_of_mode")
Y_hat_ctd = Y_hat_ctd.assign_coords(nb_of_mode=range(1, M+1))
Y_hat = pr_change_JJAS_SA_1.mean(dim = "time") + Y_hat_ctd