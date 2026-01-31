
import zipfile
import re
import os
import sys

def extract_text_from_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml').decode('utf-8')
            # Rudimentary XML parsing to get text inside <w:t> tags
            text_parts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml_content)
            return "".join(text_parts)
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

if __name__ == "__main__":
    # Adjust path to the docx found earlier
    target_file = r"G:\マイドライブ\Genesis_OS\02_仕事\99_アーカイブ\転職活動_2022\職務経歴書、履歴書\職務経歴書_20220123.docx"
    if os.path.exists(target_file):
        print(extract_text_from_docx(target_file))
    else:
        print(f"File not found: {target_file}")
