import subprocess
from utility import waiting_print, extract_url_from_file
import sys

def launch_ferox(url:str, wordlist:str, recursion_depth:str | None = None, proxy=None ):
    """ launch feroxbuster with following flags:
    \n-A: random user agent
    \n-x pdf,js,html,php,txt,json,docx: search for file with specified extension
    \n-d 0: whith infinite recursion
    \n-w: wordlist to use
    \n-E: Automatically discover extensions and add them to --extensions
    \n-p: (optional) the proxy to use 

    Args:
        url (str): Url to scan
        wordlist (str): /path/to/wordlist
        proxy (str, optional): address:port . Defaults to None.

    Returns:
        res (set of strings): a list of all url finded by ferox process
    """

    if url == "":
        print("[FEROX] url cannot empty")
        sys.exit(1)
        
    if wordlist == "":
        print("[FEROX] Wordlist cannot be none")
        sys.exit(1)
        
    args = ["feroxbuster", "-u", url, "-A", "-x", "pdf,js,html,php,txt,json,docx", "-k", "-w", wordlist, "-E", "-s", "200", "301","--no-state", "--silent"]  
    
    if proxy:
        args.append("-p")
        args.append(proxy)
        
    if recursion_depth is not None:
        args.append("-d")
        args.append(recursion_depth)
        
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, text=True)
    res = set()
    for line in process.stdout:
        if line.strip().replace("\n", "") != "":
            res.add(line)
            print(line)
        else:
            print("\r[Ferox] Scanning", end="")
    process.wait()
    return res
