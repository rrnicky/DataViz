from dash import html, dcc


row_style = {
    "display": "flex",
    "justifyContent": "space-around",
    "marginBottom": "10px"
}
button_style = {
    "border": "none",
    "background": "none",
    "cursor": "pointer",
    "padding": "10px",
}

icon_style = {
    'fontSize': '28px',
    'color': 'white',
    'cursor': 'pointer',
    'padding': '4px',
    'borderRadius': '6px',
    'textAlign': 'center',
}

icon_wrapper = {
    "display": "inline-block",
    "textAlign": "center",
}

selected_icon_style = {
    'backgroundColor': '#00ADB5',
    'borderRadius': '12px',
    'padding': '8px',
    'color': 'white'
}

custom_views_layout = html.Div(
    children=[
        html.Div(
            children=[
                dcc.Store(id='data-store',storage_type='session'),
                dcc.Store(id='selected-graph-icon',storage_type='session'),
                html.Span("DataViz - Custom Views", style={"fontSize": "22px"}),  # DataViz Text

                # Home Button - Positioned to Right
                html.A(
                    html.I(className="fa fa-home"),  # Home Icon
                    href="/",  # Redirect to Homepage
                    style={
                        "position": "absolute",
                        "right": "20px",  # Adjust Right Spacing
                        "top": "50%",  # Align Vertically
                        "transform": "translateY(-50%)",  # Center Align
                        "fontSize": "18px",  # Increase Size
                        "textDecoration": "none",
                        "color": "white",  # Set Icon Color
                        "cursor": "pointer",
                    }
                )
            ],
            style={
                "backgroundColor": "#000000",
                "color": "#e6ac00",
                "fontSize": "18px",
                "padding": "10px 20px",
                "textAlign": "left",
                "position": "relative",  # Enable Absolute Positioning for Home Icon
            }
        ),
        html.Div(
            style={
                "display": "flex",
                "background-color": "#d3d3d3",
                "height": "100vh",
            },
            children=[
                html.Div(
                    id="sidebar",
                    style={
                        "width": "20%",  # Increased width for more options
                        "padding": "10px",
                        "display": "flex",
                        "flex-direction": "column",
                        "gap": "15px",
                        "background-color": "#333333",
                        "overflowY": "auto"  # Allow scrolling if content is too tall
                    },
                    children=[
                        dcc.Upload(
                            id="upload-data",
                            children=html.Div(["📁 Upload File"]),
                            style={"color": "white", "backgroundColor": "#666", "padding": "10px",
                                   "borderRadius": "5px", "textAlign": "center", "cursor": "pointer"},
                            multiple=False
                        ),
                        html.Div(id="filename-display", style={"color": "white", "marginTop": "10px"}),
                        html.Div([
                            html.Div([
                                html.Label("Select Graph Type", style={
                                    "fontSize": "14px", "color": "#999999", "marginLeft": "9px", "marginTop": "20px"
                                }),

                                html.Div([
                                    # Row 1
                                    html.Div([
                                        html.I(
                                            className="fas fa-braille",
                                            id={'type': 'graph-icon', 'index': 'scatter'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-chart-line",
                                            id={'type': 'graph-icon', 'index': 'line'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-chart-bar",
                                            id={'type': 'graph-icon', 'index': 'bar'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ],
                                        style=row_style),

                                    # Row 2
                                    html.Div([
                                        html.I(
                                            className="fas fa-chart-pie",
                                            id={'type': 'graph-icon', 'index': 'pie'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-water",
                                            id={'type': 'graph-icon', 'index': 'area'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-th",
                                            id={'type': 'graph-icon', 'index': 'heatmap'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ], style=row_style),

                                    # Row 3
                                    html.Div([
                                        html.I(
                                            className="fas fa-project-diagram",
                                            id={'type': 'graph-icon', 'index': 'gantt'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-circle",
                                            id={'type': 'graph-icon', 'index': 'bubble'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-box",
                                            id={'type': 'graph-icon', 'index': 'box'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ], style=row_style),

                                    # Row 4 – Custom Charts
                                    html.Div([
                                        html.I(
                                            className="fas fa-dot-circle",
                                            id={'type': 'graph-icon', 'index': 'donut'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-compact-disc",
                                            id={'type': 'graph-icon', 'index': 'radial-bar'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-bullseye",
                                            id={'type': 'graph-icon', 'index': 'polar-area'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ], style=row_style),

                                    # Row 5 – Custom Charts
                                    html.Div([
                                        html.I(
                                            className="fas fa-align-left",
                                            id={'type': 'graph-icon', 'index': 'stacked-bar'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-sync",
                                            id={'type': 'graph-icon', 'index': 'radial-line'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-sort-amount-down",
                                            id={'type': 'graph-icon', 'index': 'waterfall'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ], style=row_style),

                                    # Row 6 – Custom Charts
                                    html.Div([
                                        html.I(
                                            className="fas fa-filter",
                                            id={'type': 'graph-icon', 'index': 'funnel'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-radiation",
                                            id={'type': 'graph-icon', 'index': 'radar'},
                                            n_clicks=0,
                                            style=icon_style  # Plain style by default
                                        ),
                                        html.I(
                                            className="fas fa-sort-amount-up-alt",
                                            id={'type': 'graph-icon', 'index': 'pyramid'},
                                            n_clicks=0,
                                            style=icon_style
                                        ),
                                    ], style=row_style),

                                ], style={"marginTop": "20px"})
                            ]),
                            html.Div(id="submit-trigger", style={"display": "none"}),
                        ],
                        ),
                        # Custom Options Section - REMOVED FROM SIDEBAR
                        # html.Div(id="custom-options", style={"marginTop": "20px"}),
                        html.Div(id="validation-message", style={"color": "red", "marginTop": "10px"}),
                        # Plot button directly in sidebar
                        html.Button(
                            "Plot Graph",
                            id="plot-button",
                            n_clicks=0,
                            disabled=True,
                            style={
                                "backgroundColor": "#666666",
                                "color": "#999999",
                                "border": "none",
                                "padding": "12px 20px",
                                "borderRadius": "8px",
                                "cursor": "not-allowed",
                                "fontSize": "14px",
                                "fontWeight": "bold",
                                "width": "100%",
                                "marginTop": "20px",
                                "textAlign": "center"
                            }
                        ),
                    ],
                ),
                html.Div(
                    id="main-container",
                    style={"width": "80%", "padding": "20px", "backgroundColor": "#e5f6ff"},  # Adjusted width
                    children=[
                        html.Div(id="graph-input-options"),

                        # Split main container into two columns
                        html.Div([
                            # Left column: Graph
                            html.Div([
                                dcc.Graph(id='graph-output'),
                            ], style={
                                "width": "65%",
                                "display": "inline-block",
                                "verticalAlign": "top"
                            }),

                            # Right column: Customization options
                            html.Div([
                                html.Div(id="custom-options"),
                            ], style={
                                "width": "33%",
                                "display": "inline-block",
                                "verticalAlign": "top",
                                "marginLeft": "2%",
                                "backgroundColor": "#f8f9fa",
                                "borderRadius": "8px",
                                "padding": "15px",
                                "border": "1px solid #dee2e6"
                            }),
                        ], style={"marginTop": "20px"}),
                    ]
                ),
            ],
        ),
    ]
)