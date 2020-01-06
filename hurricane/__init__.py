#!/usr/bin/env python3

"""
"""

from os import getenv
from requests import Session

from hurricane.parser import LoginVerification, ZoneParser, RecordParser


class HurricaneElectric(object):
    
    def __init__(self):
        self.zones = {}
        self.records = {}

        self.session = Session()
        self._start_session()

        response = self._login()

        self._verify_login(response.text)
        self._parse_zones(response.text)

        self._parse_all_records()

    def _request(self, url, method="POST", **kwargs):
        return self.session.request(method, url, **kwargs)

    def _start_session(self):
        url = "https://dns.he.net"

        self._request(url, "GET")
    
    def _login(self):
        url = "https://dns.he.net"
        payload = {
            "email": getenv("HE_USERNAME"),
            "pass": getenv("HE_PASSWORD"),
            "submit": "Login!"
        }

        return self._request(url, data=payload)

    def _verify_login(self, response):
        if not LoginVerification(response).parse():
            # TODO: Fail with grace
            print("Login failed")
            exit(1)

    def _parse_zones(self, response):
        for domain_id, domain_name in ZoneParser(response).parse():
            self.zones[domain_name] = domain_id
            self.records[domain_id] = {}
    
    def _parse_all_records(self):
        for zone in self.records.keys():
            url = f"https://dns.he.net/?hosted_dns_zoneid={zone}&menu=edit_zone&hosted_dns_editzone"
            response = self.session.get(url)

            self._parse_records(zone, response.text)

    def _parse_records(self, zone, response):
        for record_id, record_name, record_content, record_type in RecordParser(response).parse():
            if record_type == "TXT":
                self.records[zone][record_id] = (record_name, record_content)
    
    def get_zone_id(self, domain):
        return self.zones.get(domain, None)

    def add_record(self, zone, name, content):
        pass

    def remove_record(self, zone, name, content):
        pass