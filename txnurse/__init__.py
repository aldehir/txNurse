from __future__ import print_function, absolute_import

import sys
import json
import string
import requests

from bs4 import BeautifulSoup
from argparse import ArgumentParser


REQUEST_URL = "https://www.bon.texas.gov/forms/rnrslt.asp"


def lookup(license):
    data = build_data(license)

    response = requests.post(REQUEST_URL, data=data)
    response.raise_for_status()

    data = parse_response(response)
    data.update({'license': license})

    return data


def build_data(license):
    """Return the data to send in the POST request."""
    return {"LicNumber": str(license),
            "SSNumber": None,
            "DOB": None,
            "firstname": None,
            "lastname": None,
            "B1": "Submit"}


def parse_response(response):
    soup = BeautifulSoup(response.text, "lxml")

    content = extract_content(soup)
    name = extract_name(content)
    items = extract_items(content)

    return {'name': name, 'fields': items}


def extract_content(soup):
    try:
        return extract_first(soup.select('td.content'))
    except LookupError:
        raise NoContentError("No content found")


def extract_name(content):
    try:
        name = extract_first(content.select('h2'))
        return name.text.strip()
    except LookupError:
        raise NoSuchLicenseError('No license found')


def extract_items(content):
    elements = content.select('ul li')
    pairs = [[y.strip() for y in x.text.split(':', 1)] for x in elements]
    return dict(pairs)


def extract_first(items):
    if not items:
        raise LookupError('No items found')
    return items[0]


class LookupError(Exception):
    """Raised when a lookup error occurs."""


class NoContentError(LookupError):
    """Raised when the response page does not contain any content."""


class NoSuchLicenseError(LookupError):
    """Raised when the requested license number yields no results."""


def main():
    import sys
    import json

    args = parse_args(sys.argv[1:])

    try:
        data = lookup(args.license)
    except NoContentError as e:
        print("error: {0}".format(e), file=sys.stderr)
        sys.exit(11)
    except NoSuchLicenseError as e:
        print("error: {0}".format(e), file=sys.stderr)
        sys.exit(12)
    except LookupError as e:
        print("error: {0}".format(e), file=sys.stderr)
        sys.exit(10)
    except Exception as e:
        print("error: {0}".format(e), file=sys.stderr)
        sys.exit(255)

    if args.output:
        with open(args.output, 'w') as f:
            dump(data, f)
    else:
        dump(data, sys.stdout)


def parse_args(args):
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('license', help='license number')
    parser.add_argument('-o', '--output', help='output file')

    return parser.parse_args(args)


def dump(data, f):
    json.dump(data, f, indent=2, separators=(',', ': '))
    f.write('\n')
