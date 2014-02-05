#!/usr/bin/python2
# -*- coding:utf-8 -*-
# Andre Ericson
import unicap_br
import sys
import android

def main():
    dias = 20
    f = open('unicap.txt')
    matricula = f.readline()
    senha = f.readline()
    f.close()


    try:
        l = unicap_br.Library(matricula, senha)
	l.logon()
    except AssertionError:
        print (u'Não foi possível fazer o login, provavelmente senha/mat '
               u'inválida.')
        sys.exit(1)
    renovados = l.renew_all_old(dias)

    droid = android.Android()
    if renovados:
        for i in renovados:
            droid.notify('Unicap-br', i.title[:20] + '... para o dia ' +
                         i.deadline.strftime('%d/%m/%Y'))
    else:
        droid.notify('Unicap-br', 'Nenhum livro renovado.')

if __name__ == '__main__':
    main()
