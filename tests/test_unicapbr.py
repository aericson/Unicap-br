# -*- coding: utf-8 -*-
import unittest
from unicap_br import unicap_br
from mock import Mock
from datetime import date, timedelta

CONFIG = "test.cfg"

class MockRequest(Mock):

    def geturl(self):
        if self.http == unicap_br.LOGIN_PAGE:
            return "http://wwww.example.com"
        else:
            return self.http

    def read(self):
        if self.http == unicap_br.LOGIN_PAGE:
            return open("docs/login_response.html").read()
        elif self.http == unicap_br.RENOV_PAGE:
            return open("docs/renov_page.html").read()
        else:
            raise AssertError("Unexpected url")

class MockBrowser(Mock):

    def open(self, http):
        self.http = http
        mock = MockRequest()
        mock.http = self.http
        return mock

    def submit(self):
        mock = MockRequest()
        mock.http = self.http
        return mock

class MockTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock = MockBrowser()

    def test_get_file(self):
        self.mock.open(unicap_br.LOGIN_PAGE)
        self.mock.submit()

class UnicapBrTestCase(unittest.TestCase):

    def mock(self):
        mock = MockBrowser()
        mock.form = {}
        self.lib = unicap_br.Library("20091374482", "123456", mock)

    def unmock(self):
        self.lib = unicap_br.Library(self.mat, self.password)

    @classmethod
    def setUpClass(cls):
        with open("tests/test.cfg") as f:
            cls.mat = f.readline()
            cls.password = f.readline()

    def test_login(self):
        self.mock()
        self.assertEqual(self.lib.logon(), 'FOO BAR')
        self.assertEqual(len(self.lib.books), 2)

    def try_login(self):
        try:
            self.lib.logon()
        except unicap_br.LoginError as e:
            print u"LoginError: Não esqueça de mudar a informação em tests/test.cfg"
            raise e

    def test_renov(self):
        self.unmock()
        self.try_login()
        books = self.lib.books
        result = set()
        for i in books:
            new_deadline = date.today() + timedelta(days=15)
            if new_deadline.weekday() == 5:
                new_deadline += timedelta(days=2)
            elif new_deadline.weekday() == 6:
                new_deadline += timedelta(days=1)
            if new_deadline != i.deadline:
                result.append(i)
        done = self.lib.renew_all_old(16)
        if done:
            done = set(done)
        try:
            self.assertEqual(done, result)
        except AssertionError as ex:
            if done is not None or result:
                raise ex

    def test_book_code(self):
        self.mock()
        self.assertEqual(self.lib.logon(), 'FOO BAR')
        self.assertEqual(self.lib.books[0].code, '99249460')
        self.assertEqual(self.lib.books[1].code, '99200056')