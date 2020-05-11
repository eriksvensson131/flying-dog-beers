import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('income_per_person_gdppercapita_ppp_inflation_adjusted.csv')
countries = list(df.country)

app.layout = html.Div([
    dcc.Graph(id='gdp-by-year'),
    html.Label('Select countries'),
    dcc.Dropdown(
        id='country-selector',
        options=[
            {'label': country, 'value': country} for country in countries
        ],
        value=['Sweden', 'Denmark', 'United States', 'India', 'China'],
        multi=True
    )
])


@app.callback(
    Output(component_id='gdp-by-year', component_property='figure'),
    [Input(component_id='country-selector', component_property='value')]
)
def update_figure(selected_countries):
    df_select = df[df['country'].isin(selected_countries)]
    years = df_select.columns[100:-18]
    long_df = pd.melt(df_select, id_vars='country', value_vars=years, var_name='year', value_name='gdp')
    return {
        'data': [
            dict(
                x=long_df[long_df['country'] == i]['year'],
                y=long_df[long_df['country'] == i]['gdp'],
                mode='line',
                opacity=1.0,
                marker={
                    'size': 1,
                    'line': {'width': 0.2, 'color': 'white'}
                },
                name=i
            ) for i in long_df.country.unique()
        ],
        'layout': dict(
            xaxis={'title': 'year'},
            yaxis={'type': 'log', 'title': 'inflation adjusted gdp per capita'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)