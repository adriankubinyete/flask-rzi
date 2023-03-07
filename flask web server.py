from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return """<p>TESTE</p>"""

@app.route("/mytest", methods=['GET', 'POST', 'PUT'])
def mytest():
    args = request.args
    # args.get("arg")
    # args.get("arg", default="", type=str)
    for k in args:
        print(k)
    return "<p>teste2</p>"

@app.route("/stop", methods=['GET', 'POST', 'PUT'])
def stop():
    return "<p>Whoops.</p>"

if __name__ == "__main__":
    app.run()
    
# rodar no terminal 
# flask --app "[nome arquivo]" run
# após, dar CTRL C no terminal p/ parar o server