import os
import dash
import dash_html_components as html

app = dash.Dash(__name__)

# Get the port from the environment variable
port = int(os.environ.get("PORT", 8050))

app.layout = html.Div("Hello, Render!")

# Get the port from the environment variable
port = int(os.environ.get("PORT", 8050))

if __name__ == "__main__":
    server = app.server
    app.run_server(host="0.0.0.0", port=port)
