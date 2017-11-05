# Gandi LiveDNS zone manager

The goal of this tool is to display and version the Gandi DNS records of a zone, through the LiveDNS API.

You will need your API key from the Security page in
[your Gandi account](https://account.gandi.net/).
Store it in a `api_key.txt` file, or in an environment variable, like in the following example:

```bash
$ export GANDI_API_KEY=your_api_key
$ python3 livedns.py view
== Zone test-zone [587549ec-c25f-11e7-9d8f-00163e6dc886] ==
        No domain associated with this zone.
        1 records in this zone:

        CNAME   10800   example                example.org.
```

## Usage

```bash
# View all records for all zones
python3 livedns.py view
# Pull the records and store them in the /zones folder
python3 livedns.py pull
ls -l zones
# Create a new zone
python3 livedns.py new test-zone
# Push (upload) the local records stored in /zones to the API
python3 livedns.py push
```

## Requirements

Python 3 with the `requests` module installed.
