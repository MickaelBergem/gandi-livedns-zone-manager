"""
Update the DNS zone for a given domain using Gandi's LiveDNS API
"""
import sys

import requests
from utils import bcolors, load_api_key, print_record

API_URL = 'https://dns.api.gandi.net/api/v5'
API_KEY = load_api_key()


def api_call(url, method='GET', payload=None):
    """
    Call the API with the given method, route, and payload and
    return the Response object
    """
    if payload is None:
        payload = {}

    if url.startswith('/'):
        url = API_URL + url

    response = requests.request(method, url, data=payload, headers={'X-Api-Key': API_KEY})

    return response


def print_zones():
    """ Print all the available zones """
    # List the zones
    zones = api_call('/zones').json()
    for zone in zones:
        print(bcolors.HEADER + "== Zone {zone[name]} ==".format(zone=zone) + bcolors.ENDC)
        # Retrieve the records for this zone
        records = api_call(zone['zone_records_href']).json()
        print("{count} {bcolors.MINOR}records in this zone:{bcolors.ENDC}".format(count=len(records), bcolors=bcolors))
        # Print each record
        for record in records:
            print_record(record)


if __name__ == '__main__':
    if not API_KEY:
        print("You must specify the GANDI_API_KEY environment variable to use this script "
              "(or set it inside the file)")
        sys.exit(1)

    print_zones()
