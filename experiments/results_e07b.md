# E07b null-calibration + ablation-vs-full + SRTO holdout (frozen ≤7 feats)
- cut>=10%: base=0.268 const=0.268 (gap +0.0000) | LR=0.676 null=0.365 null-baseCI=[-0.066,+0.275] | d-vs-null=+0.311[+0.263,+0.354]
    abl-vs-full: [('nlag', -0.039), ('npipes', -0.008), ('n_past', -0.002), ('maxd', 0.002), ('gwan', 0.002), ('mech', 0.005), ('meand', 0.006)]
- cut>=12%: base=0.181 const=0.181 (gap +0.0000) | LR=0.586 null=0.289 null-baseCI=[-0.058,+0.314] | d-vs-null=+0.297[+0.238,+0.363]
    abl-vs-full: [('nlag', -0.036), ('npipes', -0.002), ('gwan', -0.001), ('mech', 0.001), ('maxd', 0.002), ('n_past', 0.002), ('meand', 0.006)]
- SRTO holdout: LR=0.281 B1=0.277 base=0.061 dCI=[-0.032,+0.039]
