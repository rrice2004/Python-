# Python Logfile Search

A command‑line log and artifact search utility designed to support SOC operations, digital forensics, and incident response (DFIR) workflows. The script enables analysts to quickly locate indicators of interest—such as keywords, IP addresses (including CIDR ranges), and MAC addresses—across large collections of logs and host‑based artifacts.
Built for investigative use, the tool helps reduce manual review time during triage, threat hunting, and post‑incident analysis, allowing responders to identify relevant evidence faster and focus effort where it matters most.

Supported File Formats
The script currently supports searching across the following evidence and log formats commonly encountered during investigations:

.ini
.log
.txt
.csv
.xlsx
.docx
<br />
<br />

## Installation

```
Built and tested with Python 3.10.11

See requirements.txt for required modules and pinned versions.

```

## Usage example


```sh
python LogFileSearch.py -h
usage: LogFileSearch.py [-h] -D DIRECTORY [-K KEYWORDS] [-I IP_ADDRESSES]
                        [-M MAC_ADDRESSES] [-P] [--case CASE_ID] [--quiet]

Multi‑File Search Utility (SOC / DFIR)

options:
  -h, --help            show this help message and exit
  -D DIRECTORY          Directory to search. Quote only if the path contains spaces.
  -K KEYWORDS           Comma‑separated keywords or phrases.
  -I IP_ADDRESSES       Comma‑separated IP addresses or CIDR ranges.
  -M MAC_ADDRESSES      Comma‑separated MAC addresses.
  -P, --prefix          Enable prefix matching for IP and MAC searches.
  --case CASE_ID        Optional case or incident identifier.
  --quiet               Minimal output for scripting or automation.

INPUT NOTES:
  • Values are comma‑separated
  • Do NOT quote individual values
  • Quote the entire argument only when spaces are present (Windows & Linux)

```

# Single Keyword Search
```sh  
python LogFileSearch.py -D c:\temp -K payload

Found 1 file(s) containing the keyword 'payload':
c:\temp\New Text Document.txt

 ```

# Multiple Keyword Search
```sh
python LogFileSearch.py -D c:\temp -K payload,.net

Found 1 file(s) containing the keyword 'payload':
c:\temp\New Text Document.txt
Found 1 file(s) containing the keyword '.net':
c:\temp\UninstalItems.log
```
> Keywords containing spaces must be passed as a single quoted argument:
> -K "file server,login failure"

<br />
<br />

# Single IP Search
```sh
python LogFileSearch.py -D C:\temp -I 10.0.0.1

Found 1 file(s) containing the keyword 'IP-10.0.0.1':
c:\temp\New Text Document.txt
```
<br />
<br />

# CIDR IP Search
```sh
python LogFileSearch.py -D C:\temp -I 192.168.1.0/24

[FOUND] IP-192.168.1.0/24 -> C:\temp\UninstallItems.log
[FOUND] IP-192.168.1.0/24 -> C:\temp\New Text Document.txt

```
<br />
<br />

# Prefix IP Search (Opt‑In)
```sh
python LogFileSearch.py -D C:\temp -P -I 192.168.1.

[FOUND] IP-192.168.1. -> C:\temp\New Text Document.txt
```
<br />
<br />

# Single Mac Address Search
```sh
python LogFileSearch.py -D c:\temp -M "AA:BB:CC:11:22:33"

Found 2 file(s) containing the keyword 'MAC-AA:BB:CC:11:22:33':
c:\temp\rips\export.ini
c:\temp\rips\export.log
```
<br />
<br />

# Prefix MAC Address Search (Opt‑In)
```sh
python LogFileSearch.py -D C:\temp -P -M AA:BB:CC

[FOUND] MAC-AA:BB:CC -> C:\temp\rips\export.ini
```
> Mac addresses can be etnered in any of the following formats: AA:BB:CC:11:22:33, AABBCC112233, AA-BB-CC-11-22-33.

<br />
<br />

# Combined Search Example
```sh
python LogFileSearch.py \
  -D C:\temp \
  -K "adobe,file server" \
  -I 192.168.1.1,10.0.0.0/8 \
  -M AA:BB:CC:11:22:33 \
  --case IR-2026-0041

[FOUND] adobe                 -> C:\temp\UninstallItems.log
[FOUND] file server           -> C:\temp\New Text Document.txt
[FOUND] IP-192.168.1.1        -> C:\temp\New Text Document.txt
[FOUND] IP-10.0.0.0/8         -> C:\temp\rips\export.ini
[FOUND] MAC-AA:BB:CC:11:22:33 -> C:\temp\rips\export.log

```


<br />
<br />
<br />

## Release History
* 0.1.0
    * Complete rewrite, added the following fixes and upgrades:
       * Quote safe argument sanitization for keywords, IPs, and MACs
       * Explicit Windows vs Linux quoting guidance in --help output
       * Support for CIDR notation in IP searches (e.g. 10.0.0.0/8, 192.168.1.0/24)
       * Optional prefix matching for IP addresses (-P / --prefix)
       * Optional prefix matching for MAC addresses (-P / --prefix)
       * Separate prefix matching functions for IPs and MACs
       * Explicit opt-in prefix mode (default behavior unchanged)
       * Improved IP regex extraction from mixed content
       * Validation and warning for invalid IP or CIDR input
       * Colored terminal output (auto disabled with --quiet)
       * --quiet flag for minimal / script friendly output
       * --case flag for incident or case identifier tagging
       * Improved argparse help formatting (RawTextHelpFormatter)
       * Consistent processing across subdirectories
       * Dedicated processing handlers for TXT, CSV, XLSX, DOCX, INI, JSON, XML
       * Unified result structure by file type (text / json / xml)
      *  Fuzzy keyword matching with adjustable threshold
       * Explicit separation of strict matching vs prefix matching logic







* 0.0.6
    * Fixed issues with OS Walk and openpyxl.
* 0.0.5
    * Added .xml and .json file search function.
* 0.0.4
    * Added .ini file search function.
    * Rewrote the argparse so that it functions correctly with switches.
    * Fixed the IP and MAC search function to take use input correctly.
* 0.0.3
    * Added fuzzywuzzy function to help with potential partial matches.
    * Fixed output to where in some instances it was outputting the same file for each instance of a keyword to just listing the single file, regardless of how many times the keyword was found.
* 0.0.2
    * Added ArgeParse function
    * Validated if keyword is not found, it's listed in the output.
* 0.0.1
    * Initial Release.

<br />

## Upcoming Changes
* Create a stand alone executable so python doesn't have to be installed.
* Fix issues with deep search directories.
* Add more file formats for searching.
* Add better IP and MAC address searching.
   
<br />
<br />
<br />
