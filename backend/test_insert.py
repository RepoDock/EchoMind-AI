from scanner.scanner import scan_folder
from database.crud import insert_file

folder_path = r"C:\Users\HP\Downloads"

files = scan_folder(folder_path)

for file in files:
    insert_file(file)

print("Files inserted successfully!")