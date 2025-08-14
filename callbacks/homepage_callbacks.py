from dash import callback, Input, Output,State, html, no_update
from layouts.homepage import create_layout
from layouts.preprocessing_page import preprocessing_layout
from layouts.custom_views_page import custom_views_layout
from layouts.ml_page import ml_layout
import dash
from dash.dash_table import DataTable
import pandas as pd
import base64, requests
# from helper_funcs import data_summary
import helper_funcs


# print(data_summary)
# print(type(data_summary))

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    print(f"Current page: {pathname}")
    if pathname == "/customize_views":
        print("Loading customize views layout")
        return custom_views_layout
    elif pathname == "/preprocessing":
        return preprocessing_layout
    elif pathname == "/ml_models":
        return ml_layout()
    return create_layout()

# Callback for displaying filename (only on home page)
@callback(
    Output("file-name-display", "children", allow_duplicate=True),
    [Input("file-upload", "filename")],
    [State("url", "pathname")],
    prevent_initial_call=True
)
def display_filename(filename, pathname):
    if pathname != "/":
        raise dash.exceptions.PreventUpdate

    if filename:
        return f"Selected File: {filename}"
    return "No file uploaded"

# Home page callback (file upload and submit processing)
@callback(
    [
        Output("file-name-display", "children", allow_duplicate=True),
        Output("data-viewer", "children"),
        Output("data-summary", "children"),
        Output("shared-data", "data"),
    ],
    [
        Input("submit-button", "n_clicks")
    ],
    [
        State("file-upload", "contents"),
        State("file-upload", "filename"),
        State("header-dropdown", "value"),
        State("index-column-dropdown", "value"),
        State("url", "pathname")
    ],
    prevent_initial_call=True
)
def process_file_upload(n_clicks, file_content, filename, header, index_column, pathname):
    if pathname != "/":
        raise dash.exceptions.PreventUpdate

    if not n_clicks or not file_content or not filename:
        return "Please select a file", no_update, no_update, no_update

    try:
        content_type, content_string = file_content.split(",")
        file_data = base64.b64decode(content_string)

        # files = {"file": (filename_state, file_data)}
        # form_data = {"header": header, "index": index_column}
        # response = requests.post("http://127.0.0.1:5000/datasummary", files=files, data=form_data, timeout=10)
        response = helper_funcs.data_summary(filename,file_data, header, index_column)
        # print(response)
        print(type(response))
        if response:
            print("ok")
            data_table = response["data"]
            if data_table and isinstance(data_table, list):
                df = pd.DataFrame(data_table)
                data_table_component = DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns]
                )
            else:
                data_table_component = html.Div("No data table available")

            data_summary = response.get("data_summary", {})
            #print("Data Summary:", data_summary)
            summary_components = []
            for col, metrics in data_summary.items():
                cleaned_metrics = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v for k, v in
                                   metrics.items()}
                df_summary = pd.DataFrame.from_dict(cleaned_metrics, orient="index", columns=["Value"]).reset_index()
                df_summary.rename(columns={"index": col}, inplace=True)

                summary_table = DataTable(
                    data=df_summary.to_dict("records"),
                    columns=[{"name": i, "id": i} for i in df_summary.columns],
                    # Cell styling
                    style_cell={
                        "textAlign": "left",
                        "whiteSpace": "normal",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "minWidth": "150px",  # Default column width
                        "maxWidth": "150px",
                        "width": "150px",
                        "padding": "8px"
                    },
                    style_header={
                        "backgroundColor": "#c2d7e0",  # Custom background color
                        "color": "#4a4a4a",  # Custom text color
                        "fontWeight": "bold",  # Bold text
                        "textAlign": "left"  # Optional: Center-align headers
                    },

                    # Styling for the first (index) column
                    style_data_conditional=[
                        {
                            "if": {"column_id": df_summary.columns[0]},  # First column
                            "fontWeight": "bold",
                            "minWidth": "30%",  # 40% width
                            "maxWidth": "40%",
                            "width": "35%"
                        },
                        {
                            "if": {"column_id": df_summary.columns[1]},  # Second column
                            "minWidth": "60%",  # 60% width
                            "maxWidth": "70%",
                            "width": "65%"
                        },
                    ],

                    style_table={
                        "width": "100%",
                        "overflowX": "auto"
                    }
                )
                summary_components.append(summary_table)

            shared_data = {
                "data": response.get("data"),
                "data_summary": data_summary
            }

            return f"Selected File: {filename}", data_table_component, html.Div(summary_components), shared_data

        else:
            return f"Error {response.status_code}: {response.text}", no_update, no_update, no_update

    except Exception as e:
        return f"Error: {e}", no_update, no_update, no_update