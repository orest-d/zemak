from flask import Flask, redirect, make_response
from macro import execute_macro
app = Flask(__name__)
import yaml
import json

@app.route('/')
def index():
    return redirect("/static/index.html")

@app.route('/test')
def test():
    return dict(log=execute_macro(r"""
    # Test macro
    CONTROL ALT T
    SLEEP 0.2
    "ls\n"
    """, execute=False))

_macros=None
def macros_definition():
    global _macros
    import os.path
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"macro.yaml")
    return yaml.load(open(path))
    if _macros is None:
        _macros = yaml.load(open(path))
    return _macros 

def macros_lookup():
    m = macros_definition()
    d={}
    for s in m:
        screen = s["id"]
        sd = d.get(screen,{})
        for row in s["grid"]:
            for macro in row:
                sd[macro["id"]]=macro
        d[screen]=sd
    return d

@app.route('/api/grid.json')
def grid():
    r = make_response( json.dumps(dict(data=macros_definition(), status="OK", message="Fetched grid") ))
    r.mimetype = 'application/json'
    return r    

@app.route('/api/lookup.json')
def lookup():
    r = make_response( json.dumps(dict(data=macros_lookup(), status="OK", message="Fetched lookup")) )
    r.mimetype = 'application/json'
    return r    

@app.route('/macro/<screen_name>/<macro_name>')
def macro(screen_name,macro_name):
    try:
        macro = macros_lookup()[screen_name][macro_name]
    except:
        return dict(log=[], status = "ERROR", message=f"Macro {screen_name} / {macro_name} not defined")
    log=execute_macro(macro["macro"], execute=True)
    r = make_response( json.dumps(dict(log=log,status=log[-1]["type"], message=log[-1]["message"]) ))
    r.mimetype = 'application/json'
    return r    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
