# E07 small ablation (ON @100m, 7 pre-registered features, SRTO held out)
- cut>=10%: prev 0.241/0.268 match 0.404/0.612 B1=0.644/b=0.268 LR(C=1.0)=0.676 dLR-B1=+0.032[+0.011,+0.053] HGB=0.652 dHGB-B1=+0.008[-0.017,+0.033] F1=0.638 Brier=0.138 shuff=0.336
    weakest-when-dropped: [('nlag', -0.007), ('npipes', 0.024)]
- cut>=12%: prev 0.175/0.181 match 0.353/0.656 B1=0.546/b=0.181 LR(C=0.1)=0.586 dLR-B1=+0.040[+0.014,+0.063] HGB=0.580 dHGB-B1=+0.034[-0.003,+0.069] F1=0.590 Brier=0.106 shuff=0.289
    weakest-when-dropped: [('nlag', 0.006), ('npipes', 0.038)]
- cut>=15%: prev 0.120/0.083 match 0.248/0.701 B1=0.364/b=0.083 LR(C=10.0)=0.340 dLR-B1=-0.024[-0.091,+0.048] HGB=0.360 dHGB-B1=-0.004[-0.073,+0.065] F1=0.440 Brier=0.074 shuff=0.136
    weakest-when-dropped: [('maxd', -0.024), ('meand', -0.024)]
