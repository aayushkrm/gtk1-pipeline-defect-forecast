# E06 tuned-shrinkage controls (ON 1km matched-new counts)
- mean_train: MAE=11.29 RMSE=18.41 spear=nan
- C1_tuned_poisson: MAE=21.27 RMSE=93.59 spear=0.728
- C2_log_ridge: MAE=6.48 RMSE=12.85 spear=0.772
- C3_calibrated_B1: MAE=8.87 RMSE=17.60 spear=0.757
  alphas: C1=10.0 C2=0.1 C3map=[0.6824516252474023, 2.5292227732244266]
- HGB MAE=[8.52, 8.52, 8.52] spear=[0.735, 0.735, 0.735]
- C4 shuffle MAE=[12.93, 11.98, 11.5] spear=[-0.415, 0.196, 0.088]
- residual HGB-C3 MAE=[-0.36, -0.36, -0.36] (neg = HGB adds beyond B1)
