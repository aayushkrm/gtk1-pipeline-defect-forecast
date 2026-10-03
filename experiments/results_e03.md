# E03 count + rare-target + grid ablation (ON, matched-new counts)
count target: mean tr/te 10.51/10.10 max_te 132 zero_frac 0.25
- mean_train: MAE=11.29 RMSE=18.41 spear=nan [nan,nan]
- persistence: MAE=12.33 RMSE=27.77 spear=0.757 [0.671,0.825]
- poisson_glm: MAE=21.28 RMSE=93.67 spear=0.728 [0.628,0.802]
- hgb_poisson_s0: MAE=8.52 RMSE=16.05 spear=0.735 [0.638,0.812]
- new-in-clean: n tr/te 51/27 prev tr/te 0.529/0.407
- grid 100m presence: AP_B1=0.821 base=0.369 n=1331 pos=491
- grid 1000m presence: AP_B1=0.961 base=0.858 n=134 pos=115
