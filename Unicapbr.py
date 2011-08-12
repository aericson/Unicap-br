#!/usr/bin/python2
"""
    Modulo para se comunicar
    com o site da biblioteca
    da UNICAP
    ~Andre Ericson(de.ericson@gmail.com)

    PS: don't be gay about print's, nao eh final
"""
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup
import re
from datetime import date

LOGIN_PAGE = 'http://www.unicap.br/pergamum/Pergamum/biblioteca_s/php/login_usu.php'
RENOV_PAGE = 'http://www.unicap.br/pergamum/Pergamum/biblioteca_s/php/au_pendente.php?titpag=%20Renova%E7%E3o&tipo=renovacao&flag=index.php'

class Book(object):
    
    def __init__(self, soup_tag):
       tds = soup_tag.findAll('td')
       self.check = str(tds[0].find('input')['name'])
       self.title = tds[2].string.strip()
       self.deadline = date(*map(int, tds[6].string.strip().split('/')[::-1]))
    
    """
        dias faltando pra devolver
    """
    def days_left(self):
        return (self.deadline - date.today()).days

    def __str__(self):
        return 'Livro: %s Data: %s' % (self.title,
                                       self.deadline.strftime('%d/%m/%Y'))

    def __repr__(self):
        return "'%s'" % str(self)


class Library(object):

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self._login()

    """
        Lista e livros locados
    """
    def get_books(self):
        r = self.browser.open(RENOV_PAGE)
        self.browser.select_form(name='form1')
        soup = BeautifulSoup(r)
        books = soup.findAll('tr',attrs={'class': re.compile('rel.*')})
        return [Book(book) for book in books]
    
    """
        Faz o login, deixe que __init__ chama essa func
    """
    def _login(self):
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
        print 'LOGGED AS ' + ' '.join(self.browser.title().split()[2:])
        self.books = self.get_books()    

    """
        Renova todos os livros com numero de dias faltando
        menor que days.
    """
    def renew(self, days=10):
        any_book = False
        for book in self.books:
            if book.days_left() < days: 
                any_book = True
                print 'gonna try %s' % book.title
                check_box = self.browser.find_control(book.check).items[0]
                check_box.selected = True
        
        if any_book:
            self.browser.submit()
            books = self.get_books() 
            any_book = False
            for book_old, book_new in zip(self.books, books):
                if book_old.deadline != book_new.deadline:
                    any_book = True
                    print ('%s renovado para o dia %s.' %
                        book_new.title, book_new.deadline.strftime('%d/%m/%Y'))
        if not any_book:
            print 'Nenhum livro renovado.'
