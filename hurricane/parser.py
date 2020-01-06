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
        self.soup = self._get_domains_table()
        
        if self.soup is None:
            return None

        for row in self._get_domain_rows():
            yield self._parse_domain_row(row)

    def _get_domains_table(self):
        return self.soup.find(id="domains_table").tbody
    
    def _get_domain_rows(self):
        yield from self.soup.find_all("tr")

    def _parse_domain_row(self, row):
        tds = row.find_all("td")

        domain_id = tds[3].img.get("value")
        domain_name = tds[2].span.text

        return domain_id, domain_name


class RecordParser(Parser):

    def parse(self):
        self.soup = self._get_dns_table()

        if self.soup is None:
            return None

        for row in self._get_dns_rows():
            yield self._parse_dns_row(row)

    def _get_dns_table(self):
        return self.soup.find(id="dns_main_content").table
    
    def _get_dns_rows(self):
        yield from self.soup.find_all("tr", {"class": "dns_tr"})
    
    def _parse_dns_row(self, row):
        tds = row.find_all("td")

        record_id = tds[1].text
        record_name = tds[2].text
        record_content = tds[6].text
        record_type = tds[3].span.text

        return record_id, record_name, record_content, record_type
