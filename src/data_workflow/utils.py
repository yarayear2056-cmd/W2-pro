import numpy as np
import pandas as pd


def bootstrap_diff_means(w, u, n_boot=2000, seed=0):
    w_clean= pd.to_numeric(w, errors="coerce").dropna().to_numpy()
    u_clean= pd.to_numeric(u, errors="coerce").dropna().to_numpy()

    assert len(w_clean) > 0 and len(u_clean) > 0, "the groups is empty after cleaning"

    rng = np.random.default_rng(seed)
    diffs = []

    for _ in range(n_boot):
        w_sam = rng.choice(w_clean, size=len(w_clean), replace=True)
        u_sam = rng.choice(u_clean, size=len(u_clean), replace=True)
        diffs.append(w_sam.mean() - u_sam.mean())

    diffs= np.array(diffs)

    return{
        "diff_mean":float(w_clean.mean() - u_clean.mean()),
        "ci_low":float(np.quantile(diffs, 0.025)),
        "ci_h":float(np.quantile(diffs, 0.975)),
    }
        

