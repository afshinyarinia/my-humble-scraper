import re


def clean_data(content):
    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content).strip()

    # Remove special characters
    content = re.sub(r'[^\w\s]', '', content)

    # Convert to lowercase
    content = content.lower()

    return content


def read_urls_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]