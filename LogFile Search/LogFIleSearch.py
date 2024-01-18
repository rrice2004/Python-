import os
import openpyxl
import re
from docx import Document

# Function to define search criteria. Currently works on .log,.txt,.csv,.xlsx and .docx
def search_files(folder_path, keywords):
    files_found = {keyword: [] for keyword in keywords}

    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs[:]:
            dir_path = os.path.join(root, dir_name)
            for sub_dir, _, _ in os.walk(dir_path):
                dirs.append(sub_dir)
            if os.path.normcase(dir_path) != os.path.normcase(folder_path):
                dirs.remove(dir_name)

        for file_name in files:
            file_path = os.path.join(root, file_name)

            if file_name.endswith(('.txt', '.log', '.csv')):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    for keyword in keywords:
                        if re.search(rf'\b{re.escape(keyword)}\b', content, flags=re.IGNORECASE):
                            files_found[keyword].append(file_path)

            elif file_name.endswith('.xlsx'):
                try:
                    workbook = openpyxl.load_workbook(file_path, read_only=True)
                    for sheet in workbook.worksheets:
                        for row in sheet.iter_rows():
                            for cell in row:
                                cell_value = cell.value
                                for keyword in keywords:
                                    if cell_value is not None and re.search(rf'\b{re.escape(keyword)}\b', str(cell_value), flags=re.IGNORECASE):
                                        files_found[keyword].append(file_path)
                                        break  # stop searching this file once a match is found
                                if file_path in files_found[keyword]:
                                    break  # stop searching this sheet once a match is found
                except openpyxl.utils.exceptions.InvalidFileException:
                    pass  # Ignore invalid XLSX files

            elif file_name.endswith('.docx'):
                try:
                    document = Document(file_path)
                    content = " ".join([paragraph.text for paragraph in document.paragraphs])
                    for keyword in keywords:
                        if re.search(rf'\b{re.escape(keyword)}\b', content, flags=re.IGNORECASE):
                            files_found[keyword].append(file_path)
                except Exception as e:
                    pass  # Ignore errors when processing Word documents

    return files_found

if __name__ == "__main__":
    # Take user input for a folder or directory to begin search along with what key word(s) to search for.
    folder_path = input("Enter the path of the folder or directory to search (wrap in double quotes if it contains spaces): ")


    keywords_input = input("Enter one or more keywords to search for (separated by commas): ")
    keywords = [keyword.strip() for keyword in keywords_input.split(',')]

    # Begin searching provided directory or folder, locating all .txt, .log, .csv, .xlsx, and .docx files containing user provided keyword(s)
    files_found = search_files(folder_path, keywords)

    # Provide an output of the file names where user provided keyword(s) were located
    for keyword, keyword_files in files_found.items():
        if len(keyword_files) > 0:
            print(f"\033[1;33mFound {len(keyword_files)} file(s) containing the keyword '{keyword}':\033[0m")
            for file_path in keyword_files:
                print(f"\033[1;33m{file_path}\033[0m")
        else:
            print(f"\033[1;31mNo files containing the keyword '{keyword}' were found.\033[0m")

