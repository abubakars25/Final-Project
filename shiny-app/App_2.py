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

# Define the keys and values for the dropdown
data_dict = {
    'Health': 393, 'Policy': 336, 'Planning': 321, 'Public Safety': 301, 'Social Services': 294, 
    'Community Programs': 261, 'Human Resources': 241, 'Legal Affairs': 214, 'Data': 181, 'Accounting': 153, 
    'Finance': 153, 'Health Policy': 120, 'Community Programs Health': 100, 
    'Building Operations': 87
}

# Dropdown options
dropdown_options = [{'label': key, 'value': key} for key in data_dict.keys()]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = html.Div([
    html.H1("Job Locations in New York City by Keyword"),
    
    html.Div([
        html.Label("Select Job Category:"),
        dcc.Dropdown(
            id='job-category-dropdown',
            options=dropdown_options,
            value=dropdown_options[0]['value'],  # Default selection
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
def update_map(selected_key):
    # Filter rows where the selected key is a substring in the 'Job Category'
    filtered_data = merged_df[
        merged_df['Job Category'].str.contains(selected_key, case=False, na=False)
    ]
    
    # Create map plot centered on New York City
    fig = px.scatter_mapbox(
        filtered_data,
        lat="latitude",
        lon="longitude",
        hover_name="Business Title",
        hover_data={"latitude": False, "longitude": False, "Job Category": True},
        zoom=10,  # Adjust zoom for NYC
        height=600,
        title=f"Job Locations for {selected_key}"
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": 40.7128, "lon": -74.0060},  # NYC center coordinates
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
