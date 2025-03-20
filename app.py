import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

# Sample data for demonstration
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "NYC", "NYC", "NYC"]
})

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # Expose the Flask server for deployment

# Define the layout of the app
app.layout = html.Div([
    html.H2("Fruit Sales by City"),
    html.Div([
        # Dropdown to select the city
        dcc.Dropdown(
            id="city-dropdown",
            options=[{"label": city, "value": city} for city in df["City"].unique()],
            value="SF",  # default selection
            clearable=False
        ),
        # Numeric input for minimum sales threshold
        dcc.Input(
            id="min-sales",
            type="number",
            placeholder="Enter minimum sales",
            value=0,    # default threshold
            min=0
        )
    ], style={"display": "flex", "gap": "20px", "margin-bottom": "20px"}),
    # Graph component to display the visualization
    dcc.Graph(id="fruit-graph")
])

# Callback to update the graph based on dropdown and numeric input selections
@app.callback(
    Output("fruit-graph", "figure"),
    [Input("city-dropdown", "value"),
     Input("min-sales", "value")]
)
def update_graph(selected_city, min_sales):
    # Filter data based on the selected city
    filtered_df = df[df["City"] == selected_city]
    # Further filter by the minimum sales threshold if provided
    if min_sales is not None:
        filtered_df = filtered_df[filtered_df["Amount"] >= min_sales]
    # Create a bar chart with Plotly Express
    fig = px.bar(filtered_df, x="Fruit", y="Amount",
                 title=f"Fruit Sales in {selected_city} (Min Sales: {min_sales})")
    return fig

if __name__ == '__main__':
    if os.environ.get('PORT'):
        # Running in a hosted environment (e.g., Render)
        port = int(os.environ.get('PORT'))
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        # Running locally: defaults to localhost:8050
        app.run(debug=True)
