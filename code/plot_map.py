import pandas as pd
import folium
from pathlib import Path

def main():
    print("Extracting coordinates and setting up the map...")
    BASE_DIR = Path(__file__).resolve().parent.parent
    data_file = BASE_DIR / 'data' / 'rideshare_kaggle.csv'
    
    # Read unique locations from the raw dataset
    df = pd.read_csv(data_file, usecols=['source', 'latitude', 'longitude']).drop_duplicates('source')
    
    # Categorization and mapping for colors
    categories = {
        'Financial District': {'type': 'Business', 'color': 'blue'},
        'North Station': {'type': 'Transit', 'color': 'red'},
        'South Station': {'type': 'Transit', 'color': 'red'},
        'Theatre District': {'type': 'Nightlife', 'color': 'purple'},
        'North End': {'type': 'Nightlife/Dining', 'color': 'purple'},
        'Fenway': {'type': 'Sports/Campus', 'color': 'orange'},
        'Boston University': {'type': 'Campus', 'color': 'orange'},
        'Northeastern University': {'type': 'Campus', 'color': 'orange'},
        'Back Bay': {'type': 'Commercial/Residential', 'color': 'green'},
        'Beacon Hill': {'type': 'Residential', 'color': 'green'},
        'West End': {'type': 'Residential', 'color': 'green'},
        'Haymarket Square': {'type': 'Commercial/Historic', 'color': 'green'}
    }

    # Center map on Boston
    m = folium.Map(location=[42.355, -71.065], zoom_start=13, tiles='CartoDB positron')

    # Add markers
    for _, row in df.iterrows():
        source = row['source']
        lat = row['latitude']
        lon = row['longitude']
        
        cat_info = categories.get(source, {'type': 'Unknown', 'color': 'gray'})
        
        # HTML label for the popup
        popup_html = f"<b>{source}</b><br><i>{cat_info['type']}</i>"
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=source,
            icon=folium.Icon(color=cat_info['color'], icon='info-sign')
        ).add_to(m)

    # Save to HTML
    output_file = BASE_DIR / 'plot' / 'boston_demand_map.html'
    m.save(output_file)
    print(f"Saved interactive map to {output_file} successfully.")

if __name__ == "__main__":
    main()
