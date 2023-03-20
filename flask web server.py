from flask import Flask, request, render_template, session, redirect, url_for
from functools import wraps
import json
from utils import test1, test2, redirectTo
from flask import jsonify
import time
import paramiko

def ssh(client, comando):
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('if_logged') is None:
            return redirect('/login',code=302)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def flask_main():
    return """<p>TESTE</p>"""

@app.route("/erro")
def flask_erro():
    return render_template("erro.html")

@app.route("/success")
def flask_success():
    return render_template("success.html")

@app.route("/zabbix", methods=['GET', 'POST'])
def flask_zabbix():
    
    if request.method =='POST': # se o método for POST, vou tratar os valores recebidos e exibir a página de resultado para POST
                
        key = "C:\\Users\\Operação 16\\.ssh\\id_rsa.pub"
                   
        zabbix_server_ip = request.form['zabbix_ip']
        zabbix_hostname = request.form['zabbix_host_name']
        host_ip = request.form['host_ip']
        host_port = 22 if request.form['host_port'] == '' else request.form['host_port']
        host_user = request.form['host_user']
        host_pass = 'noPass' if request.form['host_pass'] == '' else request.form['host_pass']
        host_key = 'noKey' if request.form['host_key'] == '' else request.form['host_key']
        
        # checagem de valores
        test1(zabbix_server_ip, "z-ip")
        test1(zabbix_hostname, "hostname")
        test1(host_ip, "h-ip")
        test1(host_port, "port")
        test1(host_user, "user")
        test1(host_pass, "pass")
        test1(host_key, "key")

        # Abrindo o processo SSH PARAMIKO
        client = paramiko.client.SSHClient()
        # Aceitando/adicionando a KEY
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print('\n-- INICIANDO CLIENTE PARAMIKO (Conexão SSH) --')
            client.connect(host_ip, username=host_user, password=host_pass, port=host_port, key_filename=key)
        except Exception as e:
            client.close()
            print(f"falha ao se conectar...")
            print(e)
            return redirectTo("/erro", _type="ssh", _erro=e)
        else:
            print('\n-- DESCENDO FIREWALL --')
            print('- nao implementado -')
            # Parando o firewall para a instalação
            # sshcommit('sudo iptables -F')

            print('\n-- INSTALAÇÃO --')
            # Instalando as dependências
            ssh(client, 'sudo rpm -Uvh https://repo.zabbix.com/zabbix/5.0/rhel/7/x86_64/zabbix-agent-5.0.22-1.el7.x86_64.rpm')
            # Instalando o ZABBIX-AGENT
            
            
            ssh(client, 'sudo yum -y install zabbix-agent')
            # Iniciando o ZABBIX-AGENT
            ssh(client, 'sudo systemctl start zabbix-agent')

            print('\n-- EDITANDO ZABBIX_AGENTD.CONF --')
            # SERVIDOR
            ssh(client, "sudo sed -i 's/Server=127.0.0.1/Server={}/g' /etc/zabbix/zabbix_agentd.conf".format(zabbix_server_ip))
            # SERVIDOR ATIVO
            ssh(client, "sudo sed -i 's/ServerActive=127.0.0.1/ServerActive={}/g' /etc/zabbix/zabbix_agentd.conf".format(zabbix_server_ip))
            # HOSTNAME
            ssh(client, "sudo sed -i 's/Hostname=Zabbix server/Hostname={}/g' /etc/zabbix/zabbix_agentd.conf".format(zabbix_hostname))
            # HOSTMETADATAITEM (utilizando sed por problemas de permissão AWS)
            ssh(client, "sudo sed -i 's,# HostMetadataItem=,HostMetadataItem=release,g' /etc/zabbix/zabbix_agentd.conf")
            # USERPARAMETER (utilizando sed por problemas de permissão AWS)
            ssh(client, "sudo sed -i 's@# UserParameter=@UserParameter=release,cat /etc/redhat-release@g' /etc/zabbix/zabbix_agentd.conf")

            print('\n-- FINALIZANDO INSTALAÇÃO --')
            # Adicionando ZABBIX à lista de sudoers
            ssh(client, 'echo "%zabbix ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers')
            # Reiniciando o agent
            ssh(client, 'sudo systemctl restart zabbix-agent')
            # Permitindo que o ZA inicie no boot
            ssh(client, 'sudo systemctl enable zabbix-agent')

            print('\n-- SUBINDO FIREWALL --')
            print('- nao implementado -')
            # Reativando o Firewall
            # sshcommit('sudo bash /etc/firewall.sh')

            # Finalizando as sessões abertas no usuário remoto
            print('\n-- FINALIZANDO SESSÃO PARAMIKO --')
            client.close()
            # conexao bem sucedida
            
            # instalação finalizada
            return render_template('success.html')
        
    elif request.method =='GET':
        return render_template('start_menu.html')
    else:
        redirectTo("/erro")

if __name__ == "__main__":
    app.run()
    
# rodar no terminal 
# flask --app "[nome arquivo]" run
# após, dar CTRL C no terminal p/ parar o server