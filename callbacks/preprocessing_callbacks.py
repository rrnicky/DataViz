from dash import callback, Dash, html, dcc, Input, Output, State, ctx, dash_table, dash
import base64, io, re
from sklearn.preprocessing import (LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler, RobustScaler,
                                   FunctionTransformer, PowerTransformer,)
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from gensim.models import Word2Vec
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

@callback(
    Output("preprocessing-summary", "children"),
    Output("column-selector", "options"),
    Output("df-original", "data"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_output(contents, filename):
    if contents is None:
        return "Upload a CSV/XLSX file to begin preprocessing.", [], []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return "Unsupported file format.", [], []
    except Exception as e:
        return f"There was an error processing the file: {e}", [], []
    # df_store
    # df_store['df'] = df.copy()
    df.columns = df.columns.astype(str)
    columns_data = [{"name": str(i), "id": str(i)} for i in list(df.columns)]
    table = dash_table.DataTable(
        id="preview-table",
        columns=columns_data,
        data=df.head(10).to_dict("records"),
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "#f1f1f1", "fontWeight": "bold"}
    )
    return html.Div([
        html.H4("Preview of Uploaded Data"),
        table,
        html.P(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    ]), [{"label": col, "value": col} for col in df.columns], df.to_dict("records")

@callback(
    Output("preprocessing-message", "children"),
    Output("preview-table", "data"),
    Output("preview-table", "columns"),
    Output("df-preprocessed", "data"),
    Input('apply-button', 'n_clicks'),
    State('column-selector', 'value'),
    State('missing-handler', 'value'),
    State('fill-const', 'value'),
    State('encoding-type', 'value'),
    State('custom-mapping', 'value'),
    State('scaling-options', 'value'),
    State('datetime-options', 'value'),
    State('basic-text-cleaning', 'value'),
    State('text-normalization', 'value'),
    State('vectorization-method', 'value'),
    State('drop-dups', 'value'),
    State('drop-nulls', 'value'),
    State('drop-null-columns', 'value'),
    State('filter-rows', 'value'),
    State('filter-cond', 'value'),
    State('sort-col', 'value'),
    State('sort-order', 'value'),
    State('add-col-name', 'value'),
    State('add-col-formula', 'value'),
    #outlier handling
    State('outlier-method', 'value'),
    State('outlier-action', 'value'),
    #other processing
    State('dtype-action', 'value'),
    State('change-dtype', 'value'),
    State('set-index', 'value'),
    State('rename-cols', 'value'),
    State('rename-input', 'value'),
    State('reorder-cols', 'value'),
    State('reorder-input', 'value'),
    State("df-original", "data"),
    prevent_initial_call=True
)
def apply_preprocessing(n_clicks, columns, missing_handler, fill_const, encoding, custom_map,
                        scaling, datetime_opts, text_opts, text_norm, text_vector,drop_dups
                        , null_drop_cond, null_drop_cols, filter_rows, filter_cond,
                        sort_col, sort_order, add_col_name, add_col_formula, outlier_method, outlier_action,
                        dtype_action, changed_dtype,index_col, rename_cols, rename_input,  reorder_cols,
                        reorder_input, df_store):

    # try:
    df = pd.DataFrame(df_store)
    df_copy = df.copy()

    if columns:
        #print(columns)
        if missing_handler == 'drop':
            df_copy = df_copy.dropna(subset=columns)
        for col in columns:
            if missing_handler == 'mean':
                df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
            elif missing_handler == 'median':
                df_copy[col] = df_copy[col].fillna(df_copy[col].median())
            elif missing_handler == 'mode':
                df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
            elif missing_handler == 'constant' and fill_const is not None:
                df_copy[col] = df_copy[col].fillna(fill_const)

            if encoding == "label":
                df_copy[col] = df_copy[col].astype('category').cat.codes
            elif encoding == "onehot":
                df_copy = pd.get_dummies(df_copy, columns=[col])
            elif encoding == "binary":
                df_copy[col] = df_copy[col].apply(lambda x: 1 if x else 0)
            elif encoding == "custom" and custom_map:
                mapping = eval(custom_map)
                df_copy[col] = df_copy[col].map(mapping)

            if scaling == "minmax":
                df_copy[col] = MinMaxScaler().fit_transform(df_copy[[col]])
            elif scaling == "zscore":
                df_copy[col] = StandardScaler().fit_transform(df_copy[[col]])
            elif scaling == "robust":
                df_copy[col] = RobustScaler().fit_transform(df_copy[[col]])
            elif scaling == "log":
                    # Add 1 to avoid log(0); only apply to positive values
                df_copy[col] = np.log1p(df_copy[col])
            elif scaling == "power":
                df_copy[col] = PowerTransformer(method='yeo-johnson').fit_transform(df_copy[[col]])

            if datetime_opts:
                if "convert" in datetime_opts:
                    df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
                if "year" in datetime_opts:
                    df_copy[col + "_year"] = df_copy[col].dt.year
                if "month" in datetime_opts:
                    df_copy[col + "_month"] = df_copy[col].dt.month
                if "day" in datetime_opts:
                    df_copy[col + "_day"] = df_copy[col].dt.day
                if "hour" in datetime_opts:
                    df_copy[col + "_hour"] = df_copy[col].dt.hour

            if text_opts:
                df_copy[col] = df_copy[col].astype(str)
                if "lower" in text_opts:
                    df_copy[col] = df_copy[col].str.lower()
                if "punct" in text_opts:
                    df_copy[col] = df_copy[col].astype(str).str.replace(r'[^\w\s]', '', regex=True)
                if "numbers" in text_opts:
                    df_copy[col] = df_copy[col].astype(str).str.replace(r'\d+', '', regex=True)
                if "strip" in text_opts:
                    df_copy[col] = df_copy[col].str.strip()
                if "stopwords" in text_opts:
                    stop_words = set(stopwords.words("english"))
                    df_copy[col] = df_copy[col].apply(
                        lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

                if "frequent" in text_opts:
                    all_words = ' '.join(df_copy[col].dropna().values).split()
                    word_freq = pd.Series(all_words).value_counts()
                    common_words = set(word_freq.head(10).index)  # Top 10 frequent words
                    df_copy[col] = df_copy[col].apply(
                        lambda x: ' '.join([word for word in x.split() if word not in common_words])
                        if isinstance(x, str) else x
                    )
                if "rare" in text_opts:
                    all_words = ' '.join(df_copy[col].dropna().values).split()
                    word_freq = pd.Series(all_words).value_counts()
                    rare_words = set(word_freq[word_freq == 1].index)  # Words appearing only once
                    df_copy[col] = df_copy[col].apply(
                        lambda x: ' '.join([word for word in x.split() if word not in rare_words])
                        if isinstance(x, str) else x
                    )
                if "tokenize" in text_opts:
                    df_copy[col] = df_copy[col].apply(lambda x: re.findall(r'\b\w+\b', x))
            if text_norm:
                if "stemming" in text_norm:
                    stemmer = PorterStemmer()
                    df_copy[col] = df_copy[col].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))
                if "lemmatization" in text_norm:
                    lemmatizer = WordNetLemmatizer()
                    df_copy[col] = df_copy[col].apply(
                        lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
            if text_vector:
                if text_vector == "bow":
                    vectorizer = CountVectorizer()
                    vectors = vectorizer.fit_transform(df_copy[col].astype(str).fillna(""))
                    bow_df = pd.DataFrame(vectors.toarray(),
                                          columns=[f"{col}_bow_" + feat for feat in vectorizer.get_feature_names_out()])
                    df_copy = pd.concat([df_copy.drop(columns=[col]), bow_df], axis=1)

                elif text_vector == "tfidf":
                    vectorizer = TfidfVectorizer()
                    vectors = vectorizer.fit_transform(df_copy[col].astype(str).fillna(""))
                    tfidf_df = pd.DataFrame(vectors.toarray(), columns=[f"{col}_tfidf_" + feat for feat in
                                                                        vectorizer.get_feature_names_out()])
                    df_copy = pd.concat([df_copy.drop(columns=[col]), tfidf_df], axis=1)
                if text_vector == "word2vec":
                    tokenized = df_copy[col].astype(str).fillna("").apply(lambda x: x.split())
                    model = Word2Vec(sentences=tokenized, vector_size=100, window=5, min_count=1, workers=4)

                    def get_vector(tokens):
                        vectors = [model.wv[word] for word in tokens if word in model.wv]
                        return np.mean(vectors, axis=0) if vectors else np.zeros(100)

                    word2vec_features = tokenized.apply(get_vector)
                    word2vec_df = pd.DataFrame(word2vec_features.tolist(),
                                               columns=[f"{col}_w2v_{i}" for i in range(100)])
                    df_copy = pd.concat([df_copy.drop(columns=[col]), word2vec_df], axis=1)
                elif text_vector == "glove":
                    # Load GloVe embeddings only once (cache if possible)
                    glove_path = 'glove.6B.100d.txt'  # Path to your downloaded GloVe file
                    embeddings_index = {}
                    with open(glove_path, encoding='utf-8') as f:
                        for line in f:
                            values = line.split()
                            word = values[0]
                            coefs = np.asarray(values[1:], dtype='float32')
                            embeddings_index[word] = coefs

                    tokenized = df_copy[col].astype(str).fillna("").apply(lambda x: x.split())
                    def get_glove_vector(tokens):
                        vectors = [embeddings_index[word] for word in tokens if word in embeddings_index]
                        return np.mean(vectors, axis=0) if vectors else np.zeros(100)

                    glove_features = tokenized.apply(get_glove_vector)
                    glove_df = pd.DataFrame(glove_features.tolist(), columns=[f"{col}_glove_{i}" for i in range(100)])
                    df_copy = pd.concat([df_copy.drop(columns=[col]), glove_df], axis=1)
                elif text_vector == "bert":
                    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                    model = BertModel.from_pretrained('bert-base-uncased')
                    def get_bert_embedding(text):
                        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
                        with torch.no_grad():
                            outputs = model(**inputs)
                        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()  # CLS token

                    bert_features = df_copy[col].astype(str).fillna("").apply(get_bert_embedding)
                    bert_df = pd.DataFrame(bert_features.tolist(), columns=[f"{col}_bert_{i}" for i in range(768)])
                    df_copy = pd.concat([df_copy.drop(columns=[col]), bert_df], axis=1)

            # Outlier handling
            if outlier_method and outlier_action:
                if outlier_method == "iqr":
                    Q1 = df_copy[col].quantile(0.25)
                    Q3 = df_copy[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
                elif outlier_method == "zscore":
                    mean = df_copy[col].mean()
                    std = df_copy[col].std()
                    lower, upper = mean - 3 * std, mean + 3 * std

                if outlier_action == "remove":
                    df_copy = df_copy[(df_copy[col] >= lower) & (df_copy[col] <= upper)]
                elif outlier_action == "cap":
                    df_copy[col] = np.clip(df_copy[col], lower, upper)
                elif outlier_action == "replace":
                    method = df_copy[col].median() if outlier_method == "iqr" else df_copy[col].mean()
                    df_copy.loc[(df_copy[col] < lower) | (df_copy[col] > upper), col] = method

            # Global tools
            if dtype_action:
                if "infer" in dtype_action:
                    df_copy = df_copy.infer_objects()
                elif "change" in dtype_action and changed_dtype:
                    df_copy[col] = df_copy[col].astype(changed_dtype)
            if index_col:
                df_copy.set_index(index_col, inplace=True)
        if rename_cols:
            new_names = eval(rename_input)
            df_copy.rename(columns=new_names, inplace=True)
        if reorder_cols:
            order = eval(reorder_input)
            df_copy = df_copy[order]

    # Row-wise operations
    if drop_dups:
        df_copy = df_copy.drop_duplicates()
    if null_drop_cond and null_drop_cols:
        if "any" in null_drop_cond:
            df_copy = df_copy.dropna(subset=null_drop_cols, how="any")
        if "all" in null_drop_cond:
            df_copy = df_copy.dropna(subset=null_drop_cols, how="all")
    if filter_rows and filter_cond:
        df_copy = df_copy.query(filter_cond)
    if sort_col and sort_order:
        df_copy = df_copy.sort_values(by=sort_col, ascending=(sort_order == "asc"))
    if add_col_name and add_col_formula:
        df_copy[add_col_name] = eval(add_col_formula, {"df": df_copy})

    return (
        html.Div("✅ Preprocessing applied successfully!", style={"color": "green", "marginBottom": "10px"}),
        df_copy.to_dict("records"),
        [{"name": i, "id": i} for i in df_copy.columns],
        df_copy.to_dict("records")  # Store preprocessed version
    )
        #return df_copy.to_dict('records'), "✅ Preprocessing applied successfully."

    # except Exception as e:
    #     return f"❌ Error: {str(e)}", dash.no_update, dash.no_update, dash.no_update

@callback(
    Output("apply-button", "style"),
    Input("apply-button", "n_clicks")
)
def update_button_style(n_clicks):
    if n_clicks and n_clicks > 0:
        print("Apply preprocessing clicked")
        return {"backgroundColor": "#28a745", "color": "white"}  # green on click
    return {"backgroundColor": "#007BFF", "color": "white"}  # default blue

@callback(
    Output("download-preprocessed", "data"),
    Input("download-btn", "n_clicks"),
    State("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def download_preprocessed(n_clicks, contents, filename):
    if contents is None:
        return

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return
    except Exception:
        return

    # Example transformation placeholder
    df_processed = df.copy()

    return dcc.send_data_frame(df_processed.to_csv, filename="preprocessed.csv", index=False)