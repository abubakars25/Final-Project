import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the data
file_path = 'merged_df.csv'  # Replace with the actual file path
merged_df = pd.read_csv(file_path)

# Ensure columns are numeric where needed
merged_df['latitude'] = pd.to_numeric(merged_df['latitude'], errors='coerce')
merged_df['longitude'] = pd.to_numeric(merged_df['longitude'], errors='coerce')

# Calculate the top 10 categories with the largest values
top_categories = (
    merged_df['Job Category']
    .value_counts()
    .head(10)
    .index.tolist()
)

# Filter dataset for top categories
top_categories_data = merged_df[merged_df['Job Category'].isin(top_categories)]

# Dropdown options
dropdown_options = [{'label': category, 'value': category} for category in top_categories]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = html.Div([
    html.H1("Job Locations by Frequent Job Categories"),
    
    html.Div([
        html.Label("Select Job Category:"),
        dcc.Dropdown(
            id='job-category-dropdown',
            options=dropdown_options,
            value=top_categories[0],  # Default selection
            clearable=False
        )
    ], style={'width': '50%', 'margin': '20px auto'}),
    
    dcc.Graph(id='job-location-map')
])

# Define callback for interactivity
@app.callback(
    Output('job-location-map', 'figure'),
    [Input('job-category-dropdown', 'value')]
)
def update_map(selected_category):
    # Filter data for the selected category
    filtered_data = top_categories_data[top_categories_data['Job Category'] == selected_category]
    
    # Create map plot
    fig = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        hover_name="Business Title",
        hover_data={"latitude": False, "longitude": False},
        zoom=10,
        height=600,
        title=f"Job Locations for {selected_category}"
    )
    fig.update_layout(mapbox_style="carto-positron", mapbox_center={"lat": 40.7128, "lon": -74.0060},  # NYC center coordinates
                      margin={"r": 0, "t": 30, "l": 0, "b": 0})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
