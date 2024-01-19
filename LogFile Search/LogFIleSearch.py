# Requires Docx, openpyxl, fuzzywuzzy and requests modules to be installed.
# A log file search to speed up troubleshooting and threat hunting. With the ability to
# search for individual, multiple keywords at a time as well as IP and MAC addresses.

import os
import openpyxl
from docx import Document
import argparse
from fuzzywuzzy import fuzz
import ipaddress

# Function to define search criteria. Currently works on .log, .txt, .csv, .xlsx, and .docx
def search_files(folder_path, search_terms):
    files_found = {term: set() for term in search_terms}
    threshold = 30  # Lowering the threshold to 30 for partial matching

# Directory to search
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs[:]:
            dir_path = os.path.join(root, dir_name)
            for sub_dir, _, _ in os.walk(dir_path):
                dirs.append(sub_dir)
            if os.path.normcase(dir_path) != os.path.normcase(folder_path):
                dirs.remove(dir_name)

        for file_name in files:
            file_path = os.path.join(root, file_name)
# text,log and csv files
            if file_name.endswith(('.txt', '.log', '.csv')):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        for term in search_terms:
                            if term.startswith('IP-') or term.startswith('MAC-'):
                                handle_ip_mac_search(term, line, file_path, files_found)
                            elif fuzz.partial_ratio(term.lower(), line.lower()) >= threshold:
                                files_found[term].add(file_path)
                                break  # stop searching this file once a match is found
# excel files
            elif file_name.endswith('.xlsx'):
                try:
                    workbook = openpyxl.load_workbook(file_path, read_only=True)
                    for sheet in workbook.worksheets:
                        for row in sheet.iter_rows():
                            for cell in row:
                                cell_value = cell.value
                                for term in search_terms:
                                    if term.startswith('IP-') or term.startswith('MAC-'):
                                        handle_ip_mac_search(term, str(cell_value), file_path, files_found)
                                    elif cell_value is not None and fuzz.partial_ratio(term.lower(), str(cell_value).lower()) >= threshold:
                                        files_found[term].add(file_path)
                                        break  # stop searching this file once a match is found
                                if file_path in files_found[term]:
                                    break  # stop searching this sheet once a match is found
                except openpyxl.utils.exceptions.InvalidFileException:
                    pass  # Ignore invalid XLSX files
# word files
            elif file_name.endswith('.docx'):
                try:
                    document = Document(file_path)
                    for paragraph in document.paragraphs:
                        for term in search_terms:
                            if term.startswith('IP-') or term.startswith('MAC-'):
                                handle_ip_mac_search(term, paragraph.text, file_path, files_found)
                            elif fuzz.partial_ratio(term.lower(), paragraph.text.lower()) >= threshold:
                                files_found[term].add(file_path)
                                break  # stop searching this file once a match is found
                except Exception as e:
                    pass  # Ignore errors when processing Word documents

    return files_found
# ip and mac search
def handle_ip_mac_search(term, content, file_path, files_found):
    if term.startswith('IP-'):
        ip_term = term[3:]
        if is_ip_match(ip_term, content):
            files_found[term].add(file_path)
    elif term.startswith('MAC-'):
        mac_term = term[4:]
        if is_mac_match(mac_term, content):
            files_found[term].add(file_path)

def is_ip_match(term, content):
    try:
        ip_address = ipaddress.ip_address(content.strip())
        if isinstance(ip_address, ipaddress.IPv4Address) and isinstance(ipaddress.ip_address(term.strip()), ipaddress.IPv4Address):
            return str(ip_address).startswith(str(term.strip()))
    except ValueError:
        return False

def is_mac_match(term, content):
    sanitized_content = ''.join(c.lower() for c in content if c.isalnum())
    sanitized_term = ''.join(c.lower() for c in term if c.isalnum())
    return sanitized_content.startswith(sanitized_term)

if __name__ == "__main__":
    # Create an ArgumentParser
    parser = argparse.ArgumentParser(description="Search for keyword(s), IP addresses, and MAC addresses in .txt, .log, .csv, .xlsx, and .docx files.")

    # Add command-line arguments
    parser.add_argument("folder_path", help="Path of the folder or directory to search (wrap in double quotes if directory name contains spaces)")
    parser.add_argument("keywords", help="Keywords can be single word or number, separated by a comma. Example: payload or IP-10.0.0.1 or MAC-AABBCC112233.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract values from parsed arguments
    folder_path = args.folder_path
    keywords = [keyword.strip() for keyword in args.keywords.split(',')]

    # Call the search_files function with the provided folder path and keywords
    files_found = search_files(folder_path, keywords)

    # Display the results to the user
    for term, term_files in files_found.items():
        unique_files = set(term_files)
        if len(unique_files) > 0:
            print(f"\033[1;33mFound {len(unique_files)} file(s) containing the keyword '{term}':\033[0m")
            for file_path in unique_files:
                print(f"\033[1;33m{file_path}\033[0m")
        else:
            print(f"\033[1;31mNo files containing the keyword '{term}' were found.\033[0m")
