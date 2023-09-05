from dash import Dash, html

app = Dash(__name__)
app.layout = html.Div([html.H1(children=["Hello, world!"])])


def main():
    app.run(debug=True)
