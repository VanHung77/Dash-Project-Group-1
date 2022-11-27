import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv('Premier League Player Stats.csv')
app = dash.Dash()

fig = px.bar(data, x="MIN", y="SHOTS")
app.layout = html.Div(children=[
    html.H1(children='Premier League Player Stat (Minute Played)'), 
    dcc.Dropdown(id='team-dropdown', 
                 options=[{'label': i, 'value': i}
                         for i in data['TEAM'].unique()],
                value='Manchester United'),
    html.P('Select Time Played Value:', className = 'fix_label', style = {'color': 'white', 'margin-left': '1%'}),
            dcc.RangeSlider(id = 'select-min',
                            min = 0,
                            max = 3050,
                            dots = False,
                            allowCross=False,
                            pushable=2,
                            value = [0, 600]),
    dcc.Graph(id='player-graph')
    
])
@app.callback(
    Output(component_id='player-graph', component_property='figure'),
    [Input(component_id='team-dropdown', component_property='value')],
    # [Input(component_id='select-min', component_property='value')]
)
def update_graph(selected_team):
    filter_data = data[data['TEAM'] == selected_team]
    line_fig = px.line(data, x='PLAYER', y=['G', 'ASST', 'SHOTS', 'SOG'])
    return line_fig

# def build_graph(year):
#     fig.update_layout(yaxis={'title':'Incoming Border'},
#                     title={'text':'Border Crossing to the Minute Played'})
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)