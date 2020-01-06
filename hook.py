#!/usr/bin/env python3

"""
"""

from dns.resolver import Resolver, NXDOMAIN
from dns.exception import DNSException
from dotenv import load_dotenv
from sys import argv
from time import sleep
from tld import parse_tld


from hurricane import HurricaneElectric

load_dotenv()


hurricane = HurricaneElectric()
prefix = "_acme-challenge."


def get_zone_id(domain):
    tld, domain, subdomain = parse_tld(domain, fix_protocol=True)

    if domain is None:
        # TODO: Fail with grace
        exit(1)

    fld = ".".join((domain, tld))

    # TODO: Get zone ID

    return None, fld, subdomain


def dns_lookup(name, resolver=None):
    if resolver is None:
        resolver = Resolver()

    try:
        yield from [str(record) for record in resolver.query(name, "TXT")]
    except NXDOMAIN:
        yield None
    except DNSException as e:
        # TODO: Fail with grace
        print(e)
        exit(1)


def dns_verify(name, content):
    retries = 3
    resolver = Resolver()

    if content is not None:
        content = f"\"{content}\""

    for retry in range(retries):
        sleep(10)

        result = dns_lookup(name, resolver)

        if content in result:
            return True

    return False


def add_record(zone, name, content):
    pass
    # TODO: This


def remove_record(zone, name, content):
    pass
    # TODO: This


def deploy_challenge(*args):
    name = prefix + args[0]
    content = args[2]

    # add_record(zone, name, content)

    dns_verify(name, content)


def clean_challenge(*args):
    name = prefix + args[0]
    content = args[2]

    # remove_record(zone, name, content)

    dns_verify(name, None)


def main():
    try:
        operation, args = argv[1], argv[2:]
    except IndexError:
        # TODO: Fail with grace
        print("Invalid argv!")
        exit(1)

    operations = {
        "deploy_challenge": deploy_challenge,
        "clean_challenge": clean_challenge,
    }

    if operation in operations:
        operations[operation](*args)        


if __name__ == "__main__":
    pass
    # main()
