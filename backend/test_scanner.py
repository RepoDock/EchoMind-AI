from scanner.scanner import scan_folder

files = scan_folder(r"C:\Users\HP\Downloads")

for file in files:
    print(file)