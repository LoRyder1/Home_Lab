import csv, re

infile = 'I30-wacsvc-profile.csv'
outfile = 'clean_I30-wacsvc-profile.csv'

with open(infile, 'r', encoding='utf-8', errors='replace') as f_in, \
     open(outfile, 'w', encoding='utf-8', newline='') as f_out:
    
    # 1. Clean NUL bytes and repair trailing quotes on the fly
    cleaned_stream = (re.sub(r',("[\s\d]+)[\r\n]*$', r',\1"', line.replace('\x00', '')).strip() + '\n' for line in f_in)
    
    # 2. Read with QUOTE_NONE to ignore bad quotes, write clean RFC-4180 CSV
    reader = csv.reader(cleaned_stream, delimiter=',', quoting=csv.QUOTE_NONE, escapechar='\\')
    writer = csv.writer(f_out, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    for row in reader:
        writer.writerow([field.strip('"').strip() for field in row])