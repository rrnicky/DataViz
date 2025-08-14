from dash import dcc, html
import logging
logging.basicConfig(level=logging.DEBUG)

def ml_layout():
    return html.Div(
    children=[
        # html.Div(
        #     "DataViz - Machine Learning Models",
        #     style={
        #         "backgroundColor": "#4a4a4a",
        #         "color": "white",
        #         "fontSize": "24px",
        #         "padding": "10px",
        #         "textAlign": "left",
        #         "fontWeight": "bold",
        #     },
        # ),
        html.Div(
            children=[
                html.Span("DataViz - ML Models", style={"fontSize": "18px", "fontWeight": "regular","color": "#e6ac00"}),  # DataViz Text

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
                #"fontWeight": "bold",
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
                        "width": "13%",
                        "padding": "10px",
                        "paddingTop": "10px",
                        "display": "flex",
                        "flex-direction": "column",
                        #"gap": "15px",
                        "background-color": "#333333"
                    },
                    children = [
                        html.Div([
                                html.Label("Machine Learning Type",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px"}), # Font size),
                                dcc.Dropdown(
                                    id="ml-type-dropdown",
                                    options=[
                                        {"label": "Supervised-Regression", "value": "supervised-r"},
                                        {"label": "Supervised-Classification", "value": "supervised-c"},
                                        {"label": "Unsupervised", "value": "unsupervised"},
                                    ],
                                    style={"marginBottom": "20px", "fontSize": "10px","color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                ),
                                html.Div(
                                    id="sr-dropdown-container",
                                    children=[
                                        html.Label("Supervised-Regression Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="sr-algorithm-dropdown",
                                            options=[
                                                {"label": "Linear Regression", "value": "lin_reg"},
                                                {"label": "Polynomial Regression", "value": "poly_reg"},
                                                {"label": "Support Vector Regression", "value": "svr"},
                                                {"label": "KNN", "value": "knn"},
                                                {"label": "Decision Tree", "value": "decision_tree"},
                                                {"label": "Random Forest", "value": "random_forest"},
                                                {"label": "Gradient Boosting", "value": "grad_boosting"},
                                                {"label": "LightGBM", "value": "lgbm"},
                                                {"label": "Neural Networks", "value": "nn"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "height":"11spx", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                                html.Div(id="slr-container", style={}),
                                html.Div(
                                    id="sc-dropdown-container",
                                    children=[
                                        html.Label("Supervised-Classification Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="sc-algorithm-dropdown",
                                            options=[
                                                {"label": "Logistic Regression", "value": "log_reg"},
                                                {"label": "Decision Tree", "value": "decision_tree"},
                                                {"label": "Random Forest", "value": "random_forest"},
                                                {"label": "Gradient Boosting", "value": "grad_boosting"},
                                                {"label": "LightGBM", "value": "lgbm"},
                                                {"label": "K Nearest Neighbours-KNN", "value": "knn"},
                                                {"label": "Naives Bayes", "value": "nb"},
                                                {"label": "Support Vector Regression", "value": "svm"},
                                                {"label": "Neural Networks", "value": "nn"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                                html.Div(
                                    id="ul-dropdown-container",
                                    children=[
                                        html.Label("UnSupervised Learning Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="ul-algorithm-dropdown",
                                            options=[
                                                {"label": "Clustering", "value": "clustering"},
                                                {"label": "Association Rule Mining", "value": "assc_rule_mining"},
                                                {"label": "Dimensionality Reduction ", "value": "dimen_red"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                                html.Div(
                                    id="clustering-dropdown-container",
                                    children=[
                                        html.Label("Clustering Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="clustering-algorithm-dropdown",
                                            options=[
                                                {"label": "K-means", "value": "k_means"},
                                                {"label": "Hierarchical", "value": "hierarchical"},
                                                {"label": "DBSCAN", "value": "dbscan"},
                                                {"label": "Mean-Shift", "value": "mean_shift"},
                                                {"label": "Spectral", "value": "spectral"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                                html.Div(
                                    id="arm-dropdown-container",
                                    children=[
                                        html.Label("Association Rule Mining Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="arm-algorithm-dropdown",
                                            options=[
                                                {"label": "Apriori", "value": "apriori"},
                                                {"label": "FP Growth", "value": "fp_growth"},
                                                {"label": "Eclat", "value": "eclat"},
                                                {"label": "Tree Based", "value": "tree"},
                                                {"label": "Spectral", "value": "spectral"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                                html.Div(
                                    id="dr-dropdown-container",
                                    children=[
                                        html.Label("Dimensionality Reduction Algorithm",style={
                                   "color": "#999999",  # Text color
                                   "fontSize": "12px", }),
                                        dcc.Dropdown(
                                            id="dr-algorithm-dropdown",
                                            options=[
                                                {"label": "Principal Component Analysis-PCA", "value": "pca"},
                                                {"label": "Linear Discriminant Analysis-LDA", "value": "lda"},
                                                {"label": "Non-negative Matrix Factorization-NMF", "value": "nmf"},
                                                {"label": "Locally Linear Embedding-LLE", "value": "lle"},
                                                {"label": "Isomap", "value": "isomap"},
                                            ],
                                            style={"marginBottom": "20px", "fontSize": "10px", "color": "#333333",
                                               "width": "100%","background-color": "#737373","borderRadius":"8px", "border":"none"}
                                        ),
                                    ],
                                    style={"display": "none"},
                                ),
                        ],
                            style={"width":"80%"}
                        ),
                    ],
                ),
                html.Div(
                    id="main-container",
                    style={"width": "80%", "padding": "20px", "backgroundColor": "#e5f6ff"},
                    children=[
                        html.Div(id="ml-model-summary",
                                 style={"height": "70vh", "backgroundColor": "#ffffff", "padding": "10px",
                                        "borderRadius": "10px"}),
                    ],
                ),
            ],
        ),
    ]
    )