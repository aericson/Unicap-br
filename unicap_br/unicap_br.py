#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
    Modulo para se comunicar
    com o site da biblioteca
    da UNICAP
    Depends on:
        - python-mechanize (programmatic web browsing)
        - BeautifulSoup (html parser)
    ~André Ericson(de.ericson@gmail.com)
"""
import re
import mechanize
import cookielib
from datetime import date
from BeautifulSoup import BeautifulSoup

LOGIN_PAGE = ('http://www.unicap.br/pergamum/Pergamum/biblioteca_s/php/login_'
              'usu.php')
RENOV_PAGE = ('http://www.unicap.br/pergamum/Pergamum/biblioteca_s/php/au_pe'
              'ndente.php?titpag=%20Renova%E7%E3o&tipo=renovacao&flag=index.'
              'php')
DEBUG = False


class Book(object):

    def __init__(self, soup_tag):
        tds = soup_tag.findAll('td')
        self.check = str(tds[0].find('input')['name'])
        self.title = tds[2].string.strip()
        self.deadline = date(*map(int, tds[6].string.strip().split('/')[::-1]))

    def days_left(self):
        """
            dias faltando pra devolver
        """
        return (self.deadline - date.today()).days

    def __str__(self):
        return u'Livro: %s Data: %s' % (self.title,
                                       self.deadline.strftime('%d/%m/%Y'))

    def __eq__(self, other):
        return self.title == other.title

    def __ne__(self, other):
        return not self.__eq__(other)


class Library(object):

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self._login()

    def get_books(self):
        """
            Lista de livros locados
        """
        r = self.browser.open(RENOV_PAGE)
        self.browser.select_form(name='form1')
        soup = BeautifulSoup(r, fromEncoding='iso-8859-1')
        books = soup.findAll('tr', attrs={'class': re.compile('rel.*')})
        return [Book(book) for book in books]

    def _login(self):
        """
            Faz o login, deixe que __init__ chama essa func
        """
        self.browser = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(cj)
        self.browser.open(LOGIN_PAGE)
        self.browser.select_form(name='form1')
        self.browser.form['login'] = self.login
        self.browser.form['password'] = self.password
        r = self.browser.submit()
        assert r.geturl() != LOGIN_PAGE
        # TODO: create an exception
        if DEBUG:
            print 'LOGGED AS ' + ' '.join(self.browser.title().split()[2:])
        self.books = self.get_books()

    def _get_control_and_set_value(self, control_name, value):
        control = self.browser.find_control(control_name)
        control.readonly = False
        control.value = value

    def _fill_form_renovar(self, str_selecs):
        self._get_control_and_set_value('renova', 'renovar')
        self._get_control_and_set_value('Selecs', str_selecs)
        self._get_control_and_set_value('acao', 'clicou')

    def renew_book(self, book):
        """
            Renova o livro book
            retorna o novo livro caso tenha renovado
            ou None caso falhe
            Possivel motivos para falha:
                - Reservas feitas
                - O livro já está renovado
        """
        check_box = self.browser.find_control(book.check).items[0]
        check_box.selected = True
        str_selecs = check_box.name + ';'
        self._fill_form_renovar(str_selecs)
        self.browser.submit()
        books = self.get_books()
        for _book in books:
            if _book.title == book.title and _book.deadline != book.deadline:
                if DEBUG:
                    print (u'%s renovado para o dia %s.' %
                            (_book.title, _book.deadline.strftime('%d/%m/%Y')))
                return _book
        else:
            return None

    def renew_all_old(self, days=10):
        """
            Renova todos os livros com numero de dias faltando
            menor que days.
            Renova lista de livros renovados ou None
        """
        str_selecs = ''
        to_do = []
        done = []
        for book in self.books:
            if book.days_left() < days:
                if DEBUG:
                    print u'gonna try %s' % book.title
                to_do.append(book)
                check_box = self.browser.find_control(book.check).items[0]
                check_box.selected = True
                str_selecs += check_box.name + ';'

        if str_selecs:
            self._fill_form_renovar(str_selecs)
            self.browser.submit()
            books = self.get_books()
            cmp_title = lambda x, y: x.title < y.title
            for book_old, book_new in zip(
                                    sorted(self.books, cmp=cmp_title),
                                    sorted(books, cmp=cmp_title)):
                if book_old.deadline != book_new.deadline:
                    if DEBUG:
                        print (u'%s renovado para o dia %s.' %
                            (book_new.title,
                                book_new.deadline.strftime('%d/%m/%Y')))
                    done.append(book_new)

                elif DEBUG and book_new in to_do:
                    print u'nao consegui renovar %s' % book_new.title
            self.books = books
        if not done:
            if DEBUG:
                print 'Nenhum livro renovado.'
            return None
        return done
