# Python Logfile Search
This script allows you to search a directory of log files and files in general for keyword(s). If you've ever had to troubleshoot
 an issue and had to look through endless log files for what you wanted, this will help speed up that time.

 > Currently works on the following file formats: .log,.txt,.csv,.xlsx and .docx

<br />
<br />

## Usage example

Say you have a directory of 40-50 log files and you qiuckly need to find which log files contain a keyword or a set or keywords,
run this script to find out which ones you need to look at.  
<br />
<br />
Example:
Say you needed to find which log files containt he keyword "payload." Provide the script the directory of your logs and the keyword
and let it search for you.  

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

![alt text](https://github.com/rrice2004/Python-/blob/main/LogFile%20Search/images/LogSearch_3.png)

<br />
<br />
<br />

## Release History
* 0.0.1
    * Work in progress

<br />
<br />
<br />

## Known Issues

1. Anything more than three directories deep, multiple results will return for the same keyword.


