#!/usr/bin/env python3

"""
"""

from os import getenv
from requests import Session

from hurricane.parser import LoginVerification


class HurricaneElectric(object):
    
    def __init__(self):
        self.session = Session()
        self._start_session()

        response = self._login()

        self._verify_login(response.text)
        self._parse_zones(response.text)

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
        return None
