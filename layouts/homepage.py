from dash import Dash, dcc, html, Input, Output, State, no_update, callback_context

# Sidebar layout - static
def sidebar_layout():
    print("Sidebar layout is being created")
    return html.Div([
        html.Div([
            html.Div(
                dcc.Upload(
                    id="file-upload",
                    children=html.Button([html.I(className="fas fa-upload"),"  Upload File"],
                        style={
                            "marginBottom": "10px",
                            "width": "120px",
                            "borderRadius": "5px",
                            "border": "none",
                            "backgroundColor": "#333333",
                            "height": "30px",
                            "color": "#999999",
                            "align": "center"
                        }
                    ),
                    style={"display": "inline-block"}
                ),
                style={"display": "flex", "justifyContent": "center", "marginBottom": "10px"}
                # Centers the upload button
            ),
            html.Div(id="file-name-display", style={"marginBottom": "10px", "color": "#ff751a"}),
            # html.Div([
                html.Div([
                    html.Label("Header",
                               style={
                                    "color": "#999999",            # Text color
                                    "fontSize": "12px",         # Font size
                                    "fontWeight": "regular",       # Bold text
                                    "textAlign": "left",      # Center alignment
                                    #"backgroundColor": "lightgray",  # Background color
                                    #"padding": "10px",          # Padding
                                    "display": "block",         # Ensures proper spacing
                                }),
                    dcc.Dropdown(
                        id="header-dropdown",
                        options=[{"label": "Yes", "value": "True"}, {"label": "No", "value": "False"}],
                        value="True",
                        clearable=False,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "10px", "height": "8px",
                               "backgroundColor": "#737373", "border":"none", "borderRadius":"8px"}
                    ),
                ], style={"width": "100%", "paddingRight": "4%"}),

                html.Div([
                    html.Label("Index Column",
                               style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px",  # Font size
                                   "fontWeight": "regular",  # Bold text
                                   "textAlign": "left",  # Center alignment
                                   # "backgroundColor": "lightgray",  # Background color
                                   # "padding": "10px",          # Padding
                                   "display": "block",  # Ensures proper spacing
                               }
                ),
                    dcc.Dropdown(
                        id="index-column-dropdown",
                        options=[{"label": "Yes", "value": "True"}, {"label": "No", "value": "False"}],
                        value="True",
                        clearable=False,
                        style={"marginBottom": "10px", "width": "100%", "fontSize": "10px", "height": "8px","backgroundColor": "#737373", "border":"none","borderRadius":"8px"}
                    ),
                ], style={"width": "100%", "paddingTop": "30px"}),
            # ], style={"display": "flex", "justifyContent": "space-between"}),
            html.Div(
                html.Button("Submit", id="submit-button",
                    style={
                        "marginTop": "20px",
                        "width": "80%",
                        "borderRadius": "5px",
                        "backgroundColor": "#339966",
                        "height": "30px",
                        "border": "none"
                    }
                ),
                style={"display": "flex", "justifyContent": "center", "marginTop": "20px"}  # Centers the submit button
            ),
        ], style={"padding": "10px", "backgroundColor": "#000000", "borderRadius": "10px", "width": "80%","margin": "auto"}),

        html.Button("Visualizer", id="visualizer-button", style={"marginLeft": "10px","marginTop": "40px", "width": "80%", "backgroundColor":"#333333", "border": "none",
        "outline": "none", "boxShadow": "none", "height": "22px", "color": "#999999",  "textAlign": "left", "fontSize": "14px",
                                                                 "cursor": "pointer","fontFamily": "Verdana, sans-serif"}),
        html.Div([
            dcc.Link(
                html.Button("Customize Views", style={"marginLeft": "10px","marginTop": "15px", "width": "80%", "backgroundColor":"#333333", "border": "none",
        "outline": "none", "boxShadow": "none", "height": "22px", "color": "#999999",  "textAlign": "left", "fontSize": "14px",
                                                      "cursor": "pointer","fontFamily": "Verdana, sans-serif" }),
                href="/customize_views"
            ),
        ]),
        html.Div([
            dcc.Link(
                html.Button("Preprocessing", id="preprocessing-button", style={"marginLeft": "10px","marginTop": "15px", "width": "80%", "backgroundColor":"#333333", "border": "none",
        "outline": "none", "boxShadow": "none", "height": "22px", "color": "#999999",  "textAlign": "left", "fontSize": "14px",
                                                                               "cursor": "pointer","fontFamily": "Verdana, sans-serif" }), #"fontWeight": "bold"
                href="/preprocessing"
            )
        ]),
        html.Div([
            dcc.Link(
                html.Button("ML Models", id="ml-models-button", style={"marginLeft": "10px","marginTop": "15px", "width": "80%", "backgroundColor":"#333333", "border": "none",
        "outline": "none", "boxShadow": "none", "height": "22px", "color": "#999999",  "textAlign": "left", "fontSize": "14px",
                                                                       "cursor": "pointer","fontFamily": "Verdana, sans-serif" }),
                href="/ml_models"
            )
        ]),
    ], style={
        "width": "15%",
        "backgroundColor": "#333333",
        "paddingTop": "10px",
        "borderRight": "2px solid #4a4a4a",
        # "display": "flex",
        # "justifyContent": "center",  # Centers content horizontally
        # "alignItems": "center",  # Centers content vertically
        # "flexDirection": "column"
    })

# Main layout
def create_layout():
    return html.Div([
        # Header strip (static)
        html.Div("DataViz", style={
            "backgroundColor": "#000000",
            "color": "#e6ac00",
            "fontSize": "22px",
            "padding-left": "20px",
            "padding-top": "10px",
            "padding-bottom": "10px",
            "textAlign": "left",
            "fontWeight": "regular",
            #"fontStyle": "regular"
        }),

        # Sidebar and main content layout
        html.Div([
            sidebar_layout(),  # Static sidebar

            # Data viewer and summary (dynamic)
            html.Div([
                # DataViewer Section
                html.Div([
                    html.Div("DataViewer", style={
                        "textAlign": "center",
                        "fontSize": "15px",
                        "fontWeight": "regular",
                        "padding": "5px",
                        #"backgroundColor": "#c2d7e0",
                        "color": "#4a4a4a"
                    }),
                    html.Div(id="data-viewer", style={
                        "height": "100vh",
                        #"backgroundColor": "#e5f6ff",
                        "padding": "10px",
                        "overflow": "auto"
                    }),
                ], style={"width": "45%", "float": "left", "borderRight": "2px solid #8c8c8c"}),

                # DataSummary Section
                html.Div([
                    html.Div("DataSummary", style={
                        "textAlign": "center",
                        "fontSize": "15px",
                        "fontWeight": "regular",
                        "padding": "5px",
                        #"backgroundColor": "#c2d7e0",
                        "color": "#4a4a4a"
                    }),
                    html.Div(id="data-summary", style={
                        "height": "100vh",
                        #"backgroundColor": "#e5f6ff",
                        "padding": "10px",
                        "overflow": "auto"
                    }),
                ], style={"width": "55%", "float": "right"}),
            ], style={"width": "85%", "display": "flex", "flexDirection": "row", "justifyContent": "space-between"}),
        ], style={"display": "flex", "flexDirection": "row"})
    ])
