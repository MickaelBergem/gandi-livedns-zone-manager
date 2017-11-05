# Gandi LiveDNS zone manager

The goal of this tool is to display and version the Gandi DNS records of a zone, through the LiveDNS API.

You will need your API key from the Security page in [your Gandi account](https://account.gandi.net/).

```bash
$ export GANDI_API_KEY=your_api_key
$ python3 livedns.py
== Zone example.org ==
25 records in this zone:
 MX     10800   @                       50 fb.mail.gandi.net.
 MX     10800   @                       10 spool.mail.gandi.net.
 CNAME  10800   example-cname           blog.securem.eu.
 A      1200    aws-server              1.2.3.4
 A      1200    aws-another-server      5.6.7.8
```

## Requirements

Python 3 with the `requests` module installed.
