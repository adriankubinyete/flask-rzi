from flask import Flask, request, render_template
import json
from flask import jsonify
import time
import paramiko

def sshcommit(comando):
    print(f'> "{comando}"...')
    stdin, stdout, stderr = client.exec_command(comando, get_pty=True)
    resultpmk = stdout.read().decode('utf-8')
    erro = 'Erro!'
    if stdout.channel.recv_exit_status() == 0:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    else:
        print(f'RETURN: ' + str(stdout.channel.recv_exit_status()))
    if "Permission denied" in resultpmk:
        print('PERMISSION DENIED!')
        print(f'{resultpmk}')
        stdin.close()
        stdout.close()
        stderr.close()
        return erro
    else:
        stdin.close()
        stdout.close()
        stderr.close()
        return resultpmk


app = Flask(__name__)

@app.route("/")
def main():
    return """<p>TESTE</p>"""

@app.route("/erro")
def erro():
    return """<p>pagina de erro</p>"""

@app.route("/mytest", methods=['GET', 'POST', 'PUT'])
def mytest():
    
    if request.method =='POST': # se o método for POST, vou tratar os valores recebidos e exibir a página de resultado para POST
        
        key = "C:\\Users\\Operação 16\\.ssh\\id_rsa.pub"
        
        zabbix_server_ip = request.form['zabbix_ip']
        zabbix_host_name = request.form['zabbix_host_name']
        host_ip = request.form['host_ip']
        host_port = request.form['host_port']
        host_user = request.form['host_user']
        host_pass = request.form['host_pass']
        #print(f"""
#{zabbix_server_ip}
#{zabbix_host_name}
#{host_ip}
#{host_port}
#{host_user}
#{host_pass}""")

        # Abrindo o processo SSH PARAMIKO
        client = paramiko.client.SSHClient()
        # Aceitando/adicionando a KEY
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print('\n-- CONEXÃO PARAMIKO (SSH) --')
            client.connect(host_ip, username=host_user, password=host_pass, port=host_port, key_filename=key)
        except Exception as e:
            client.close()
            print(f"falha ao se conectar...")
            print(e)
            return '''<script>window.location.assign("/erro")</script>
'''
        else:
            print("conectado")

        return f'''
                  <h1>valor de zhn: {zabbix_host_name}</h1>
                  <h1>valor de ip: {host_ip}</h1>
                  <h1>valor de porta: {host_port}</h1>
                  <h1>valor de usuario: {host_user}</h1>
                  <h1>valor de senha: {host_pass}</h1>'''

    # o método NÃO É POST, então vou tratar com este outro html
    return '''
<form method="POST">
    <div><label>Zabbix IP: <input type="text" name="zabbix_ip" required></label></div>
    <div><label>HostName: <input type="text" name="zabbix_host_name" required></label></div>
    <div><label>IP: <input type="text" name="host_ip" required></label></div>
    <div><label>PORTA: <input type="text" name="host_port" required></label></div>
    <div><label>USUÁRIO: <input type="text" name="host_user" required></label></div>
    <div><label>SENHA: <input type="text" name="host_pass" required></label></div>
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