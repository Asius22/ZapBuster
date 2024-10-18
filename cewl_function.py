import subprocess
from utility import waiting_print

TARGET = "https://iltrispizzeria.it"

def get_output_file_name(url):
    output_name = str(url).replace("https://", "")
    output_name = output_name.replace("http://", "")
    output_name = output_name.replace("www.", "")
    output_name = output_name.replace(".", "_") 
    
    return f"cewl_{output_name}.txt"

def launch_cewl(url):
    output_name = get_output_file_name(url)
    args = ["cewl", "-w", f"{output_name}", "-o", "--meta", url]
    process = subprocess.Popen(args, stdout=subprocess.DEVNULL,)
    
    while process.poll() is None:
        waiting_print("Creating Wordlist")
    return output_name


    
if __name__=="__main__":
    launch_cewl(TARGET)