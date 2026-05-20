import pandas as pd
from pathlib import Path

# Data Source: https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma?resource=download

def main():
    print("Loading raw data...")
    BASE_DIR = Path(__file__).resolve().parent.parent
    file = BASE_DIR / 'data' / 'rideshare_kaggle.csv'
    df = pd.read_csv(file)

    # time zone
    df['dt'] = pd.to_datetime(df['timestamp'], unit='s').dt.tz_localize('UTC').dt.tz_convert('US/Eastern')

    # Calculate time features
    df['hour'] = df['dt'].dt.hour
    df['day_of_week'] = df['dt'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int) # 5=Sat, 6=Sun

    # cleaning feature
    print("Aggregating demand...")
    df['group_id'] = df['dt'].dt.strftime('%Y%m%d%H')
    
    demand_table = df.groupby(['group_id', 'source']).agg(
        order_count=('id', 'count'),
        temperature=('temperature', 'mean'),   
        precipIntensity=('precipIntensity', 'mean'),
        hour=('hour', 'first'),
        is_weekend=('is_weekend', 'first')
    ).reset_index()

    # Save to CSV
    output_file = BASE_DIR / 'data' / 'cleaned_demand.csv'
    demand_table.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Total rows: {len(demand_table)}")

if __name__ == "__main__":
    main()