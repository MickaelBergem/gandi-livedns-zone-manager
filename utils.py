class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    MINOR = '\033[37m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_record(record):
    """ Pretty-print the record """
    for rec_value in record['rrset_values']:
        print(
            " {rec[rrset_type]}\t"
            "{bcol.MINOR}{rec[rrset_ttl]}{bcol.ENDC}\t"
            "{rec[rrset_name]: <20}\t"
            "{value}"
            .format(rec=record, value=rec_value, bcol=bcolors)
        )
