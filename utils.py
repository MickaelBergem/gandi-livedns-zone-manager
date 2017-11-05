import os


class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    MINOR = '\033[37m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_record(record):
    """ Pretty-print the record """
    for rec_value in record['rrset_values']:
        print(
            "\t{rec[rrset_type]}\t"
            "{bcol.MINOR}{rec[rrset_ttl]}{bcol.ENDC}\t"
            "{rec[rrset_name]: <20}\t"
            "{value}"
            .format(rec=record, value=rec_value, bcol=bcolors)
        )


def load_api_key():
    """
    Try to load the API key from:
    * the configuration file `api_key.txt`
    * the GANDI_API_KEY environment variable
    If the key is not found, return None.
    """
    try:
        with open('./api_key.txt', 'r') as file:
            key_file = file.read().strip()
    except FileNotFoundError:
        pass
    else:
        if key_file:
            return key_file

    key_env = os.environ.get('GANDI_API_KEY')
    # If the variable is not defined, returns None
    return key_env
