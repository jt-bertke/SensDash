from dash import Dash, html

app = Dash(__name__)

card = html.Div(
    [
        html.H3("Speed"),
        html.H1("72 MPH"),
    ],
    style={
        "backgroundColor": "#1e1e1e",
        "padding": "20px",
        "borderRadius": "12px",
        "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
        "width": "200px",
        "textAlign": "center",
        "color": "white",
    },
)

app.layout = html.Div([card])

if __name__ == "__main__":
    app.run(debug=True)