# models/

Place your trained model artifacts in this folder. The backend loads them at
startup (see `app/config/settings.py` and `app/inference/predictor.py`):

```
models/production_model.joblib   # preferred; falls back to best_model.joblib
models/best_model.joblib
models/preprocessor.joblib        # REQUIRED
```

These binary files were not part of the source dump — copy them here from your
training machine before deploying. Without `preprocessor.joblib` and a model
file, `/predict` will fail.

If the files are larger than 100 MB, commit them with Git LFS:

```
git lfs install
git lfs track "*.joblib"
git add .gitattributes models/*.joblib
```

You can regenerate them by running `python train.py` (uses `data/raw/creditcard.csv`).
