from dash import html, dcc,callback, Input, Output,State, html, no_update, exceptions, ALL
import base64
import dash,io
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from layouts.custom_views_page import icon_style

@callback(
    [Output("data-store", "data"),
     Output("filename-display", "children")],
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def save_data(contents, filename):
    if contents is None:
        return None, "No file uploaded"

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith('.csv'):
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(io.BytesIO(decoded))
    else:
        return None, "Unsupported file format"

    return df.to_json(date_format='iso', orient='split'), f"Uploaded: {filename}"


# ✅ Store selected graph type
@callback(
    Output('selected-graph-icon', 'data'),
    Input({'type': 'graph-icon', 'index': dash.ALL}, 'n_clicks'),
    State({'type': 'graph-icon', 'index': dash.ALL}, 'id'),
    prevent_initial_call=True
)
def store_selected_icon(n_clicks, ids):
    if not dash.callback_context.triggered:
        return dash.no_update

    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    triggered_index = eval(triggered_id)['index']
    return triggered_index


@callback(
    Output({'type': 'graph-icon', 'index': ALL}, 'style'),
    Input('selected-graph-icon', 'data'),
    State({'type': 'graph-icon', 'index': ALL}, 'id')
)
def update_icon_styles(selected_icon, all_ids):
    new_styles = []
    for icon_id in all_ids:
        is_selected = icon_id['index'] == selected_icon
        style = icon_style.copy()
        if is_selected:
            style['backgroundColor'] = '#FFFFFF'
            style['color'] = '#000000'
        new_styles.append(style)
    return new_styles


# ✅ Render dropdowns based on graph type - ALWAYS include all dropdowns but hide them
@callback(
    Output("graph-input-options", "children"),
    Input("selected-graph-icon", "data"),
    State("data-store", "data"),
    prevent_initial_call=True
)
def show_input_fields(graph_type, data_json):
    if not graph_type or not data_json:
        return html.Div("Upload data and select a graph type.")

    df = pd.read_json(data_json, orient='split')
    options = [{"label": col, "value": col} for col in df.columns]
    numeric_options = [{"label": col, "value": col} for col in df.select_dtypes(include=['number']).columns]

    # ALWAYS create all dropdowns, but hide the ones not needed
    x_dropdown = dcc.Dropdown(id="x-axis-dropdown", options=options, placeholder="Select X-axis")
    y_dropdown = dcc.Dropdown(id="y-axis-dropdown", options=numeric_options, placeholder="Select Y-axis")
    z_dropdown = dcc.Dropdown(id="z-axis-dropdown", options=numeric_options, placeholder="Select Z-axis",
                              style={"display": "none" if graph_type not in ["heatmap", "bubble"] else "block"})
    color_dropdown = dcc.Dropdown(id="color-dropdown", options=options, placeholder="Color by column (optional)",
                                  style={"display": "none" if graph_type in ["pie", "heatmap"] else "block"})
    size_dropdown = dcc.Dropdown(id="size-dropdown", options=numeric_options, placeholder="Size by column (optional)",
                                 style={"display": "none" if graph_type not in ["scatter", "bubble"] else "block"})

    # Arrange dropdowns in two rows layout with proper alignment
    all_dropdowns = [
        # First row: X-axis and Color by
        html.Div([
            html.Div([
                html.Label("X-Axis", style={
                    "marginBottom": "5px",
                    "display": "block",
                    "height": "15px"  # Fixed height for alignment
                }),
                x_dropdown,
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

            html.Div([
                html.Label("Color by (optional)", style={
                    "marginBottom": "5px",
                    "display": "block" if graph_type not in ["pie", "heatmap"] else "none",
                    "height": "15px"  # Fixed height for alignment
                }),
                color_dropdown,
            ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%", "verticalAlign": "top"}),
        ], style={"marginBottom": "15px"}),

        # Second row: Y-axis and Size by
        html.Div([
            html.Div([
                html.Label("Y-Axis", style={
                    "marginBottom": "5px",
                    "display": "block",
                    "height": "15px"  # Fixed height for alignment
                }),
                y_dropdown,
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

            html.Div([
                html.Label("Size by (optional)", style={
                    "marginBottom": "5px",
                    "display": "block" if graph_type in ["scatter", "bubble"] else "none",
                    "height": "15px"  # Fixed height for alignment
                }),
                size_dropdown,
            ], style={"width": "48%", "display": "inline-block", "marginLeft": "4%", "verticalAlign": "top"}),
        ], style={"marginBottom": "15px"}),

        # Third row: Z-axis (only for heatmap and bubble charts)
        html.Div([
            html.Div([
                html.Label("Z-Axis", style={
                    "marginBottom": "5px",
                    "display": "block" if graph_type in ["heatmap", "bubble"] else "none",
                    "height": "15px"  # Fixed height for alignment
                }),
                z_dropdown,
            ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),
        ], style={
            "marginBottom": "15px",
            "display": "block" if graph_type in ["heatmap", "bubble"] else "none"
        }),
    ]

    if graph_type in ["scatter", "line", "bar", "area", "bubble"]:
        return html.Div(all_dropdowns)

    elif graph_type in ["pie", "donut"]:
        return html.Div(all_dropdowns)

    elif graph_type == "heatmap":
        return html.Div(all_dropdowns)

    elif graph_type == "box":
        return html.Div(all_dropdowns)

    # Replace the else block in the show_input_fields callback with this:

    elif graph_type == "gantt":
        # Gantt chart needs: Task names (x), Start dates, End dates, optional Category
        return html.Div(all_dropdowns + [
            html.P("For Gantt charts: X-axis = Task names, Y-axis = Start dates, Z-axis = End dates",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])


    elif graph_type in ["radial-bar", "polar-area"]:
        # Radial/polar charts need: Categories (x) and Values (y)
        return html.Div(all_dropdowns + [
            html.P(f"For {graph_type.replace('-', ' ').title()}: X-axis = Categories, Y-axis = Values",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    elif graph_type == "stacked-bar":
        # Stacked bar needs: Categories (x), Values (y), Stack groups (color)
        return html.Div(all_dropdowns + [
            html.P("For Stacked Bar: X-axis = Categories, Y-axis = Values, Color = Stack groups",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])


    elif graph_type == "radial-line":
        # Radial line chart needs: Categories (x), Values (y), optional grouping (color)
        return html.Div(all_dropdowns + [
            html.P("For Radial Line: X-axis = Categories, Y-axis = Values, Color = Series (optional)",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    elif graph_type == "waterfall":
        # Waterfall chart needs: Categories (x), Values (y)
        return html.Div(all_dropdowns + [
            html.P("For Waterfall: X-axis = Categories, Y-axis = Values (positive/negative changes)",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    elif graph_type == "funnel":
        # Funnel chart needs: Stages (x), Values (y)
        return html.Div(all_dropdowns + [
            html.P("For Funnel: X-axis = Stages, Y-axis = Values (decreasing order)",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    elif graph_type == "radar":
        # Radar chart needs: Metrics (x), Values (y), optional Series (color)
        return html.Div(all_dropdowns + [
            html.P("For Radar: X-axis = Metrics, Y-axis = Values, Color = Series (optional)",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    elif graph_type == "pyramid":
        # Pyramid chart needs: Categories (x), Values (y)
        return html.Div(all_dropdowns + [
            html.P("For Pyramid: X-axis = Categories, Y-axis = Values (hierarchical)",
                   style={"color": "blue", "marginTop": "10px", "fontSize": "12px"})
        ])

    else:
        # Fallback for any truly unrecognized types
        return html.Div(all_dropdowns + [
            html.P(f"Graph type '{graph_type}' configuration loaded. Select appropriate columns.",
                   style={"color": "green", "marginTop": "10px", "fontSize": "12px"})
        ])

# ✅ UPDATED: Customization options now styled for main container
@callback(
    Output("custom-options", "children"),
    Input("selected-graph-icon", "data"),
    prevent_initial_call=True
)
def show_custom_options(graph_type):
    if not graph_type:
        return html.Div()

    base_style = {"color": "#333333", "fontSize": "12px", "marginBottom": "8px", "fontWeight": "500"}
    input_style = {"width": "100%", "marginBottom": "10px", "fontSize": "12px"}
    hidden_style = {"display": "none"}

    # ALL CUSTOM INPUTS - ALWAYS PRESENT BUT CONDITIONALLY HIDDEN
    all_custom_inputs = [
        html.H5("Customization Options", style={
            "color": "#007bff",
            "fontSize": "16px",
            "fontWeight": "bold",
            "marginBottom": "15px",
            "borderBottom": "2px solid #007bff",
            "paddingBottom": "5px"
        }),

        html.Label("Chart Title", style=base_style),
        dcc.Input(id="chart-title", type="text", placeholder="Enter chart title", style=input_style),

        html.Label("Primary Color", style=base_style),
        html.Div([
            dcc.Dropdown(
                id="primary-color",
                options=[
                    {"label": "🔵 Blue", "value": "#636EFA"},
                    {"label": "🔴 Red", "value": "#EF553B"},
                    {"label": "🟢 Green", "value": "#00CC96"},
                    {"label": "🟡 Yellow", "value": "#FFA15A"},
                    {"label": "🟣 Purple", "value": "#AB63FA"},
                    {"label": "🟠 Orange", "value": "#FF6692"},
                    {"label": "🟤 Brown", "value": "#B6E880"},
                    {"label": "⚫ Black", "value": "#000000"},
                    {"label": "⚪ White", "value": "#FFFFFF"},
                    {"label": "🔶 Dark Orange", "value": "#FF8C00"},
                    {"label": "🟢 Dark Green", "value": "#008000"},
                    {"label": "🔵 Navy", "value": "#000080"},
                ],
                value="#636EFA",
                style={"width": "100%", "fontSize": "12px"}
            ),
        ], style={"marginBottom": "15px"}),

        # SCATTER-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Scatter Plot Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Point Size", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "point-size"}, min=1, max=20, value=8,
                       marks={i: str(i) for i in range(1, 21, 5)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Point Symbol", style=base_style),
            dcc.Dropdown(
                id={"type": "custom-input", "id": "point-symbol"},
                options=[
                    {"label": "Circle", "value": "circle"},
                    {"label": "Square", "value": "square"},
                    {"label": "Diamond", "value": "diamond"},
                    {"label": "Cross", "value": "cross"},
                    {"label": "X", "value": "x"},
                    {"label": "Triangle Up", "value": "triangle-up"},
                    {"label": "Triangle Down", "value": "triangle-down"},
                    {"label": "Star", "value": "star"},
                ],
                value="circle",
                style=input_style
            ),

            html.Label("Opacity", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "opacity"}, min=0.1, max=1.0, value=0.8, step=0.1,
                       marks={i / 10: f"{i / 10:.1f}" for i in range(1, 11, 2)},
                       tooltip={"placement": "bottom", "always_visible": True}),
        ], style=hidden_style if graph_type != "scatter" else {}),

        # LINE-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Line Chart Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Line Width", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "line-width"}, min=1, max=10, value=2,
                       marks={i: str(i) for i in range(1, 11, 2)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Line Style", style=base_style),
            dcc.Dropdown(
                id={"type": "custom-input", "id": "line-style"},
                options=[
                    {"label": "Solid", "value": "solid"},
                    {"label": "Dash", "value": "dash"},
                    {"label": "Dot", "value": "dot"},
                    {"label": "Dash Dot", "value": "dashdot"},
                ],
                value="solid",
                style=input_style
            ),

            html.Label("Show Markers", style=base_style),
            dcc.Checklist(
                id={"type": "custom-input", "id": "show-markers"},
                options=[{"label": " Enable markers", "value": True}],
                value=[],
                style={"color": "#333333"}
            ),
        ], style=hidden_style if graph_type != "line" else {}),

        # BAR-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Bar Chart Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Bar Orientation", style=base_style),
            dcc.RadioItems(
                id={"type": "custom-input", "id": "bar-orientation"},
                options=[
                    {"label": " Vertical", "value": "vertical"},
                    {"label": " Horizontal", "value": "horizontal"},
                ],
                value="vertical",
                style={"color": "#333333"},
                labelStyle={"display": "block", "marginBottom": "5px"}
            ),

            html.Label("Bar Opacity", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "bar-opacity"}, min=0.1, max=1.0, value=0.8, step=0.1,
                       marks={i / 10: f"{i / 10:.1f}" for i in range(1, 11, 3)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Show Text on Bars", style=base_style),
            dcc.Checklist(
                id={"type": "custom-input", "id": "show-text"},
                options=[{"label": " Show values", "value": True}],
                value=[],
                style={"color": "#333333"}
            ),
        ], style=hidden_style if graph_type != "bar" else {}),

        # PIE/DONUT-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Pie Chart Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Hole Size (for donut)", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "hole-size"}, min=0, max=0.8,
                       value=0.3 if graph_type == "donut" else 0, step=0.1,
                       marks={i / 10: f"{int(i * 10)}%" for i in range(0, 9, 2)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Show Labels", style=base_style),
            dcc.Checklist(
                id={"type": "custom-input", "id": "show-labels"},
                options=[{"label": " Show slice labels", "value": True}],
                value=[True],
                style={"color": "#333333"}
            ),

            html.Label("Show Values", style=base_style),
            dcc.Checklist(
                id={"type": "custom-input", "id": "show-values"},
                options=[{"label": " Show slice values", "value": True}],
                value=[True],
                style={"color": "#333333"}
            ),
        ], style=hidden_style if graph_type not in ["pie", "donut"] else {}),

        # HEATMAP-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Heatmap Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Color Scale", style=base_style),
            dcc.Dropdown(
                id={"type": "custom-input", "id": "color-scale"},
                options=[
                    {"label": "Viridis", "value": "Viridis"},
                    {"label": "Plasma", "value": "Plasma"},
                    {"label": "Inferno", "value": "Inferno"},
                    {"label": "Magma", "value": "Magma"},
                    {"label": "Blues", "value": "Blues"},
                    {"label": "Reds", "value": "Reds"},
                    {"label": "Greens", "value": "Greens"},
                    {"label": "RdYlBu", "value": "RdYlBu"},
                ],
                value="Viridis",
                style=input_style
            ),

            html.Label("Show Color Bar", style=base_style),
            dcc.Checklist(
                id={"type": "custom-input", "id": "show-colorbar"},
                options=[{"label": " Show color scale", "value": True}],
                value=[True],
                style={"color": "#333333"}
            ),
        ], style=hidden_style if graph_type != "heatmap" else {}),

        # AREA-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Area Chart Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Fill Opacity", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "fill-opacity"}, min=0.1, max=1.0, value=0.6, step=0.1,
                       marks={i / 10: f"{i / 10:.1f}" for i in range(1, 11, 3)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Line Width", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "area-line-width"}, min=0, max=5, value=1,
                       marks={i: str(i) for i in range(0, 6)},
                       tooltip={"placement": "bottom", "always_visible": True}),
        ], style=hidden_style if graph_type != "area" else {}),

        # BOX-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Box Plot Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Box Points", style=base_style),
            dcc.Dropdown(
                id={"type": "custom-input", "id": "box-points"},
                options=[
                    {"label": "None", "value": False},
                    {"label": "Outliers Only", "value": "outliers"},
                    {"label": "Suspected Outliers", "value": "suspectedoutliers"},
                    {"label": "All Points", "value": "all"},
                ],
                value="outliers",
                style=input_style
            ),

            html.Label("Box Opacity", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "box-opacity"}, min=0.1, max=1.0, value=0.8, step=0.1,
                       marks={i / 10: f"{i / 10:.1f}" for i in range(1, 11, 3)},
                       tooltip={"placement": "bottom", "always_visible": True}),
        ], style=hidden_style if graph_type != "box" else {}),

        # BUBBLE-SPECIFIC OPTIONS
        html.Div([
            html.Hr(style={"borderColor": "#dee2e6", "margin": "15px 0"}),
            html.H6("Bubble Chart Options", style={"color": "#495057", "marginBottom": "10px"}),

            html.Label("Max Bubble Size", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "max-bubble-size"}, min=10, max=100, value=50, step=5,
                       marks={i: str(i) for i in range(10, 101, 20)},
                       tooltip={"placement": "bottom", "always_visible": True}),

            html.Label("Bubble Opacity", style=base_style),
            dcc.Slider(id={"type": "custom-input", "id": "bubble-opacity"}, min=0.1, max=1.0, value=0.7, step=0.1,
                       marks={i / 10: f"{i / 10:.1f}" for i in range(1, 11, 3)},
                       tooltip={"placement": "bottom", "always_visible": True}),
        ], style=hidden_style if graph_type != "bubble" else {}),
    ]

    return html.Div(all_custom_inputs)


# ✅ Callback to create initial placeholder when graph type is selected
@callback(
    Output('graph-output', 'figure'),
    Input("selected-graph-icon", "data"),
    State("data-store", "data"),
    prevent_initial_call=True
)
def create_placeholder_graph(graph_type, data_json):
    """Create placeholder graph when graph type is selected"""
    # if not graph_type or not data_json:
    #     raise exceptions.PreventUpdate

    if not graph_type:
        raise exceptions.PreventUpdate

    if not data_json:
        # Return empty figure instead of raising PreventUpdate
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Please upload data first",
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        return empty_fig

    df = pd.read_json(data_json, orient='split')

    # Create empty placeholder figure
    fig = px.scatter(df.head(0), x=df.columns[0], y=df.columns[1])

    if graph_type == "heatmap":
        fig.update_layout(title="Select X, Y, and Z columns for Heatmap Chart")
    else:
        fig.update_layout(title=f"Select columns for {graph_type.title()} Chart")

    return fig


# Callback to enable/disable plot button based on data and graph type
@callback(
    [Output("plot-button", "disabled"),
     Output("plot-button", "style")],
    [Input("data-store", "data"),
     Input("selected-graph-icon", "data")],
    prevent_initial_call=True
)
def update_plot_button(data_json, graph_type):
    base_style = {
        "border": "none",
        "padding": "12px 20px",
        "borderRadius": "8px",
        "cursor": "pointer",
        "fontSize": "14px",
        "fontWeight": "bold",
        "width": "100%",
        "marginTop": "20px",
        "textAlign": "center"
    }

    if data_json and graph_type:
        # Enable button - data uploaded and graph type selected
        style = base_style.copy()
        style.update({
            "backgroundColor": "#00ADB5",
            "color": "white",
        })
        return False, style
    else:
        # Disable button - missing data or graph type
        style = base_style.copy()
        style.update({
            "backgroundColor": "#666666",
            "color": "#999999",
            "cursor": "not-allowed"
        })
        return True, style


# ✅ Enhanced callback that creates graphs with custom options - FIXED to handle missing states
@callback(
    [Output('graph-output', 'figure', allow_duplicate=True),
    Output('validation-message', 'children')],
    Input("plot-button", "n_clicks"),
    State("x-axis-dropdown", "value"),
    State("y-axis-dropdown", "value"),
    State("z-axis-dropdown", "value"),
    State("color-dropdown", "value"),
    State("size-dropdown", "value"),
    State("selected-graph-icon", "data"),
    State("data-store", "data"),
    # Common options as State
    State("chart-title", "value"),
    State("primary-color", "value"),
    # All custom options as State - will handle None values gracefully
    State({"type": "custom-input", "id": "point-size"}, "value"),
    State({"type": "custom-input", "id": "point-symbol"}, "value"),
    State({"type": "custom-input", "id": "opacity"}, "value"),
    State({"type": "custom-input", "id": "line-width"}, "value"),
    State({"type": "custom-input", "id": "line-style"}, "value"),
    State({"type": "custom-input", "id": "show-markers"}, "value"),
    State({"type": "custom-input", "id": "bar-orientation"}, "value"),
    State({"type": "custom-input", "id": "bar-opacity"}, "value"),
    State({"type": "custom-input", "id": "show-text"}, "value"),
    State({"type": "custom-input", "id": "hole-size"}, "value"),
    State({"type": "custom-input", "id": "show-labels"}, "value"),
    State({"type": "custom-input", "id": "show-values"}, "value"),
    State({"type": "custom-input", "id": "color-scale"}, "value"),
    State({"type": "custom-input", "id": "show-colorbar"}, "value"),
    State({"type": "custom-input", "id": "fill-opacity"}, "value"),
    State({"type": "custom-input", "id": "area-line-width"}, "value"),
    State({"type": "custom-input", "id": "box-points"}, "value"),
    State({"type": "custom-input", "id": "box-opacity"}, "value"),
    State({"type": "custom-input", "id": "max-bubble-size"}, "value"),
    State({"type": "custom-input", "id": "bubble-opacity"}, "value"),
    prevent_initial_call=True
)
def update_graph_with_custom_options(n_clicks, x_col, y_col, z_col, color_col, size_col,
                                     graph_type, data_json, chart_title, primary_color,
                                     point_size, point_symbol, opacity,
                                     line_width, line_style, show_markers,
                                     bar_orientation, bar_opacity, show_text,
                                     hole_size, show_labels, show_values,
                                     color_scale, show_colorbar,
                                     fill_opacity, area_line_width,
                                     box_points, box_opacity,
                                     max_bubble_size, bubble_opacity):
    """Update graph when plot button is clicked - handles None values for custom options"""
    # if not n_clicks or not graph_type or not data_json:
    #     raise exceptions.PreventUpdate

    # Better initial checks
    if not n_clicks or n_clicks == 0:
        raise exceptions.PreventUpdate

    if not graph_type or not data_json:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="Missing data or graph type")
        return empty_fig, "Please select graph type and upload data"


    df = pd.read_json(data_json, orient='split')

    # Check required inputs for different graph types
    # if graph_type == "heatmap":
    #     if not x_col or not y_col or not z_col:
    #         raise exceptions.PreventUpdate
    # elif graph_type in ["pie", "donut"]:
    #     if not x_col or not y_col:
    #         raise exceptions.PreventUpdate
    # else:
    #     if not x_col or not y_col:
    #         raise exceptions.PreventUpdate

    # Validation rules
    missing_fields = []
    if graph_type == "heatmap":
        if not x_col: missing_fields.append("X-axis *")
        if not y_col: missing_fields.append("Y-axis *")
        if not z_col: missing_fields.append("Z-axis *")
    elif graph_type in ["pie", "donut"]:
        if not x_col: missing_fields.append("Name column *")
        if not y_col: missing_fields.append("Value column *")
    else:
        if not x_col: missing_fields.append("X-axis *")
        if not y_col: missing_fields.append("Y-axis *")

    if missing_fields:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            title="Please fill required fields before plotting",
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        return empty_fig, f"Please select: {', '.join(missing_fields)}."

    # Set default values for None inputs
    chart_title = chart_title or f"{graph_type.title()} Chart"
    primary_color = primary_color or "#636EFA"

    # Create the appropriate graph with customization
    if graph_type == 'scatter':
        fig = px.scatter(df, x=x_col, y=y_col,
                         color=color_col if color_col else None,
                         size=size_col if size_col else None,
                         color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply scatter-specific customizations (only if values exist)
        if point_size or point_symbol or opacity:
            marker_dict = {}
            if point_size is not None:
                marker_dict['size'] = point_size
            if point_symbol is not None:
                marker_dict['symbol'] = point_symbol
            if opacity is not None:
                marker_dict['opacity'] = opacity
            marker_dict['line'] = dict(width=1, color='white')

            fig.update_traces(marker=marker_dict)

    elif graph_type == 'line':
        fig = px.line(df, x=x_col, y=y_col,
                      color=color_col if color_col else None,
                      color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply line-specific customizations
        line_dict = {}
        if line_width is not None:
            line_dict['width'] = line_width
        if line_style is not None:
            line_dict['dash'] = line_style

        if show_markers and True in show_markers:
            fig.update_traces(mode='lines+markers', line=line_dict)
        else:
            fig.update_traces(mode='lines', line=line_dict)

    elif graph_type == 'bar':
        if bar_orientation == 'horizontal':
            fig = px.bar(df, x=y_col, y=x_col,
                         color=color_col if color_col else None,
                         color_discrete_sequence=[primary_color] if not color_col else None,
                         orientation='h')
        else:
            fig = px.bar(df, x=x_col, y=y_col,
                         color=color_col if color_col else None,
                         color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply bar-specific customizations
        if bar_opacity is not None:
            fig.update_traces(opacity=bar_opacity)

        if show_text and True in show_text:
            fig.update_traces(texttemplate='%{y}', textposition='outside')

    elif graph_type == 'area':
        fig = px.area(df, x=x_col, y=y_col,
                      color=color_col if color_col else None,
                      color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply area-specific customizations
        area_dict = {
            'fill': 'tonexty',
            'fillcolor': primary_color,
        }
        if fill_opacity is not None:
            area_dict['opacity'] = fill_opacity

        line_dict = {}
        if area_line_width is not None:
            line_dict['width'] = area_line_width

        fig.update_traces(**area_dict, line=line_dict)

    elif graph_type in ['pie', 'donut']:
        fig = px.pie(df, names=x_col, values=y_col,
                     color_discrete_sequence=px.colors.qualitative.Set3)

        # Apply pie-specific customizations
        textinfo = []
        if show_labels and True in show_labels:
            textinfo.append('label')
        if show_values and True in show_values:
            textinfo.append('value')

        trace_dict = {}
        if hole_size is not None:
            trace_dict['hole'] = hole_size
        if textinfo:
            trace_dict['textinfo'] = '+'.join(textinfo)
        else:
            trace_dict['textinfo'] = 'none'

        fig.update_traces(**trace_dict)

    elif graph_type == 'heatmap':
        fig = px.density_heatmap(df, x=x_col, y=y_col, z=z_col,
                                 histfunc="avg",
                                 color_continuous_scale=color_scale or "Viridis")

        # Apply heatmap-specific customizations
        if show_colorbar is not None and True not in show_colorbar:
            fig.update_layout(coloraxis_showscale=False)

    elif graph_type == 'box':
        fig = px.box(df, x=x_col, y=y_col,
                     color=color_col if color_col else None,
                     color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply box-specific customizations
        trace_dict = {}
        if box_points is not None:
            trace_dict['boxpoints'] = box_points if box_points is not False else False
        if box_opacity is not None:
            trace_dict['opacity'] = box_opacity

        fig.update_traces(**trace_dict)

    elif graph_type == 'bubble':
        fig = px.scatter(df, x=x_col, y=y_col,
                         size=z_col if z_col else size_col,
                         color=color_col if color_col else None,
                         size_max=max_bubble_size or 50,
                         color_discrete_sequence=[primary_color] if not color_col else None)

        # Apply bubble-specific customizations
        if bubble_opacity is not None:
            fig.update_traces(opacity=bubble_opacity)

    elif graph_type == 'gantt':
        # Gantt chart using Plotly's timeline
        if not x_col or not y_col or not z_col:
            fig = go.Figure()
            fig.update_layout(title="Gantt Chart requires Task, Start Date, and End Date columns")
        else:
            # Convert date columns if they're strings
            df_gantt = df.copy()
            try:
                df_gantt[y_col] = pd.to_datetime(df_gantt[y_col])
                df_gantt[z_col] = pd.to_datetime(df_gantt[z_col])
            except:
                pass

            fig = px.timeline(df_gantt, x_start=y_col, x_end=z_col, y=x_col,
                              color=color_col if color_col else None,
                              color_discrete_sequence=[primary_color] if not color_col else None)
            fig.update_yaxes(autorange="reversed")  # Tasks from top to bottom

    elif graph_type == 'waterfall':
        # Waterfall chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Waterfall Chart requires Category and Value columns")
        else:
            values = df[y_col].tolist()
            categories = df[x_col].tolist()

            # Calculate cumulative values for waterfall effect
            cumulative = [0]
            for i, val in enumerate(values):
                cumulative.append(cumulative[-1] + val)

            fig = go.Figure(go.Waterfall(
                name="Waterfall",
                orientation="v",
                measure=["relative"] * len(values),
                x=categories,
                textposition="outside",
                text=[f"{val:+.1f}" for val in values],
                y=values,
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))

    elif graph_type == 'funnel':
        # Funnel chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Funnel Chart requires Stage and Value columns")
        else:
            fig = go.Figure(go.Funnel(
                y=df[x_col],
                x=df[y_col],
                textinfo="value+percent initial",
                marker_color=primary_color,
                connector={"line": {"color": primary_color, "dash": "dot", "width": 3}}
            ))

    elif graph_type == 'pyramid':
        # Pyramid chart (inverted funnel)
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Pyramid Chart requires Category and Value columns")
        else:
            # Sort data by values (largest at bottom)
            df_sorted = df.sort_values(by=y_col, ascending=True)
            fig = go.Figure(go.Funnel(
                y=df_sorted[x_col],
                x=df_sorted[y_col],
                textinfo="value+percent initial",
                marker_color=primary_color,
            ))
            fig.update_layout(funnelmode="stack")

    elif graph_type == 'radar':
        # Radar/Spider chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Radar Chart requires Metrics and Values columns")
        else:
            if color_col and color_col in df.columns:
                # Multiple series radar chart
                fig = go.Figure()
                for series in df[color_col].unique():
                    series_data = df[df[color_col] == series]
                    fig.add_trace(go.Scatterpolar(
                        r=series_data[y_col],
                        theta=series_data[x_col],
                        fill='toself',
                        name=str(series),
                        line_color=primary_color if len(df[color_col].unique()) == 1 else None
                    ))
            else:
                # Single series radar chart
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=df[y_col],
                    theta=df[x_col],
                    fill='toself',
                    name='Values',
                    line_color=primary_color
                ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, df[y_col].max() * 1.1])
                )
            )

    elif graph_type == 'stacked-bar':
        # Stacked bar chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Stacked Bar Chart requires Category, Value, and Stack Group columns")
        else:
            if color_col:
                # Group by x_col and color_col, sum y_col values
                pivot_df = df.pivot_table(index=x_col, columns=color_col, values=y_col,
                                          aggfunc='sum', fill_value=0)
                fig = go.Figure()

                for col in pivot_df.columns:
                    fig.add_trace(go.Bar(
                        name=str(col),
                        x=pivot_df.index,
                        y=pivot_df[col],
                    ))
                fig.update_layout(barmode='stack')
            else:
                # Regular bar chart if no color grouping
                fig = px.bar(df, x=x_col, y=y_col, color_discrete_sequence=[primary_color])

    elif graph_type == 'donut':
        # Donut chart (handled in pie section but adding specific case)
        fig = px.pie(df, names=x_col, values=y_col,
                     color_discrete_sequence=px.colors.qualitative.Set3,
                     hole=0.4)  # Makes it a donut

        # Apply donut-specific customizations
        textinfo = []
        if show_labels and True in show_labels:
            textinfo.append('label')
        if show_values and True in show_values:
            textinfo.append('value')

        trace_dict = {'hole': hole_size or 0.4}
        if textinfo:
            trace_dict['textinfo'] = '+'.join(textinfo)
        else:
            trace_dict['textinfo'] = 'none'

        fig.update_traces(**trace_dict)

    elif graph_type == 'radial-bar':
        # Radial bar chart using polar coordinates
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Radial Bar Chart requires Category and Value columns")
        else:
            fig = go.Figure()
            fig.add_trace(go.Barpolar(
                r=df[y_col],
                theta=df[x_col],
                name='Radial Bars',
                marker_color=primary_color,
                opacity=0.8
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(tickfont_size=10),
                    angularaxis=dict(tickfont_size=10)
                )
            )

    elif graph_type == 'polar-area':
        # Polar area chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Polar Area Chart requires Category and Value columns")
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=df[y_col],
                theta=df[x_col],
                mode='markers',
                marker=dict(
                    size=df[y_col] * 2,  # Scale marker size by values
                    color=primary_color,
                    opacity=0.7
                ),
                name='Polar Area'
            ))

    elif graph_type == 'radial-line':
        # Radial line chart
        if not x_col or not y_col:
            fig = go.Figure()
            fig.update_layout(title="Radial Line Chart requires Category and Value columns")
        else:
            if color_col and color_col in df.columns:
                # Multiple series
                fig = go.Figure()
                for series in df[color_col].unique():
                    series_data = df[df[color_col] == series]
                    fig.add_trace(go.Scatterpolar(
                        r=series_data[y_col],
                        theta=series_data[x_col],
                        mode='lines+markers',
                        name=str(series)
                    ))
            else:
                # Single series
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=df[y_col],
                    theta=df[x_col],
                    mode='lines+markers',
                    name='Radial Line',
                    line_color=primary_color
                ))

    else:
        # Final fallback for truly unrecognized types
        fig = px.scatter(df, x=x_col, y=y_col,
                         color=color_col if color_col else None,
                         size=size_col if size_col else None,
                         color_discrete_sequence=[primary_color] if not color_col else None)
        fig.update_layout(title=f"'{graph_type}' chart type - showing as scatter plot")

    # else:
    #     # Fallback for unimplemented types
    #     fig = px.scatter(df, x=x_col, y=y_col,
    #                      color=color_col if color_col else None,
    #                      color_discrete_sequence=[primary_color] if not color_col else None)

    # Apply common layout customizations
    fig.update_layout(
        title=chart_title,
        title_font_size=16,
        title_x=0.5,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        transition_duration=300,
        height=400,  # Smaller graph height
        margin=dict(l=60, r=60, t=80, b=60)  # Compact margins
    )

    # Update axes styling with visible lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,  # Show x-axis line
        linewidth=2,  # Make axis line thicker
        linecolor='black',  # Black axis line
        mirror=True  # Show line on both sides
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,  # Show y-axis line
        linewidth=2,  # Make axis line thicker
        linecolor='black',  # Black axis line
        mirror=True  # Show line on both sides
    )

    return fig, " "
