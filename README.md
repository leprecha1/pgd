# PGD - Python Google Dorks
Retieve dorks from GHDB and link them as incidents once something is being found against a given domain.

## Scrap script
To start scrapping you should

```shell
[venv]$ [venv]python ./ghdb/scrapper.py
``` 

The script will search for dorks from the last 3 years filtering by categories and as default should save the results in the file: googledorks.txt.

## Search for dorks within a given domain

```shell
$ [venv]python ./ghdb/pgd.py
``` 

The script will check for dorks against a domain using google search and webkit selenium, in this way we are acting a human-like also the interaction is made by randomic routines.
