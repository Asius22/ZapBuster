import re
import time

_URL_REGEX = r'(http[s]?://[^\s]+)'

def extract_url_from_file(filename):
    res = set()
    try: 
        with open(filename) as file:
            for line in file.readlines():
                
                res.add(extract_url_from_str(line))
            res.remove(None)
            return res
    except OSError:
        print("Il file non esiste oppure non può essere aperto")
        
def extract_url_from_str(str):
    match = match = re.search(_URL_REGEX, str)
    if match:
        return match.group(1)
    
def waiting_print(str):
    
    for i in range(0, 3):
        print("\r" + ' ' * 50 , end="")
        print(f"\r{str} {". " * (i + 1)} ", end="")

        time.sleep(0.5)
        
    print("")

def progress_print(process, progress):
    
    print("\r" + ' ' * 50 , end="")
    print(f"\r{process}: {progress}% ", end="")
    if progress == "100":
        print("")

