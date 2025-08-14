from dash import html, dcc, dash_table


preprocessing_layout = html.Div([
    html.Div(
        children=[
            html.Span("DataViz - Preprocessing", style={"fontSize": "22px", "fontWeight": "regular"}),
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
        style={"height": "40px","backgroundColor": "#000000", "color": "#e6ac00", "fontSize": "20px",
               "padding-left": "20px", "padding-top": "10px", "padding-bottom": "10px", "textAlign": "left",
               "position": "relative"}  # Enable Absolute Positioning for Home Icon}
    ),
    html.Div(
        style={"display": "flex", "background-color": "#d3d3d3", "height": "100vh"},
        children=[
            html.Div(
                id="sidebar",
                style={"width": "40%", "padding": "10px", "background-color": "#111111", "overflowY": "scroll", "maxHeight": "100vh"},
                children=[
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(["📁 Upload File"]),
                        style={"color": "white", "backgroundColor": "#666", "padding": "10px", "borderRadius": "5px",
                               "textAlign": "center", "cursor": "pointer", "marginTop":"10px","marginLeft":"80px","marginBottom":"10px", "width":"60%"},
                        multiple=False
                    ),
                    html.Br(),
                    html.Div([
                        html.H4("Column wise Preprocessing Panel", style={"color": "#E97B44", 'marginLeft':"4%", "textAlign":"center"}), ##52BA9B #F6D298
                        # html.Br(),
                        html.Label("Select Column(s)", style={"color": "white",'marginLeft':"4%" }),
                        dcc.Dropdown(id="column-selector", multi=True, style={ "backgroundColor":"#FEF7EE", 'marginLeft':"4%","width":"80%"}),
                        html.Br(),
                        # first row
                        html.Div([
                            # Missing Value Handling Box
                            html.Div([
                                html.H5("Missing Value Handling", style={"color": "#F6D298", "marginTop":"4px"}), #52A5BA
                                dcc.RadioItems(
                                    id='missing-handler',
                                    options=[
                                        {'label': 'Drop rows', 'value': 'drop'},
                                        {'label': 'Fill with mean', 'value': 'mean'},
                                        {'label': 'Fill with median', 'value': 'median'},
                                        {'label': 'Fill with mode', 'value': 'mode'},
                                        {'label': 'Fill with constant', 'value': 'constant'}
                                    ],
                                    labelStyle={"display": "block", "color": "white"}
                                ),
                                dcc.Textarea(
                                    id="fill-const",
                                    placeholder="Enter constant to fill",
                                    style={"width": "90%","backgroundColor":"#FEF7EE"}
                                )
                            ], style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'marginRight': '4%',
                                'marginLeft':"4%",
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)'
                            }),

                            # Encoding Box
                            html.Div([
                                html.H5("Encoding", style={"color": "#F6D298","marginTop":"4px"}),
                                dcc.RadioItems(
                                    id="encoding-type",
                                    options=[
                                        {"label": "Label Encoding", "value": "label"},
                                        {"label": "One-Hot", "value": "onehot"},
                                        {"label": "Binary", "value": "binary"},
                                        {"label": "Custom Mapping", "value": "custom"},
                                    ],
                                    labelStyle={"display": "block", "color": "white"}
                                ),
                                dcc.Textarea(
                                    id="custom-mapping",
                                    placeholder="Enter JSON mapping",
                                    style={"width": "90%","backgroundColor":"#FEF7EE"}
                                )
                            ], style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)',
                                'marginRight':"4%"
                            })
                        ],
                            style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),
                        #second row
                        html.Div([
                            html.Div([
                                html.H5("Scaling / Normalization", style={"color": "#F6D298","marginTop":"4px"}),
                                dcc.Checklist(
                                    options=[
                                        {"label": "MinMax", "value": "minmax"},
                                        {"label": "Z-Score", "value": "zscore"},
                                        {"label": "Robust", "value": "robust"},
                                        {"label": "Log Transform", "value": "log"},
                                        {"label": "Power Transform", "value": "power"},
                                    ],
                                    id="scaling-options",
                                    labelStyle={"display": "block", "color": "white"}
                                )
                            ],style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'marginRight': '4%',
                                'marginLeft':"4%",
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)'
                            }),

                            html.Div([
                                html.H5("Datetime Conversion", style={"color": "#F6D298","marginTop":"4px"}),
                                dcc.Checklist(
                                    options=[
                                        {"label": "Convert to datetime", "value": "convert"},
                                        {"label": "Extract Year", "value": "year"},
                                        {"label": "Extract Month", "value": "month"},
                                        {"label": "Extract DayOfWeek", "value": "day"},
                                        {"label": "Extract Hour", "value": "hour"},
                                    ],
                                    id="datetime-options",
                                    labelStyle={"display": "block", "color": "white"}
                                )
                            ],style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)',
                                'marginRight':"4%"
                            }),
                        ],style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),
                        #third row
                        html.Div([
                            html.Div([
                                html.H5("Other Processing", style={"color": "#F6D298","marginTop":"4px"}),
                                html.Div([
                                        # Radio buttons in a row
                                        html.Div([
                                            dcc.RadioItems(
                                                id='dtype-action',
                                                options=[
                                                    {'label': 'Infer datatypes', 'value': 'infer'},
                                                    {'label': 'Change datatype', 'value': 'change'}
                                                ],
                                                labelStyle={'display': 'inline-block', 'marginRight': '20px', 'color': 'white'},
                                                # style={'marginBottom': '10px'}
                                            ),
                                            dcc.Textarea(
                                                id='change-dtype',
                                                placeholder='Enter datatypes',
                                                style={'width': '90%', "backgroundColor":"#FEF7EE",'marginTop': '5px','marginBottom': '10px'}
                                            ),
                                        ]),

                                        # Set index column checkbox
                                        html.Div([
                                            dcc.Checklist(
                                                id='set-index',
                                                options=[{'label': 'Set index column', 'value': 'set'}],
                                                labelStyle={'display': 'block', 'color': 'white'}
                                            )
                                        ]),

                                        # Rename columns
                                        html.Div([
                                            dcc.Checklist(
                                                id='rename-cols',
                                                options=[{'label': 'Rename columns', 'value': 'rename'}],
                                                labelStyle={'display': 'block', 'color': 'white'}
                                            ),
                                            dcc.Textarea(
                                                id='rename-input',
                                                placeholder='Enter new column names',
                                                style={'width': '90%',"backgroundColor":"#FEF7EE"}
                                            )
                                        ]),

                                        # Reorder columns
                                        html.Div([
                                            dcc.Checklist(
                                                id='reorder-cols',
                                                options=[{'label': 'Reorder columns', 'value': 'reorder'}],
                                                labelStyle={'display': 'block', 'color': 'white'}
                                            ),
                                            dcc.Textarea(
                                                id='reorder-input',
                                                placeholder='Enter new column order',
                                                style={'width': '90%',"backgroundColor":"#FEF7EE"}
                                            )
                                        ])
                                    ])
                            ],style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'marginRight': '4%',
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)',
                                'marginLeft':"4%"
                            }),
                            html.Div([
                                    html.H5("Outlier Handling", style={"color": "#F6D298", "marginTop":"4px" }),
                                    dcc.RadioItems(
                                        id="outlier-method",
                                        options=[
                                            {"label": "IQR", "value": "iqr"},
                                            {"label": "Z-score", "value": "zscore"},
                                        ],
                                        labelStyle={"display": "inline-block", "margin-right": "10px", "color": "white"}
                                    ),
                                    dcc.RadioItems(
                                        id="outlier-action",
                                        options=[
                                            {"label": "Remove", "value": "remove"},
                                            {"label": "Cap at percentiles", "value": "cap"},
                                            {"label": "Replace with (mean/median)", "value": "replace"},
                                        ],
                                        labelStyle={"display": "block", "color": "white"}
                                    )
                                ],
                            style={
                                'width': '48%',
                                # 'border': '2px solid #ccc',
                                'borderRadius': '8px',
                                'backgroundColor': '#333333',
                                'padding': '10px',
                                'boxShadow': '2px 2px 10px rgba(0,0,0,0.2)',
                                'marginRight':"4%"
                            })
                        ], style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),

                        html.Div([
                            html.H4("Text Preprocessing", style={"color": "#F6D298", "textAlign":"center"}),
                            html.H5("Basic Cleaning", style={"color": "#F6D298", "marginTop":"4px" }),
                            dcc.Checklist(
                                id="basic-text-cleaning",
                                options=[
                                    {"label": "Lowercase", "value": "lower"},
                                    {"label": "Remove punctuation", "value": "punct"},
                                    {"label": "Remove numbers", "value": "numbers"},
                                    {"label": "Strip whitespace", "value": "strip"},
                                    {"label": "Remove stopwords", "value": "stopwords"},
                                    {"label": "Remove frequent words", "value": "frequent"},
                                    {"label": "Remove rare words", "value": "rare"},
                                    {"label": "Tokenize text", "value": "tokenize"}
                                ],
                                labelStyle={"display": "b lock", "color": "white"},
                                style={"marginBottom": "10px"}
                            ),

                            #html.Label("Word normalization", style={"color": "white"}),
                            html.H5("Word normalization", style={"color": "#F6D298", "marginTop":"4px" }),
                            dcc.RadioItems(
                                id="text-normalization",
                                options=[
                                    {"label": "Stemming", "value": "stem"},
                                    {"label": "Lemmatization", "value": "lemma"},
                                ],
                                value="none",
                                labelStyle={"display": "block", "color": "white"}
                            ),
                            html.Br(),
                            html.H5("Vectorization Method", style={"color": "#F6D298", "marginTop":"4px" }),
                            #html.Label("Vectorization Method", style={"color": "white"}),
                                dcc.RadioItems(
                                    id="vectorization-method",
                                    options=[
                                        {"label": "Bag of Words", "value": "bow"},
                                        {"label": "TF-IDF", "value": "tfidf"},
                                        {"label": "Word Embeddings(Word2Vec)", "value": "word2vec"},
                                        {"label": "Word Embeddings(GloVe)", "value": "glove"},
                                        {"label": "Transformer Embeddings(BERT)", "value": "bert"}
                                    ],
                                    value="none",
                                    labelStyle={"display": "block", "color": "white"}
                                )
                        ], style={
                            "backgroundColor": "#333333",
                            "padding": "15px",
                            "marginBottom": "20px",
                            #"border": "1px solid white",
                            "borderRadius": "10px",
                            'marginRight':"4%",
                            'marginLeft':"4%"
                        }),
                    ],style = {"border": "1px solid white", "borderRadius": "10px"}),


                    html.Div([
                        html.Div([
                            html.H4("Row wise Preprocessing Panel", style={"color": "#E97B44", "textAlign":"center"}),
                            # html.H4("🔁 Row-wise Operations Panel", style={"color": "white"}),
                            dcc.Checklist(
                                options=[
                                    {"label": "Drop duplicate rows", "value": "drop_duplicates"},
                                ],
                                id="drop-dups",
                                labelStyle={"display": "block", "color": "white"}
                            ),
                            dcc.RadioItems(
                                id="drop-nulls",
                                options=[
                                    {"label": "Any null", "value": "any"},
                                    {"label": "All null", "value": "all"},
                                ],
                                labelStyle={"display": "inline-block", "margin-right": "10px", "color": "white"}
                            ),
                            dcc.Dropdown(id="drop-null-columns", multi=True, placeholder="Select columns for null drop"),
                            html.Br(),
                            dcc.Checklist(
                                options=[{"label": "Filter rows", "value": "filter_rows"}],
                                id="filter-rows",
                                labelStyle={"display": "block", "color": "white"}
                            ),
                            dcc.Textarea(id="filter-cond", placeholder="e.g. Salary > 50000", style={"width": "99%"}),
                            html.Br(),
                            html.Br(),
                            dcc.Checklist(
                                options=[{"label": "Sort by", "value": "sort_by"}],
                                id="sort-checklist",
                                labelStyle={"display": "block", "color": "white"}
                            ),
                            dcc.Dropdown(id="sort-col", placeholder="Select column"),
                            dcc.RadioItems(
                                id="sort-order",
                                options=[
                                    {"label": "Ascending", "value": "asc"},
                                    {"label": "Descending", "value": "desc"},
                                ],
                                labelStyle={"display": "inline-block", "margin-right": "10px", "color": "white"}
                            ),
                            html.Br(),
                            html.Div([
                                html.Label("Add new column:", style={"color": "white"}),
                                dcc.Textarea(id="add-col-name", placeholder="Column Name",style={"width": "99%"}),
                                dcc.Textarea(id="add-col-formula", placeholder="Formula: df['a'] + df['b']", style={"width": "99%"})
                            ])
                        ], id = "row-ops", style={"backgroundColor": "#333333", "border": "1px solid #ccc", "padding": "15px", "marginBottom": "20px", "borderRadius": "10px"}),

                    ], style = {"marginTop":"20px"}),
                    html.Br(),

                    html.Button("Apply Preprocessing", id="apply-button", n_clicks=0, style={
                        "backgroundColor": "#007bff",
                        "color": "white",
                        "width": "200px !important",
                        "height": "60px !important",
                        "fontSize": "18px",
                        "border": "none",
                        "borderRadius": "8px",
                        "margin": "auto",
                        "display": "block !important"
                    })
                ]
            ),
            html.Div(
                id="main-container",
                style={"width": "85%", "padding": "20px", "backgroundColor":"#FEF7EE", "position": "relative"},
                children=[
                    dcc.Store(id="df-original"),
                    dcc.Store(id="df-preprocessed"),
                    html.Div(id="preprocessing-message"),
                    html.Div(id="preprocessing-summary", style={"height": "70vh", "backgroundColor": "#ffffff", "padding": "10px", "borderRadius": "10px"}),
                    dash_table.DataTable(
                            id="preview-table",
                            columns=[],  # Empty initially
                            data=[],     # Empty initially
                            page_size=10,
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "left", "padding": "5px"},
                            style_header={"backgroundColor": "#f1f1f1", "fontWeight": "bold"}
                        ),
                    html.Div([
                        html.Button("Download Preprocessed CSV", id="download-btn",
                                    style={"marginTop": "10px",
                                            "backgroundColor":"#366D3F",
                                            "color": "white",
                                            "width": "200px !important",
                                            "height": "60px !important",}),
                        dcc.Download(id="download-preprocessed")
                    ], style={"position": "absolute", "right": "20px", "bottom": "130px"})
                ]
            )
        ]
    )
    ],style={'fontFamily': 'Inter, sans-serif', 'fontSize': "14px"})

