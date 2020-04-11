from flask import Flask, redirect, make_response, request
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


def macro_definition_path():
    import os.path
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"macro_active.yaml")
    if os.path.exists(path):
        return path
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),"macro.yaml")

_macros=None

def macros_definition():
    global _macros
    return yaml.load(open(macro_definition_path()))
#    if _macros is None:
#        _macros = yaml.load(open(path))
#    return _macros 

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
    try:
        r = make_response( json.dumps(dict(data=macros_definition(), status="OK", message="Fetched grid") ))
    except:
        r = make_response( json.dumps(dict(data=[], status="ERROR", message="Error loading macro definition")) )
    r.mimetype = 'application/json'
    return r    

@app.route('/api/lookup.json')
def lookup():
    try:
        r = make_response( json.dumps(dict(data=macros_lookup(), status="OK", message="Fetched lookup")) )
    except:
        r = make_response( json.dumps(dict(data={}, status="ERROR", message="Error creating lookup")) )
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

@app.route('/api/load.yaml')
def load():
    r = make_response(open(macro_definition_path()).read())
    r.mimetype = 'text/plain'
    return r

@app.route('/api/save', methods = ['POST'])
def save():
    import os.path
    import traceback
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"macro_active.yaml")
    try:
        with open(path,"w") as f:
            f.write(request.json["data"])
    except:
        traceback.print_exc()
        r = make_response( json.dumps(dict(status="ERROR", message="Error while saving") ))
        r.mimetype = 'application/json'

    r = make_response( json.dumps(dict(status="OK", message="Saved") ))
    r.mimetype = 'application/json'
    return r    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
