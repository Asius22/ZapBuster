import re
import time, subprocess
_URL_REGEX = r"(http[s]?://[^\s]+)"

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
        print("\r" + " " * 50 , end="")
        print(f"\r{str} {". " * (i + 1)} ", end="")

        time.sleep(0.5)

def progress_print(process, progress):
    
    print("\r" + " " * 50 , end="")
    print(f"\r{process}: {progress}% ", end="")
    if progress == "100":
        print("")
        
        

def merge_wordlist(file1, file2, output):
    """_summary
    crea la seguente pipeline:
        stampa file1 e file2
        ordina le righe
        cancella i duplicati
        l"output finale stampalo in output
    """
    # Primo step: `cat file1 file2`
    result1 = subprocess.run(["cat", file1, file2], stdout=subprocess.PIPE, text=True)

    # Secondo step: `sort`, che prende l"output del primo step
    result2 = subprocess.run(["sort"], input=result1.stdout, stdout=subprocess.PIPE, text=True)

    # Terzo step: `uniq`, che prende l"output del secondo step e scrive nel file output.txt
    with open(output, "w") as output_file:
        subprocess.run(["uniq"], input=result2.stdout, stdout=output_file, text=True)

