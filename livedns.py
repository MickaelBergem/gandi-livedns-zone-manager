#!/usr/bin/python3
"""
Update the DNS zone for a given domain using Gandi's LiveDNS API
"""
import argparse
import glob
import os
import re
import sys

import requests
from utils import bcolors, load_api_key, print_record

# API configuration
API_URL = 'https://dns.api.gandi.net/api/v5'
API_KEY = load_api_key()

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ZONES_FOLDER = BASE_DIR + '/zones/'


def api_call(url, method='GET', payload=None, **kwargs):
    """
    Call the API with the given method, route, and payload and
    return the Response object
    """
    if payload is None:
        payload = {}

    if url.startswith('/'):
        url = API_URL + url

    headers = {'X-Api-Key': API_KEY}
    if 'headers' in kwargs:
        headers.update(kwargs.pop('headers'))

    response = requests.request(method, url, data=payload, headers=headers, **kwargs)

    if response.status_code >= 400:
        print(bcolors.FAIL + "The API returned an error:" + bcolors.ENDC)
        print(response.json())
        sys.exit(1)

    return response


def print_zones(*args, **kwargs):
    """ Print all the available zones """
    # List the zones
    zones = api_call('/zones').json()
    for zone in zones:
        print(bcolors.HEADER + "== Zone {zone[name]} [{zone[uuid]}] ==".format(zone=zone) + bcolors.ENDC)

        # List associated domains
        domains = api_call(zone['domains_href']).json()
        if domains:
            print(
                "{bcolors.MINOR}\tDomain(s) associated with this zone:{bcolors.ENDC} {domains}"
                .format(bcolors=bcolors, domains=', '.join([domain['fqdn'] for domain in domains]))
            )
        else:
            print("\tNo domain associated with this zone.")

        # Retrieve the records for this zone
        records = api_call(zone['zone_records_href']).json()
        print("\t{count} {bcolors.MINOR}records in this zone:{bcolors.ENDC}\n".format(count=len(records), bcolors=bcolors))
        # Print each record
        for record in records:
            print_record(record)
        print()


def pull_zones(*args, **kwargs):
    """ Retrieve the zones from the API and store them on disk """
    zones = api_call('/zones').json()
    for zone in zones:
        print(bcolors.HEADER + "== Zone {zone[name]} [{zone[uuid]}] ==".format(zone=zone) + bcolors.ENDC)

        # Retrieve the records for this zone
        records_response = api_call(zone['zone_records_href'], headers={'Accept': 'text/plain'})
        print("\tWriting... ", end='')

        # Save the records in a file
        filename = "{zone[name]}_{zone[uuid]}.txt".format(zone=zone)
        with open(ZONES_FOLDER + filename, 'w') as records_file:
            records_file.write(records_response.content.decode('utf-8'))
        print("{bcolors.OKGREEN}done{bcolors.ENDC} ({fn})".format(fn=filename, bcolors=bcolors))

    print("\n" + bcolors.OKBLUE + "Written all zones in " + ZONES_FOLDER + bcolors.ENDC)


def push_zones(*args, **kwargs):
    """ Push the zones to the API from the zone files on disk """
    zone_files = glob.glob(ZONES_FOLDER + '*_*.txt')
    pattern = re.compile(r'(.*)_(.*)\.txt')
    for zone in zone_files:
        zone_name, zone_uuid = re.match(pattern, os.path.basename(zone)).groups()
        print("{bcolors.MINOR}Found zone{bcolors.ENDC} {name} {bcolors.MINOR}({uuid}){bcolors.ENDC}".format(bcolors=bcolors, name=zone_name, uuid=zone_uuid))

        # Read the zone file
        with open(zone, 'r') as zone_file:
            records_raw = zone_file.read()

        if not records_raw:
            print(bcolors.WARNING + "Empty zone file, aborting!" + bcolors.ENDC)
            continue

        # Print zone content
        # print(bcolors.GRAY + records_raw + bcolors.ENDC)

        # Get the zone info
        zone = api_call('/zones/' + zone_uuid).json()
        if zone['name'] != zone_name:
            print(bcolors.FAIL + "Zone file was renamed, aborting. Please rename the zone file with the new name if you want to continue." + bcolors.ENDC)
            continue

        print("{bcolors.MINOR}\tUploading the zone...{bcolors.ENDC} ".format(bcolors=bcolors), end='')
        resp = api_call(zone['zone_records_href'], method='PUT', payload=records_raw)
        if resp.status_code != 201:
            print(bcolors.FAIL + "\tWrite failed (?)\n" + bcolors.ENDC)
            print("{bcolors.FAIL}{resp}{bcolors.ENDC}".format(bcolors=bcolors, resp=resp.json()))
            sys.exit(1)

        print(bcolors.OKGREEN + 'ok' + bcolors.ENDC)
        print(
            "{bcol.GRAY}\tServer answered: {msg}{bcol.ENDC}"
            .format(msg=resp.json()['message'], bcol=bcolors)
        )


def new_zone(options, *args, **kwargs):
    """ Create a new zone """
    if not options.options:
        print(bcolors.FAIL + "The `new` command requires a `name` argument: the zone name." + bcolors.ENDC)
        sys.exit(1)

    name = options.options[0]

    print("Creating new zone \"{bcolors.BOLD}{name}{bcolors.ENDC}\"... ".format(bcolors=bcolors, name=name), end='')
    resp = api_call('/zones', method='POST', payload={'name': name})
    if resp.status_code == 200:
        print(bcolors.OKGREEN + "done" + bcolors.ENDC + ', uuid=' + resp.json()['uuid'])
    else:
        print(bcolors.FAIL + "error" + bcolors.ENDC)
        print(resp.json())


if __name__ == '__main__':
    if not API_KEY:
        print(bcolors.FAIL + "You must specify the GANDI_API_KEY environment variable "
              "to use this script (or set it inside the file)" + bcolors.ENDC)
        sys.exit(1)

    # Allowed action verbs for the CLI
    ALLOWED_CHOICES = {
        'view': print_zones,
        'pull': pull_zones,
        'new': new_zone,
        'push': push_zones,
    }

    parser = argparse.ArgumentParser(description='Manage LiveDNS zone records')
    parser.add_argument(
        'command',
        choices=ALLOWED_CHOICES.keys(),
        help='the action you want to perform',
    )
    parser.add_argument('options', nargs='*', help="command-specific options")

    args = parser.parse_args()

    ALLOWED_CHOICES[args.command](args)
