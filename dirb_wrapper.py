import subprocess
import utility as UT

WORD_LIST = "/usr/share/wordlists/dirb/common.txt"
OUTPUT_FILE = "dirb_out.txt"

# Avvia dirb su una wordlist comune se non specificata un'altra
def start_dirb(target, wordlist = WORD_LIST):
    args = ["dirb",target ,wordlist, "-o", OUTPUT_FILE, "-N 404", ]
    
    process = subprocess.Popen(args, start_new_session=True, stdout=subprocess.DEVNULL, )


    while process.poll() is None:
        UT.waiting_print("[DIRB] Scanning")

    print("\nScansione Completa!")
    
    urls = UT.extract_url_from_file(OUTPUT_FILE)
    clean_running()
    return urls
    
def clean_running():
    subprocess.run(["rm", "-f", OUTPUT_FILE])
    