import subprocess
import sys, os

def launch_ferox(urls:set, wordlist:str, output_dir:str, recursion_depth:str | None = None, proxy:str=None, rate_limit:bool=False):
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
    if len(urls) <= 0:
        print("[FEROX] Some problem has verified")
        sys.exit(1)
    if wordlist == "":
        print("[FEROX] Wordlist cannot be none")
        sys.exit(1)
        
    url_file = f"{output_dir}/reachable_urls"
    
    with open(url_file, mode="w") as file:
        file.writelines(f"{url}\n" for url in urls)
        file.close()
        
    max_workers = int(os.cpu_count() * 0.7) # use 70% of CPU cores
    
    ferox_args = ["feroxbuster", "--stdin", "--parallel", f"{max_workers}", "-A", "-x", "pdf,js,html,php,txt,json,docx", "-k", "-r","-w", wordlist, "-E", "-g","-s", "200", "301", "401", "403", "405", "--no-state", "--silent"]  
    
    if proxy:
        ferox_args.append("-p")
        ferox_args.append(proxy)
        
    if recursion_depth is not None:
        ferox_args.append("-d")
        ferox_args.append(recursion_depth)
        
    if rate_limit:
        ferox_args.append("-t")
        ferox_args.append("200")
        ferox_args.append("-L")
        ferox_args.append("5")
        ferox_args.append("--thorough")
        
    cat_args= ["cat", url_file]
    try:
        cat_process = subprocess.Popen(cat_args, stdout=subprocess.PIPE, text=True)
        ferox_process = subprocess.Popen(ferox_args, stdout=subprocess.PIPE, stdin=cat_process.stdout, text=True)
        cat_process.stdout.close()
        res = set()
        i = 0
        for line in ferox_process.stdout:
            if line != "":
                res.add(line)
                sys.stdout.write(line.strip() + "\n")
                i+=1
                if i == 10:
                    sys.stdout.flush()
                    i = 0
        ferox_process.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt intercettato: passo alla prossima fase")
        
        ferox_process.terminate()
        cat_process.terminate()
    return res
