# Python Logfile Search
A log file search script to speed up troubleshooting and threat hunting. With the ability to search for individual or multiple keywords, IP addresses and MAC addresses. Help speed up your workflow and save time.

 > Currently works on the following file formats: .ini,.log,.txt,.csv,.xlsx and .docx
 >> Requires python-docx, openpyxl, fuzzywuzzy and python-Levenshtein modules to be installed.

<br />
<br />

## Installation

```
This tool was built with Python 3.10.11
See the requirements.txt file for modules and module versions.
```

## Usage example


```sh
python LogFileSearch.py -h
usage: LogFileSearch.py [-h] [-D DIRECTORY] [-K KEYWORDS] [-I IP_ADDRESSES] [-M MAC_ADDRESSES]

Search for keyword(s), IP addresses, MAC addresses, and sections/values in .txt, .log, .csv, .xlsx, .docx, and .ini
files.

options:
  -h, --help            show this help message and exit
  -D DIRECTORY, --directory DIRECTORY
                        Directory to search for files. Enclose in double quotes if it contains spaces.
  -K KEYWORDS, --keywords KEYWORDS
                        Keywords separated by commas.
  -I IP_ADDRESSES, --ip IP_ADDRESSES
                        IP addresses separated by commas. Enclose in double quotes.
  -M MAC_ADDRESSES, --mac MAC_ADDRESSES
                        MAC addresses separated by commas. Enclose in double quotes.
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
> Keywords that contain a space must be wrapped in double quotes. EX: "file server"

<br />
<br />

# Single IP Search
```sh
python LogFileSearch.py -D c:\temp -I "10.0.0.1"

Found 1 file(s) containing the keyword 'IP-10.0.0.1':
c:\temp\New Text Document.txt
```
<br />
<br />

# Multiple IP Search
```sh
python LogFileSearch.py -D c:\temp -I "10.0.0.1","192.168.1.1"

Found 1 file(s) containing the keyword 'IP-10.0.0.1':
c:\temp\New Text Document.txt
Found 2 file(s) containing the keyword 'IP-192.168.1.1':
c:\temp\UninstalItems.log
c:\temp\New Text Document.txt
```
> IP addresses must be wrapped in double quotes.
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

# Multiple Mac Address Search
```sh
python LogFileSearch.py -D c:\temp -M "AA:BB:CC:11:22:33","0A-00-27-00-00-0E"

Found 2 file(s) containing the keyword 'MAC-AA:BB:CC:11:22:33':
c:\temp\rips\export.ini
c:\temp\rips\export.log
Found 1 file(s) containing the keyword 'MAC-0A-00-27-00-00-0E':
c:\temp\rips\export.ini
```
> Mac addresses can be etnered in any of the following formats: AA:BB:CC:11:22:33, AABBCC112233, AA-BB-CC-11-22-33. They must be wrapped in doubled quotes.

<br />
<br />

# Combination Search
```sh
python LogFileSearch.py -D c:\temp -M "AA:BB:CC:11:22:33" -K adobe,"file server" -I "192.168.1.1"

Found 1 file(s) containing the keyword 'adobe':
c:\temp\UninstalItems.log
Found 1 file(s) containing the keyword 'file server':
c:\temp\New Text Document.txt
Found 3 file(s) containing the keyword 'IP-192.168.1.1':
c:\temp\rips\export.ini
c:\temp\UninstalItems.log
c:\temp\New Text Document.txt
Found 2 file(s) containing the keyword 'MAC-AA:BB:CC:11:22:33':
c:\temp\rips\export.ini
c:\temp\rips\export.log
```


<br />
<br />
<br />

## Release History
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
