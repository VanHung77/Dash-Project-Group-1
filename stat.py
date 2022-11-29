import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv('Premier League Player Stats.csv')
app = dash.Dash()

# fig = px.bar(data, x="MIN", y="SHOTS")
app.layout = html.Div(children=[
    html.H1(children='Premier League Player Stat (Performance)'), 
    html.Label(['Đội tuyển bạn đang chọn:'], style={'font-weight': 'bold', "text-align": "center"}),
    dcc.Dropdown(id='team-dropdown', 
                 options=[{'label': i, 'value': i}
                         for i in data['TEAM'].unique()],
                value='Manchester United'),
    html.P('Select Minute Played:', className = 'fix_label', style = {'color': 'white', 'margin-left': '1%'}),
            html.Label(['Kéo để lọc cầu thủ theo thời gian chơi:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.RangeSlider(id = 'select-min',
                            min = 0,
                            max = 3050,
                            dots = False,
                            allowCross=False,
                            pushable=2,
                            value = [0, 600]),
            # html.Div(id='min-played-range-slider'),
    dcc.Graph(id='player-graph')
    
])
@app.callback(
    Output(component_id='player-graph', component_property='figure'),
    [Input(component_id='team-dropdown', component_property='value'),
    Input(component_id='select-min', component_property='value')]
)
def update_graph(selected_team, selected_min):
    # print(selected_min)
    filter_data_min = data[(data['MIN'] >= selected_min[0])&(data['MIN']<=selected_min[1])]
    filter_data_team = filter_data_min[data['TEAM'] == selected_team]
    # fig = px.line(filter_data_min, x='PLAYER', y=['G', 'ASST', 'SHOTS', 'SOG'])
    fig = px.line(filter_data_team, x='PLAYER', y=['G', 'ASST', 'SHOTS', 'SOG'])
    # filter_data_min = 'You have selected "{}"'.format(selected_min)
    # team_dropdown_name= "Đội tuyển bạn đang chọn là: {}".format(selected_team)
    return fig

if __name__ == '__main__':
    print('Use CTRL+C TO SHUTDOWN DASH')
    app.run_server(debug=True)
    