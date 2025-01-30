import argparse
import os
from docx import Document
from configparser import ConfigParser
import ipaddress
from fuzzywuzzy import fuzz
import json
import xml.etree.ElementTree as ET
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

def search_files(directory, extensions, search_terms):
    # Initialize the files_found dictionary to store results
    files_found = {term: {"text": set(), "json": set(), "xml": set()} for term in search_terms}
    threshold = 75  # Lowering the threshold to 30 for partial matching

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Skip Excel files here and handle them separately
            if file_name.endswith('.xlsx'):
                try:
                    workbook = openpyxl.load_workbook(file_path, read_only=True)
                    for sheet in workbook.worksheets:
                        for row in sheet.iter_rows():
                            for cell in row:
                                cell_value = cell.value
                                for term in search_terms:
                                    handle_search(term, str(cell_value), file_path, files_found, threshold)
                except openpyxl.utils.exceptions.InvalidFileException:
                    pass  # Skip invalid Excel files
                continue  # Skip the file if it's an Excel file

            # Process other file types like .txt, .log, etc.
            if file_name.endswith(tuple(extensions)):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        for term in search_terms:
                            handle_search(term, line, file_path, files_found, threshold)

            # Handle .docx files
            elif file_name.endswith('.docx'):
                try:
                    document = Document(file_path)
                    for paragraph in document.paragraphs:
                        for term in search_terms:
                            handle_search(term, paragraph.text, file_path, files_found, threshold)
                except Exception as e:
                    pass  # Skip any errors related to .docx files

            # Handle .ini files (ConfigParser)
            elif file_name.endswith('.ini'):
                try:
                    config = ConfigParser()
                    config.read(file_path)
                    for section in config.sections():
                        for option, value in config.items(section):
                            for term in search_terms:
                                handle_search(term, option, file_path, files_found, threshold)
                                handle_search(term, value, file_path, files_found, threshold)
                except Exception as e:
                    pass  # Skip any errors related to .ini files

            # Handle .json files
            elif file_name.endswith('.json'):
                try:
                    with open(file_path, 'r') as json_file:
                        json_data = json.load(json_file)
                        json_content = json.dumps(json_data)
                        for term in search_terms:
                            handle_search(term, json_content, file_path, files_found, threshold)
                except Exception as e:
                    pass  # Skip any errors related to .json files

            # Handle .xml files
            elif file_name.endswith('.xml'):
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()
                    xml_content = ET.tostring(root, encoding='unicode', method='xml')
                    for term in search_terms:
                        handle_search(term, xml_content, file_path, files_found, threshold)
                except Exception as e:
                    pass  # Skip any errors related to .xml files

    return files_found

# Helper function to search terms in content and store results
def handle_search(term, content, file_path, files_found, threshold):
    if term.startswith('IP-') or term.startswith('MAC-'):
        handle_ip_mac_search(term, content, file_path, files_found)
    elif fuzz.partial_ratio(term.lower(), content.lower()) >= threshold:
        if file_path.endswith('.json'):
            files_found[term]["json"].add(file_path)
        elif file_path.endswith('.xml'):
            files_found[term]["xml"].add(file_path)
        else:
            files_found[term]["text"].add(file_path)

# Handle searches for IP and MAC addresses
def handle_ip_mac_search(term, content, file_path, files_found):
    if term.startswith('IP-'):
        ip_term = term[3:]
        if is_ip_match(ip_term, content):
            files_found[term]["text"].add(file_path)
    elif term.startswith('MAC-'):
        mac_term = term[4:]
        if is_mac_match(mac_term, content):
            files_found[term]["text"].add(file_path)

# Check if the IP matches
def is_ip_match(term, content):
    try:
        ip_address_obj = ipaddress.ip_address(content.strip())
        if isinstance(ip_address_obj, ipaddress.IPv4Address) and isinstance(ipaddress.ip_address(term.strip()), ipaddress.IPv4Address):
            return str(ip_address_obj).startswith(str(term.strip()))
    except ValueError:
        return False

# Check if the MAC address matches
def is_mac_match(term, content):
    sanitized_content = ''.join(c.lower() for c in content if c.isalnum())
    sanitized_term = ''.join(c.lower() for c in term if c.isalnum())
    return sanitized_content.startswith(sanitized_term)

# Main function to parse arguments and execute search
def main():
    parser = argparse.ArgumentParser(description="Search for keyword(s), IP addresses, MAC addresses, and sections/values in .txt, .log, .csv, .xlsx, .docx, .ini, .json, and .xml files.")
    parser.add_argument("-D", "--directory", dest="directory", help="Directory to search for files. Enclose in double quotes if it contains spaces.")
    parser.add_argument("-K", "--keywords", dest="keywords", help="Keywords separated by commas.")
    parser.add_argument("-I", "--ip", dest="ip_addresses", help="IP addresses separated by commas. Enclose in double quotes.")
    parser.add_argument("-M", "--mac", dest="mac_addresses", help="MAC addresses separated by commas. Enclose in double quotes.")

    args = parser.parse_args()

    directory = os.path.abspath(args.directory) if args.directory else None
    extensions = ['log', 'txt', 'xlsx', 'csv', 'docx', 'ini', 'json', 'xml']
    keywords = [keyword.strip() for keyword in args.keywords.split(',')] if args.keywords else []
    ip_addresses = [ip.strip() for ip in args.ip_addresses.split(',')] if args.ip_addresses else []
    mac_addresses = [mac.strip() for mac in args.mac_addresses.split(',')] if args.mac_addresses else []

    search_terms = keywords + [f"IP-{ip}" for ip in ip_addresses] + [f"MAC-{mac}" for mac in mac_addresses]

    files_found = search_files(directory, extensions, search_terms)

    # Print results
    for term, file_types in files_found.items():
        unique_text_files = set(file_types["text"])
        unique_json_files = set(file_types["json"])
        unique_xml_files = set(file_types["xml"])

        if len(unique_text_files) > 0:
            print(f"Found {len(unique_text_files)} text file(s) containing the keyword '{term}':")
            for file_path in unique_text_files:
                print(file_path)
        if len(unique_json_files) > 0:
            print(f"Found {len(unique_json_files)} JSON file(s) containing the keyword '{term}':")
            for file_path in unique_json_files:
                print(file_path)
        if len(unique_xml_files) > 0:
            print(f"Found {len(unique_xml_files)} XML file(s) containing the keyword '{term}':")
            for file_path in unique_xml_files:
                print(file_path)
        if len(unique_text_files) == 0 and len(unique_json_files) == 0 and len(unique_xml_files) == 0:
            print(f"No files containing the keyword '{term}' were found.")

if __name__ == "__main__":
    main()
