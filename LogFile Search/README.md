# Python Logfile Search
This script allows you to search a directory of log files and files in general for keyword(s). If you've ever had to troubleshoot
 an issue and had to look through endless log files for what you wanted, this will help speed up that time.

 > Currently works on the following file formats: .log,.txt,.csv,.xlsx and .docx
> > Requires Docx, openpyxl and requests modules to be installed.

<br />
<br />

## Usage example
```sh
python LogSearch2.py -h
usage: LogSearch2.py [-h] folder_path keywords

Search for keyword(s) in .txt, .log, .csv, .xlsx, and .docx files.

positional arguments:
  folder_path  Path of the folder or directory to search (wrap in double quotes if directory name contains spaces)
  keywords     Keywords can be single word or number, seperated by a comma. Example: payload or 10.0.0.1 or video's.

options:
  -h, --help   show this help message and exit
```

```  
Single keyword: python LogSearch.py c:\temp\logs payload

Multiple keywords:  python LogSearch.py c:\temp\logs payload,10.0.0.1,agent,overboard

 ```

# Single Keyword Search
```sh
Enter the path of the folder or directory to search (wrap in double quotes if it contains spaces): C:\temp\
Enter one or more keywords to search for (separated by commas): payload

Found 2 file(s) containing the keyword 'payload':
C:\temp\logs\collector.log
C:\temp\logs\ingress.log
```
![alt text](https://github.com/rrice2004/Python-/blob/main/LogFile%20Search/images/LogSearch_1.png)
<br />
<br />

# Multiple Keyword Search
```sh
Enter the path of the folder or directory to search (wrap in double quotes if it contains spaces): C:\temp\
Enter one or more keywords to search for (separated by commas): payload,10.0.0.1

Found 2 file(s) containing the keyword 'payload':
c:\temp\logs\collector.log
c:\temp\logs\ingress.log
Found 2 file(s) containing the keyword '10.0.0.1':
c:\temp\Book1.csv
c:\temp\logs\nsc.log
```
![alt text](https://github.com/rrice2004/Python-/blob/main/LogFile%20Search/images/LogSearch_2.png)

<br />

```sh
Enter the path of the folder or directory to search (wrap in double quotes if it contains spaces): c:\temp\
Enter one or more keywords to search for (separated by commas): payload,10.0.0.1,web-engine,workflow
Found 2 file(s) containing the keyword 'payload':
c:\temp\logs\collector.log
c:\temp\logs\ingress.log
Found 5 file(s) containing the keyword '10.0.0.1':
c:\temp\Book1.csv
c:\temp\logs\Book2.csv
c:\temp\logs\nsc.log
c:\temp\logs\New folder\Book3.csv
c:\temp\logs\New folder\Book3.csv
Found 3 file(s) containing the keyword 'web-engine':
c:\temp\logs\auth.log
c:\temp\logs\nsc.log
c:\temp\logs\nse.log
Found 3 file(s) containing the keyword 'workflow':
c:\temp\logs\eso.log
c:\temp\logs\nsc.log
c:\temp\logs\nse.log
```
![alt text](https://github.com/rrice2004/Python-/blob/main/LogFile%20Search/images/LogSearch_3.png)

<br />
<br />
<br />

## Release History
* 0.0.2
    * Added ArgeParse function
    * Validated if keyword is not found, it's listed in the output.
* 0.0.1
    * Work in progress

<br />

## Upcoming Changes
* Create a stand alone executable so python doesn't have to be installed.
* Fix issues with deep search directories.
* Add more file formats for searching.
   
<br />
<br />
<br />

## Known Issues

1. Anything more than three directories deep, multiple results will return for the same keyword.


