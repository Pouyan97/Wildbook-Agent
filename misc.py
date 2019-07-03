# 
# Miscellaneous functions to load .properties and WEKA files
# 
# Viktor Kirillov 
# 

import csv

# Reading .properties file, returns a dictionary
def loadProperties(filepath, sep='=', com='#'):
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(com):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = key_value[1].strip()
                props[key] = value
    return props


# Reading WEKA file, returning a dictionary
def loadWEKA(filename, limit=0):
    attributes = [] # Will store csv columns names here
    data = []       # Will store readed file here
    
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar="'")
        
        line_num = 0
        dataBegan = False
        
        for row in reader:
            # Getting info from @ATTRIBUTE's
            if not dataBegan:
                if len(row) > 0:
                    # Extracting @ATTRIBUTE's
                    row_splitted = row[0].split()
                    if row_splitted[0] == "@ATTRIBUTE":
                        attributes.append(row_splitted[1])
                    
                    # If we found that @data started
                    if row[0] == "@data":
                        dataBegan = True
                        continue
            
            # Reading only payload of the file
            if dataBegan:
                if len(row) > 1:
                    # Appending row into data array
                    data.append(row)
                    line_num += 1

                    # Limiting the number of rows to read
                    if line_num > limit and limit > 0:
                        break
        
    return (data, attributes)