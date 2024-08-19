import os
import dash
from dash import html

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div("Hello, Render!")

if __name__ == "__main__":
    # Get the port from the environment variable
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)
