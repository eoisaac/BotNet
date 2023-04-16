def read_text_file(file_path):
    with open(file_path) as file:
        for line in file:
            yield line.strip()