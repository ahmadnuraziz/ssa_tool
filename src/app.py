import dash
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Analytics Tool", className="display-4"),
        html.Hr(),
        # html.P(
        #     "Simple Self-service Analytics Tools", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/homepage", active="exact"),
                dbc.NavLink("Power Analysis Calculator", href="/power-analysis-calculator-page", active="exact"),
                dbc.NavLink("A/B Testing Calculator", href="/ab-testing-calculator-page", active="exact"),
                dbc.NavLink("Coming Soon!", href="/coming-soon", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/homepage":
        return dbc.Container([
          html.H1(children='Welcome!'),
        	html.P("Here you can find a simple self-service analytics tools that (hopefully) can help your work."),
          html.P("The tools include:"),
          html.P("1. Power analysis calculator for sample size and experiment duration estimation."),
					html.P("2. Post-experiment analysis calculator for A/B testing experiment analysis. On current version, still only for proportion metric, such as conversion rate."),
          html.P("3. Coming soon!")
				])
    
    elif pathname == "/power-analysis-calculator-page":
        return dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Power Analysis Calculator",className='text-primary my-4 text-center'), width=10)
    ],  justify="center"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
            dbc.CardHeader("Input Parameters", className="text-center"),
            dbc.CardBody([
            dbc.Row([
                html.Div([
                    html.Label('Metric Type'),
                    dcc.Dropdown(
                        id='metric_type',
                        multi=False,
                        # value = 'Proportion',
                        options=[
                            {'label': 'Proportion',
                             'value': 'proportion'},
                            {'label': 'Continuous', 'value': 'continuous'}]
                    )
                ])
            ], className="mb-3", style={'width': '60%'}),

            dbc.Row([
                html.Div([
                    html.Label('Metric Mean'),
                    dbc.Input(type="number", id="metric_mean",min=0)]),

                html.Div(id='metric_type_note')
            ], className="mb-3", style={'width': '60%'}),

            dbc.Row([
                html.Div([
                    html.Label('Metric Variance'),
                    dbc.Input(type="number", id="metric_variance",min=0)])
            ], className="mb-3", style={'width': '60%'}),

            dbc.Row([
                html.Div([
                    html.Label('Daily Traffic'),
                    dbc.Input(type="number", id="daily_traffic",min=0)])
            ], className="mb-3", style={'width': '60%'}),

            dbc.Row([
                dbc.Col([
                    html.Label( 'Percentage Population'),
                    dbc.InputGroup([
                        dbc.Input(type="number",
                                  value=100,
                                  min=0,
                                  max=100,  step=1, id="percentage_population"),
                        dbc.InputGroupText("%")
                    ])
                ]),

                dbc.Col([
                    html.Br(),
                    html.I(
                        id="info-population", className="fas fa-info-circle"),

                    dbc.Tooltip(
                        "The percentage population",
                        target="info-population",
                        placement="right"
                    )
                ])
            ], className="mb-3", style={'width': '70%'}),

            dbc.Row([
                dbc.Col([
                    html.Label('Number of Variants'),
                    dbc.Input(type="number",value=2, id="n_variants",min=1)]),

                dbc.Col([
                    html.Br(),
                    html.I(
                        id="info-variants", className="fas fa-info-circle"),

                    dbc.Tooltip(
                        "Including control variant",
                        target="info-variants",
                        placement="right"
                    )
                ])
            ], className="mb-3", style={'width': '60%'}),

            dbc.Row([
                dbc.Col([
                    html.Label(
                        'Statistical Significance'),
                    dbc.InputGroup([
                        dbc.Input(type="number",
                                  value=95,
                                  min=0,
                                  max=100,  step=1, id="statistical_significance"),
                        dbc.InputGroupText("%")
                    ])
                ]),

                dbc.Col([
                    html.Br(),
                    html.I(
                        id="info-statistical-significance", className="fas fa-info-circle"),

                    dbc.Tooltip(
                        "The default value is 95%",
                        target="info-statistical-significance",
                        placement="right"
                    )
                ])
            ], className="mb-3", style={'width': '70%'}),

            dbc.Row([
                dbc.Col([
                    html.Label(
                        'Statistical Power'),
                    dbc.InputGroup([
                        dbc.Input(type="number",
                                  value=80,
                                  min=0,
                                  max=100,  step=1, id="statistical_power"),
                        dbc.InputGroupText(
                            "%")
                    ])
                ]),

                dbc.Col([
                    html.Br(),
                    html.I(
                        id="info-statistical-power", className="fas fa-info-circle"),

                    dbc.Tooltip(
                        "The default value is 80%",
                        target="info-statistical-power",
                        placement="right"
                    )
                ])
            ], className="mb-3", style={'width': '70%'}),

            dbc.Row([
                dbc.Col([
                    html.Label(
                        'Minimum Detectable Effect'),
                    html.Br(),
                    dcc.RangeSlider(
                        id='mde_slider',
                        min=0,  # Minimum value of the slider
                        max=100,  # Maximum value of the slider
                        # value=5,  # Default value of the slider
                        value=[1, 10],
                        step=1,  # Step size
                        marks={
                            i: {'label': str(i) + '%'} for i in range(0, 101, 10)
                        },
                        tooltip={
                            "placement": "bottom", "always_visible": True},
                    )
                ], width={"size": 8})
            ])
					])
        ])
			]), # Row 2, column 1

      dbc.Col([
        dbc.Card([
            dbc.CardHeader("Output", className="text-center py-2"),
            dbc.CardBody([
            dcc.Graph(id='duration_chart',style={'margin-bottom': '15px'}),

            dcc.Graph(id='sample_size_chart',style={'margin-top': '15px'})
					])])
				])  # Row 2, column 1
    	])  # Row 2
		])  # container
    
    elif pathname == "/ab-testing-calculator-page":
        return dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("A/B Testing Calculator",className='text-primary my-4 text-center'), width=10)
    ],  justify="center"),

    dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
              dbc.Row([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div(html.H1("A", className="mt-3"), className="text-center")  # Align "A" with inputs
                            ], width=1, className="d-flex align-items-center"),  # Centering "A"

                            dbc.Col([
                                html.Label('Users'),
                                dbc.Input(type="number", id="users_varA", min=0, value=1000),
                            ], width=5),  # Adjusted to 5 for equal spacing
                            dbc.Col([
                                html.Label('Conversions'),
                                dbc.Input(type="number", id="conversions_varA", min=0, value=100),
                            ], width=5)  # Adjusted to 5 for equal spacing
                        ])
                    ], className="mb-3")
                ]), #row for group A

              dbc.Row([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Div(html.H1("B", className="mt-3"), className="text-center")  # Align "B" with inputs
                            ], width=1, className="d-flex align-items-center"),  # Centering "B"

                            dbc.Col([
                                html.Label('Users'),
                                dbc.Input(type="number", id="users_varB", min=0, value=1000),
                            ], width=5),  # Adjusted to 5 for equal spacing
                            dbc.Col([
                                html.Label('Conversions'),
                                dbc.Input(type="number", id="conversions_varB", min=0, value=90),
                            ], width=5)  # Adjusted to 5 for equal spacing
                        ])
                    ], className="mb-3")
                ]), #row for group B

              dbc.Row([
                    dbc.Col([
                      dcc.RadioItems(options=[
                          {'label': 'One-sided', 'value': 'One-sided'},
                          {'label': 'Two-sided', 'value': 'Two-sided'}
                          ],
                          id='hypothesis',
                          value='Two-sided',  # Default selected value
                          inline=True,
                          labelStyle={'margin-right': '20px'}  # Increase spacing between the options
                    )
                  ])
              ]), #Hypothesis

              # html.Br(),

              # dbc.Row([
              #       dbc.Col([
              #         dbc.Button("Calculate", id="calculate_button", className="btn btn-primary", style={"color": "white"})
              #       ])
              # ]), # Button row

            ])
        ])
    ]),

    dbc.Col([
            dbc.Row(id='results-row', children=[
            # This row will be populated by the callback
          ])
        ])
      ])
    ]) #container
  

@app.callback(
    [
        Output('metric_type_note', 'children'),
        Output('metric_mean', 'step')
    ],

    [
        Input('metric_type', 'value')
    ]
)
def update_metric_note(metric_type):
    if metric_type == 'proportion':
        note = html.P('Note: Value should be between 0 and 1',
                      style={'color': 'red'})
        step = 0.1
    else:
        note = ''
        step = 1
    return note, step


@app.callback(
    [Output('duration_chart', 'figure'),
     Output('sample_size_chart', 'figure')],
    [
      Input('metric_mean', 'value'),
      Input('metric_variance', 'value'),
      Input('daily_traffic', 'value'),
      Input('n_variants', 'value'),
      Input('mde_slider', 'value'),
      Input('statistical_significance', 'value'),
      Input('statistical_power', 'value'),
      Input('percentage_population', 'value'),
    ]
)
def update_chart(mean, variance, traffic, n_variant, mde_range, statistical_significance, statistical_power,percentage_population):
    if not all(v is not None for v in [mean, variance, traffic, n_variant]) or not mde_range:
        # If not all inputs are filled, return an empty chart
        return go.Figure(), go.Figure()

    alpha = 1 - statistical_significance/100
    beta = 1 - statistical_power/100

    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(1 - beta)
    
    population = percentage_population/100

    duration = [population*int(n_variant*(2*(z_alpha+z_beta)**2 / (((mde*mean/100)**2)/variance))/traffic)
                for mde in range(mde_range[0], mde_range[1] + 1)]
    
    sample_size = [int((2*(z_alpha+z_beta)**2 / (((mde*mean/100)**2)/variance)))
                   for mde in range(mde_range[0], mde_range[1] + 1)]
    
    x_values = list(range(mde_range[0], mde_range[1] + 1))

    # Create a figure and update it with the X and Y values
    fig1 = go.Figure(data=go.Scatter(
        x=x_values, y=duration, mode='lines+markers'))

    fig1.update_layout(
        title={
            'text': 'Required Experiment Duration',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                    family="Verdana",
                    size=16,
                    color="black"
            )
        },
        xaxis_title={
            'text': 'MDE (%)',
            'font': dict(
                family="Verdana",
                size=12,
                color="black"
            ),
        },
        yaxis_title={
            'text': 'Duration in Days',
            'font': dict(
                family="Verdana",
                size=12,
                color="black"
            ),
        }
    )

    fig2 = go.Figure(data=go.Scatter(
        x=x_values, y=sample_size, mode='lines+markers'))

    fig2.update_layout(
        title={
            'text': 'Required Sample Size',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                    family="Verdana",
                    size=16,
                    color="black"
            ),
        },
        xaxis_title={
            'text': 'MDE (%)',
            'font': dict(
                family="Verdana",
                size=12,
                color="black"
            ),
        },
        yaxis_title={
            'text': 'Number of Sample Size',
            'font': dict(
                family="Verdana",
                size=12,
                color="black"
            ),
        }
    )
    return fig1, fig2

@app.callback(
    Output('results-row', 'children'),
    [Input('users_varA', 'value'),
     Input('users_varB', 'value'),
     Input('conversions_varA', 'value'),
     Input('conversions_varB', 'value'),
     Input('hypothesis','value')]
)

def update_calculation(users_varA, users_varB, conversions_varA, conversions_varB, hypothesis ):
    # Calculate conversion rates and statistics as before
    conversion_rate_A = conversions_varA / users_varA
    conversion_rate_B = conversions_varB / users_varB
    percentage_difference = ((conversion_rate_B - conversion_rate_A) / conversion_rate_A) * 100
    
    count = np.array([conversions_varA, conversions_varB])
    nobs = np.array([users_varA, users_varB])

    if hypothesis == 'Two-sided':
      stat, pval = proportions_ztest(count, nobs)
    else:
      stat, pval = proportions_ztest(count, nobs, alternative='larger')

    alpha = 0.05
    significant = "Yes" if pval < alpha else "No"

    # Determine the className based on percentage_difference
    className = "text-success" if percentage_difference > 0 else "text-danger"

    conclusion = 'better' if percentage_difference > 0 else 'worse'
    condition = 'can' if pval < 0.05 else "cannot"
    
    output_calculation = [
        dbc.Row([
          dbc.Col(
          dbc.Card([
            dbc.CardBody([
                html.H5("Variant A Conversions", className="card-title"),
                html.H2(str(conversion_rate_A)+'%', className="card-text"),
              ])
            ], className="h-100"), width=6),

          dbc.Col(
          dbc.Card([
            dbc.CardBody([
                html.H5("Variant B Conversions", className="card-title"),
                html.H2(str(conversion_rate_B)+'%', className="card-text"),
                html.P(f"Compared to variant A: {percentage_difference:.1f}%", className=className)
              ])
            ], className="h-100"), width=6),
        ]),

        html.Br(),

        dbc.Row([
          dbc.Col(
          dbc.Card([
            dbc.CardBody([
                html.H5("p value", className="card-title"),
                html.H2(f"{pval:.4f}", className="card-text"),
                html.P("We {} conclude that the variant B is {} than variant A".format(condition,conclusion))
            ])
          ], className="h-100"),width = 12)
        ], className="g-4")
    ]

    return output_calculation

if __name__ == "__main__":
    app.run_server(debug=True)