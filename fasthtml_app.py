import modal

app = modal.App("solab-fast-html")

@app.function(
    image=modal.Image.debian_slim(python_version="3.12").pip_install(
        "python-fasthtml==0.5.2"
    ),
    gpu="any",
)

@modal.asgi_app()
def serve():
    import json
    import subprocess
    import fasthtml.common as fh
    app, rt = fh.fast_app(
        hdrs=(fh.Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js"),),
        debug=True
    )

    data = json.dumps({
    "data": [{"x": [1, 2, 3, 4],"type": "scatter"},
            {"x": [1, 2, 3, 4],"y": [16, 5, 11, 9],"type": "scatter"}],
    "title": "Plotly chart in FastHTML ",
    "description": "This is a demo dashboard",
    "type": "scatter"
    })

    @app.get("/gpu")
    def gpu():
        output = subprocess.run("nvidia-smi", capture_output=True, text=True)
        return fh.Div(
            *[fh.P(line) for line in output.stdout.splitlines()],
            hx_get="change",
            )

    @rt("/chart")
    def get():
        return fh.Titled(
            "Chart Demo", 
            fh.Div(id="myDiv"),
            fh.Script(f"var data = {data}; Plotly.newPlot('myDiv', data);")
        )

    @rt("/oops")
    def get():
        1 / 0
        return fh.Titled("FastHTML Error!", fh.P("Let's error!"))

    @rt("/{name}/{age}")
    def get(name: str, age: int):
        return fh.Titled(f"Hello {name.title()}, age {age}")

    @rt("/")  
    def get():
        return fh.Titled("HTTP POST", fh.P("Handle POST"))

    @rt("/")  
    def post():
        return fh.Titled("HTTP POST", fh.P("Handle POST"))

    return app

