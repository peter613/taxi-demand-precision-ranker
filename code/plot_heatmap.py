import pandas as pd
import plotly.express as px
from pathlib import Path

def main():
    print("Loading cleaned demand data...")
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file = BASE_DIR / 'data' / 'cleaned_demand.csv'
    df = pd.read_csv(data_file)

    # Calculate average demand per region per hour
    pivot_df = df.pivot_table(index='source', columns='hour', values='order_count', aggfunc='mean')
    
    # Sort regions by overall total demand so the heatmap looks ordered
    pivot_df['total'] = pivot_df.sum(axis=1)
    pivot_df = pivot_df.sort_values('total', ascending=False)
    pivot_df = pivot_df.drop('total', axis=1)

    print("Generating Interactive Heatmap...")
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Hour of the Day (0-23)", y="Region (Source)", color="Average Demand"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="YlOrRd",
        title="Average Rideshare Demand: Region vs. Hour of Day"
    )
    
    fig.update_layout(xaxis_nticks=24)
    
    output_file = BASE_DIR / 'plot' / 'demand_heatmap.html'
    fig.write_html(output_file)
    print(f"Saved {output_file} successfully.")

if __name__ == "__main__":
    main()
