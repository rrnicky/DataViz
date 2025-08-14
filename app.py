from dash import Dash, dcc, html, Input, Output, State, no_update
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

import callbacks.homepage_callbacks
import callbacks.preprocessing_callbacks
import callbacks.custom_views_callbacks

# App setup

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
                                 "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
                                 "https://fonts.googleapis.com/css2?family=Inter&display=swap", dbc.themes.BOOTSTRAP])

app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id="url", refresh=False),  # Tracks URL changes
        dcc.Store(id="shared-data"),  # Store for shared data
        #dcc.Store(id="graph-data", data={}),
        dcc.Store(id="store-dropdown", data={"opened": False}),
        html.Div(id="page-content") ,  # Renders pages dynamically
    ],
)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        print(f"App error: {e}")
