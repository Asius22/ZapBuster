import subprocess
import os, time
from utility import waiting_print


WL_PREFIX="./wordlists"



def get_output_file_name(url):
    """_summary
    crea un pathname sulla base dell'url in modo da poterlo riutilizzare per scansioni future
    """
    output_name = str(url).replace("https://", "")
    output_name = output_name.replace("http://", "")
    output_name = output_name.replace("www.", "")
    output_name = output_name.replace(":", "-")
    output_name = output_name.replace(".", "_") 
    output_name = output_name.replace("/", "") 

    return f"cewl_{output_name}.txt"


def launch_cewl(url):
    """_summary_
    Args:
        url (string): l'url da analizzare per creare la wordlist
        
    Returns:
        string: il pathname della wordlist creata
    """
    output_path = os.path.join(WL_PREFIX, get_output_file_name(url))
    
    if os.path.exists(output_path):
        
        choice = input("Esiste già una wordlist per questo url, vuoi sovrascriverla? (y/N)")
        while choice.lower() not in ["y", "n"]:
            choice = input("Risposta non valida. Vuoi sovrascriverla? (y/N)")
            print("rispondere solo con y o n")
                    
        if choice.lower() ==  "y":
            args = ["cewl", "-w", f"{output_path}", "--meta", "-d","10", url]
            process = subprocess.Popen(args, stdout=subprocess.DEVNULL,)
            
            while process.poll() is None:
                waiting_print("Analyzing site")
                time.sleep(1)
            print("")
        
    return output_path
