import re, io
import pandas as pd
import numpy as np


#round off mean
#range instead of min and max value

ALLOWED_EXTENSIONS = { 'csv', 'xlsx', 'xls'}

def data_summary(filename, file_data, if_header, if_index):
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file part in the request."}), 400

    # file = request.files['file']

    if filename == '':
        return {"error": "No file selected for uploading."}

    if file_data and allowed_file(filename):
        # if_header = request.form['header']
        # if_index = request.form['index']
        header_row, index_col = find_first_data_row(filename, file_data, if_header, if_index)
        # print(header_row, index_col)
        #file['file'][1].seek(0)
        if filename.rsplit('.', 1)[1].lower() == "csv":
            file = io.StringIO(file_data.decode('utf-8'))
            df = pd.read_csv(file,header=header_row, index_col=index_col)
        else:
            file = io.BytesIO(file_data)
            df = pd.read_excel(file, header=header_row, index_col=index_col)
        file.seek(0)
        #returns a new DataFrame where each column has been changed to the best possible data type.
        new_df = df.convert_dtypes()
        data_summary = {}
        for (col, d_type) in zip(list(df.columns), list(new_df.dtypes)):
            col_summary = column_data_summary(df[col], d_type)
            data_summary[col] = col_summary

        # Ensure datetime columns are converted to ISO format and handle NaT
        for col in new_df.select_dtypes(include=['datetime64[ns]']):
            new_df[col] = pd.to_datetime(new_df[col], errors='coerce')  # Ensure datetime format
            new_df[col] = new_df[col].apply(
                lambda x: x.isoformat() if pd.notna(x) else None)  # Convert datetime to string

        # Ensure all NaN and NaT are converted to None for JSON compatibility
        new_df = new_df.replace({np.nan: None})
        new_df = new_df.where(pd.notna(new_df), None)  # Replace any remaining NaT with None

        # Convert dataframe to dict
        data_json = new_df.to_dict("records")
        # print(new_df.head())
        def clean_data_summary(data_summary):
            cleaned_summary = {}
            for key, metrics in data_summary.items():
                cleaned_metrics = {}
                for metric, value in metrics.items():
                    try:
                        # Handle lists, arrays, and tuples
                        if isinstance(value, (list, tuple, np.ndarray)):
                            cleaned_metrics[metric] = [
                                None if pd.isna(v) or v is pd.NaT  # Handle NaN and NaT
                                else v.isoformat() if isinstance(v, pd.Timestamp)  # Convert datetime
                                else v.item() if isinstance(v, (np.int64, np.float64))  # Convert numpy numbers
                                else v
                                for v in value
                            ]
                        # Handle single NaN or NaT
                        elif pd.isna(value) or value is pd.NaT:
                            cleaned_metrics[metric] = None
                        # Convert datetime to ISO format
                        elif isinstance(value, pd.Timestamp):
                            cleaned_metrics[metric] = value.isoformat()
                        # Convert numpy numbers to native Python types
                        elif isinstance(value, (np.int64, np.float64)):
                            cleaned_metrics[metric] = value.item()
                        # Everything else
                        else:
                            cleaned_metrics[metric] = value
                    except Exception as e:
                        print(f"Error cleaning field '{metric}' in '{key}': {e}")
                        cleaned_metrics[metric] = str(value)  # Fallback to string
                cleaned_summary[key] = cleaned_metrics
            return cleaned_summary

        # Clean the data_summary
        data_summary = clean_data_summary(data_summary)

        return {"data": data_json,"data_summary": data_summary}# "data_table": data_json}) #"data": new_df.to_dict("records")


def detect_pattern(s):
    if pd.isna(s):  # Handle NaN values
        return 'NaN'
    s = re.sub(r'\d', 'D', s)  # Replace digits with 'D'
    s = re.sub(r'[a-zA-Z]', 'A', s)  # Replace letters with 'A'
    s = re.sub(r'[^\w\s]', 'S', s)  # Replace special characters with 'S'
    return s

def find_first_data_row(filename,file_data, header, indexCol):
    # Read the Excel file without treating any row as the header
    file_ext = filename.rsplit('.', 1)[1].lower()
    # print("file_ext:", file_ext)
    if file_ext == "csv":
        file = io.StringIO(file_data.decode('utf-8'))
        df = pd.read_csv(file, header=None)
        #print(df.head())
    else:
        file = io.BytesIO(file_data)
        df = pd.read_excel(file, engine="openpyxl", header=None)
    header_row=None
    indexCol_name= None
    if header:
        # Iterate through the rows to find the first non-empty row
        for i, row in df.iterrows():
            if row.notna().any():  # Check if any value in the row is not NaN
                header_row= i  # Return the row index where data starts
                break
        #print(header_row)
        file.seek(0)
        if file_ext == "csv":
            df = pd.read_csv(file, header=header_row)
        else:
            df = pd.read_excel(file, header=header_row)
    if indexCol:
        cols = df.columns
        indexCol_name = cols[0]
    return header_row, indexCol_name
    # raise ValueError("No data found in the file.")

def column_data_summary(col, d_type):
    summary = {}
    total_items = len(list(col))
    col_new = col.dropna()
    value_count = len(list(col_new))
    missing_values = total_items - value_count
    summary["Value Count"] = value_count
    summary["Missing Value Count"] = missing_values
    summary['DataTypes'] = str(d_type)
    summary["Unique Value Count"] = len(set(col))
    if len(set(col)) > 20:
        summary["Unique Values"] = list(set(col))[0:9]
    else:
        summary["Unique Values"] = list(set(col))
    mixed_types = []
    if d_type == 'object':
        types = col.apply(type).value_counts()
        for key, val in types.items():
            mixed_types.append({key:str(val)})
        summary['DataTypes'] = mixed_types
    elif d_type == 'string':
        # string_length, shortest and longest string length
        # check ifdigitsonly, isalpha, isalphanumeric, containsspecialcharacter
        pattern = col.apply(detect_pattern)
        pattern_counts = pattern.value_counts()
        patterns = []
        for key, val in pattern_counts.items():
            patterns.append({key:val})
        summary["String Patterns"] = patterns
        #print(pattern_counts)
    elif d_type in ['Int64', 'Float64']:
        summary["Mean"] = str(col.mean())
        summary["Median"] = str(col.median())
        # summary["Mode"] = col.mode()[0]
        summary["Min Value"] = str(col.min())
        summary["Max Value"] = str(col.max())
    # else: # what about datetime, timestamp, boolean, binary data
    #     print("O")
    #print(total_items,value_count, missing_values, d_type)
    return summary

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_data_for_chart(df, graph_type, x_col, y_col, z_col=None, color_col=None):
    """
    Preprocess data based on chart type requirements
    """
    df_processed = df.copy()

    # Handle missing values
    if x_col and x_col in df_processed.columns:
        df_processed = df_processed.dropna(subset=[x_col])
    if y_col and y_col in df_processed.columns:
        df_processed = df_processed.dropna(subset=[y_col])

    # Chart-specific preprocessing
    if graph_type == 'gantt':
        # Convert date columns for Gantt charts
        if y_col and z_col:
            try:
                df_processed[y_col] = pd.to_datetime(df_processed[y_col])
                df_processed[z_col] = pd.to_datetime(df_processed[z_col])
            except Exception as e:
                print(f"Date conversion error: {e}")

    elif graph_type in ['pie', 'donut', 'funnel']:
        # Aggregate duplicate categories for pie/donut charts
        if x_col and y_col:
            df_processed = df_processed.groupby(x_col)[y_col].sum().reset_index()

    elif graph_type == 'waterfall':
        # Sort by categories for waterfall
        if x_col:
            df_processed = df_processed.sort_values(by=x_col)

    elif graph_type == 'pyramid':
        # Sort by values for pyramid (ascending for proper pyramid shape)
        if y_col:
            df_processed = df_processed.sort_values(by=y_col, ascending=True)

    elif graph_type in ['radar', 'radial-line']:
        # Ensure we have enough data points for circular charts
        if len(df_processed) < 3:
            print(f"Warning: {graph_type} works best with at least 3 data points")

    return df_processed


def validate_chart_data(df, graph_type, x_col, y_col, z_col=None):
    """
    Validate if data is suitable for the selected chart type
    """
    errors = []

    if graph_type == 'gantt':
        if not z_col:
            errors.append("Gantt charts require start date, end date, and task columns")
        else:
            # Check if date columns can be converted
            try:
                pd.to_datetime(df[y_col].head())
                pd.to_datetime(df[z_col].head())
            except:
                errors.append("Gantt chart date columns must be convertible to datetime")

    elif graph_type in ['pie', 'donut']:
        if df[y_col].sum() <= 0:
            errors.append("Pie charts require positive values")

    elif graph_type == 'heatmap':
        if not z_col:
            errors.append("Heatmap requires X, Y, and Z (value) columns")

    elif graph_type in ['radar', 'radial-line', 'polar-area']:
        if len(df) < 3:
            errors.append(f"{graph_type} charts work best with at least 3 data points")

    return errors
