import pandas as pd
import numpy as np
from catboost import CatBoostRanker, Pool
from pathlib import Path

def main():
    print("Preparing data for Ranking...")
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file = BASE_DIR / 'data' / 'cleaned_demand.csv'
    
    # Load from cleaned CSV
    df = pd.read_csv(data_file)
    
    # Sort chronologically by group_id
    df = df.sort_values('group_id').reset_index(drop=True)
    
    # Create integer group_id for CatBoost Ranker
    groups = pd.factorize(df['group_id'])[0]
    
    # Features and Target
    X = df[['source', 'temperature', 'precipIntensity', 'hour', 'is_weekend']]
    y = df['order_count'] 

    # Categorical features for CatBoost
    cat_features = ['source']

    # Time series split: 80% train, 20% test
    unique_groups = df['group_id'].unique()
    train_groups_count = int(len(unique_groups) * 0.8)
    train_groups = unique_groups[:train_groups_count]
    train_mask = df['group_id'].isin(train_groups)

    X_train, X_test = X[train_mask], X[~train_mask]
    y_train, y_test = y[train_mask], y[~train_mask]
    group_train, group_test = groups[train_mask], groups[~train_mask]

    print(f"Training data size: {len(X_train)} (Groups: {len(np.unique(group_train))})")
    print(f"Test data size: {len(X_test)} (Groups: {len(np.unique(group_test))})")

    train_pool = Pool(
        data=X_train,
        label=y_train,
        group_id=group_train,
        cat_features=cat_features
    )
    
    test_pool = Pool(
        data=X_test,
        label=y_test,
        group_id=group_test,
        cat_features=cat_features
    )

    model = CatBoostRanker(
        iterations=1000,
        learning_rate=0.1,
        depth=6,
        loss_function='YetiRank',
        eval_metric='NDCG:top=3',
        random_seed=42
    )

    print("\nTraining CatBoostRanker model...")
    model.fit(
        train_pool,
        eval_set=test_pool,
        verbose=50,
        #early_stopping_rounds=50
    )

    model_file = BASE_DIR / 'data' / 'catboost_model.cbm'
    model.save_model(model_file)
    print(f"\nModel successfully saved to {model_file}")

if __name__ == "__main__":
    main()
