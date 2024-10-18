import subprocess
import os
from utility import waiting_print

TARGET = "https://iltrispizzeria.it"
WL_PREFIX="./wordlists"

def get_output_file_name(url):
    output_name = str(url).replace("https://", "")
    output_name = output_name.replace("http://", "")
    output_name = output_name.replace("www.", "")
    output_name = output_name.replace(".", "_") 
    output_name = output_name.replace("/", "") 

    return f"cewl_{output_name}.txt"


def launch_cewl(url):
    output_path = os.path.join(WL_PREFIX, get_output_file_name(url))
    print(output_path)
    if not os.path.exists(output_path):
        args = ["cewl", "-w", f"{output_path}", "-o", "--meta", url]
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL,)
        
        while process.poll() is None:
            waiting_print("Creating Wordlist")
        print("")
    return output_path


if __name__=="__main__":
    launch_cewl(TARGET)