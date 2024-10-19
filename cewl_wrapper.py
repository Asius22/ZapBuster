import subprocess
import os, time
from utility import waiting_print

TARGET = "https://iltrispizzeria.it"
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

    if not os.path.exists(output_path):
        args = ["cewl", "-w", f"{output_path}", "--meta", url]
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL,)
        
        while process.poll() is None:
            waiting_print("Analyzing site")
            time.sleep(1)
        print("")
        
    return output_path


if __name__=="__main__":
    launch_cewl(TARGET)