import glob, subprocess, os, sys, re, copy, json

font = {
    'name': '',
    'type': '',
    'encoding': '',
    'emb': '',
    'sub': '',
    'uni': '',
    'object': '',
    'ID': ''
}

if len(sys.argv) < 2:
    print("Requires folder path.")
    sys.exit()


def get_column_coordinates(dash_line):
    indices = [space.start() for space in re.finditer(' ', dash_line)]
    dashes = dash_line.split(' ')
    widths = [len(dash) for dash in dashes]
    return indices, widths


def get_parsed_fonts(out):
    lines = out.split('\n')
    lines = [line for line in lines if line.strip()]
    column_indices, column_widths = get_column_coordinates(lines[1])
    column_indices.insert(0, 0)

    data = []
    for i in range(len(lines) - 2):
        line = lines[i + 2]

        for j in range(len(font.keys()) - 1):
            start_index = column_indices[j]
            width = column_widths[j]
            font[list(font.keys())[j]] = line[start_index:start_index + width + 1].strip()
        font['ID'] = font['object'].split()[1].strip()
        font['object'] = font['object'].split()[0].strip()
        data.append(copy.deepcopy(font))
    return data


folder_path = os.path.abspath(sys.argv[1])
pattern = os.path.join(folder_path, '**/*.pdf')
for filename in glob.iglob(pattern, recursive=True):
    print(filename)
    # Call pdffonts with the input PDF.
    out = subprocess.Popen(['pdffonts', filename],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT
                           )
    # get the stdout and stderr from bash.
    stdout, stderr = out.communicate()
    # Convert it from bytes to ascii.
    try:
        out = stdout.decode()
        # Parse stdout into fonts.
        data = get_parsed_fonts(out)
    except:
        print("Unable to process fileL {}.".format(filename))
    folder_name, file_name = os.path.split(filename)
    font_filename = file_name.replace('.pdf', '_fonts.json')
    with open(os.path.join(folder_name, font_filename), mode='w') as fonts_file:
        fonts_file.write(json.dumps(data))
