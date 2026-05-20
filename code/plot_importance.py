import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from catboost import CatBoostRanker, Pool
from pathlib import Path

def main():
    print("Loading data...")
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file = BASE_DIR / 'data' / 'cleaned_demand.csv'
    model_file = BASE_DIR / 'data' / 'catboost_model.cbm'
    
    df = pd.read_csv(data_file)
    df = df.sort_values('group_id').reset_index(drop=True)
    
    X = df[['source', 'temperature', 'precipIntensity', 'hour', 'is_weekend']]
    y = df['order_count']
    groups = pd.factorize(df['group_id'])[0]
    
    print("Loading model...")
    model = CatBoostRanker()
    model.load_model(model_file)
    
    sample_size = min(1000, len(X))
    X_sample = X.iloc[:sample_size]
    y_sample = y.iloc[:sample_size]
    group_sample = groups[:sample_size]
    
    pool = Pool(
        data=X_sample,
        label=y_sample,
        group_id=group_sample,
        cat_features=['source']
    )
    
    print("Generating Feature Importance plot...")
    importances = np.abs(model.get_feature_importance(data=pool))
    feature_names = X.columns
    
    idx = np.argsort(importances)
    plt.figure(figsize=(8, 5))
    plt.barh(np.array(feature_names)[idx], np.array(importances)[idx], color='skyblue')
    plt.xlabel('Feature Importance Score')
    plt.title('CatBoost Feature Importance')
    plt.tight_layout()
    
    feat_imp_file = BASE_DIR / 'plot' / 'feature_importance.png'
    plt.savefig(feat_imp_file, dpi=150)
    plt.close()
    
    print("Generating SHAP summary plot...")
    shap_vals = model.get_feature_importance(data=pool, type='ShapValues')
    shap_values = shap_vals[:, :-1]
    
    plt.figure(figsize=(10, 6))
    
    # Convert categorical strings to codes for SHAP plotting
    X_plot = X_sample.copy()
    for col in X_plot.columns:
        if X_plot[col].dtype == 'object':
            X_plot[col] = X_plot[col].astype('category').cat.codes

    shap.summary_plot(shap_values, X_plot, show=False)
    plt.tight_layout()
    
    shap_file = BASE_DIR / 'plot' / 'shap_summary.png'
    plt.savefig(shap_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Done! Saved {feat_imp_file.name} and {shap_file.name}")

if __name__ == "__main__":
    main()
