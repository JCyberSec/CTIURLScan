# CTIURLScan

CTIURLScan is a command line tool to enable analysts to search URLscan.io submissions. Pull screenshot and DOM content. As well as, automatic extraction of API items to allow for easier ingestion later on.

# Features
- Search URLscan.io
- Define the time to search
- Define the number of results
- Pull PNG of a scan
- Pull DOM of a scan
- Automatic extraction of scanned results

# Flags
- Search
  - -t / --term :: Search Term or string to search in URLScan.io.
  - -s / --size :: Number of results to return. Default is 96
  - -d / --date :: Date to search back for the results. Default is last 24hr
  - -e / --extract :: Item in the JSON to extract.

- Collect
  - -u / --uuid :: UUID of the scan to collect. Can parse multiple UUIDs with a space separator 
  - -d / --dom :: Dump the DOM content of the scan onto screen
  - -s / --screenshot :: Save the screenshot of the scan
  - -v / --dump :: Dump the full content of the response for the scan onto screen

# Sample Usage
## Search
```python
$ python3 main.py search -t 'page.url:"google"' -e url -d 3d
$ python3 main.py collect -u e18a2121-3c81-4fbd-9b61-38770f833052 -d
```

# Benefits of the tool
You can carefully target scans and pipe the output into further processing in the command line. 
The tool allows for easy extract of URLs, UUIDs, IP, Domains etc from the output of the API onto the command line
