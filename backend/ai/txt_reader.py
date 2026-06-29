def extract_txt_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            return file.read()

    except Exception as e:
        print(f"TXT Error: {e}")
        return ""