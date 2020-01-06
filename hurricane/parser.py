#/usr/bin/env python3

"""
"""

from bs4 import BeautifulSoup


class Parser(object):
    
    def __init__(self, data):
        self.data = data
        self.soup = BeautifulSoup(self.data, "html.parser")

    def parse(self):
        raise NotImplementedError()


class LoginVerification(Parser):

    def parse(self):
        if self._get_dns_error() is not None:
            return False
        
        if self._get_login_form() is not None:
            return False
        
        return True

    def _get_dns_error(self):
        return self.soup.find(id="dns_error")
    
    def _get_login_form(self):
        forms = self.soup.find_all("form")

        for form in forms:
            if form.get("name") == "login":
                return form
        
        return None


class ZoneParser(Parser):

    def parse(self):
        pass


class RecordParser(Parser):

    def parse(self):
        pass
