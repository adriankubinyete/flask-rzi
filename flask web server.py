from flask import Flask, request, render_template
import json
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def main():
    return """<p>TESTE</p>"""

@app.route("/mytest", methods=['GET', 'POST', 'PUT'])
def mytest():
    
    if request.method =='POST': # se o método for POST, vou tratar os valores recebidos e exibir a página de resultado para POST

        request_data = request.get_json(force=True)
        zhn = request_data['zhn']
        print(request_data['zhn'])
        ip = request_data['ip']
        porta = request_data['porta']
        usuario = request_data['usuario']
        senha = request_data['senha']

#        zhn = request.form.get('zhn')
#        ip = request.form.get('ip')
#        porta = request.form.get('porta')
#        usuario = request.form.get('usuario')
#        senha = request.form.get('senha')
        return f'''
                  <h1>valor de zhn: {zhn}</h1>
                  <h1>valor de ip: {ip}</h1>
                  <h1>valor de porta: {porta}</h1>
                  <h1>valor de usuario: {usuario}</h1>
                  <h1>valor de senha: {senha}</h1>'''

    # o método NÃO É POST, então vou tratar com este outro html
    return '''
<form method="POST">
    <div><label>ZHN: <input type="text" name="zhn"></label></div>
    <div><label>IP: <input type="text" name="ip"></label></div>
    <div><label>PORTA: <input type="text" name="porta"></label></div>
    <div><label>USUÁRIO: <input type="text" name="usuario"></label></div>
    <div><label>SENHA: <input type="text" name="senha"></label></div>
    <input type="submit" value="Submit">
</form>'''

def post():
    return 


def just_a_test():
    # request.args['arg'] = obrigatório, se não existir, retornará 400 Bad Request
    # request.args.get['arg'] = opcional, se não existir, retornará None
    primeiro = request.args.get('primeiro')
    segundo = request.args.get('segundo')
    terceiro = request.args.get('terceiro') 
    return '''<h1>primeiro:{}</h1>
<h1>segundo:{}</h1>
<h1>terceiro:{}</h1>'''.format(primeiro, segundo, terceiro)

if __name__ == "__main__":
    app.run()
    
# rodar no terminal 
# flask --app "[nome arquivo]" run
# após, dar CTRL C no terminal p/ parar o server