#!/usr/bin/python2
# Andre Ericson
import unicap_br
from optparse import OptionParser
import sys


def main():
    parser = OptionParser(usage="./%prog -m MATRICULA -p SENHA -d DIAS", version="%prog 0.1")
    parser.add_option('-d','--dias', dest='dias', help='Numero de dias faltando para realizar a renovacao')
    parser.add_option('-m', '--matricula', dest='matricula')
    parser.add_option('-p', '--password', dest='password', help='Senha da biblioteca') 
    (options, args) = parser.parse_args()
    if not options.dias or not options.matricula or not options.password:
        parser.print_help()
        sys.exit(1)
    try:
        l = unicap_br.Library(options.matricula, options.password)
    except AssertionError:
        print 'Nao foi possivel fazer o login, provavelmente senha/mat invalida.'
        sys.exit(1)
    renovados = l.renew_all_old(options.dias) 
    if renovados:
        print 'Os seguintes titulos foram renovados:'
        for i in renovados:
            print i.title, 'para o dia', i.deadline.strftime('%d/%m/%Y')
    else:
        print ('Nenhum livro foi renovado. Livro(s) deve(m) estar reservado(s) ou '
        'a data de devolucao ja esta entre 15-17 dias.')

if __name__ == '__main__':
    main()
