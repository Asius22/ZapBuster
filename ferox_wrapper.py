import subprocess
from utility import waiting_print, extract_url_from_file

import time
"feroxbuster -u <URL> -A -x pdf,js,html,php,txt,json,docx -k -d 0 -w <wordlist da usare> -E -B -g -p --silent"


def launch_ferox(url, wordlist, proxy=None):
    """

    Args:
        url (str): Url to scan
        wordlist (str): /path/to/wordlist
        proxy (str, optional): address:port . Defaults to None.
    Result:
        res (set of strings): a list of all url finded by ferox process
    """
    if url is None:
        print("[FEROX] url cannot none")
        return
    if wordlist is None:
        print("[FEROX] Wordlist cannot be none")
        return 
    output = "tmp.txt"
    args = ["feroxbuster", "-u", url, "-A", "-x", "pdf,js,html,php,txt,json,docx", "-k", "-d","0", "-w", wordlist, "-E", "-B", "-g", "-o", output, "--silent"]
    
    if proxy:
        args.append("-p")
        args.append(proxy)
    
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, text=True)
    start = time.time()
    while process.poll() is None:
        waiting_print("Scanning site")
        if time.time() < start + 60 * 2:
            process.kill()
            break;
    
    res = extract_url_from_file(output)
    subprocess.call(["rm", "-f", output])
    print("processo terminato")
    return res

if __name__=="__main__":
    launch_ferox("iltrispizzeria.it", "./wordlists/cewl_iltrispizzeria_it.txt")