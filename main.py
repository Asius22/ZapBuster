
import argparse, sys
import threading
import concurrent.futures
import ferox_wrapper as fw
from pathlib import Path
from zap_wrapper import ZAPWrapper
from utility import merge_wordlist, waiting_print
from cewl_wrapper import launch_cewl as cewl

SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/common.txt"


def analyze_urls_from_file(zap: ZAPWrapper, file, url=None, ajax=False):
    
    zap.import_url_from_file(file)
    for site in zap.get_sites():
        zap.start_spider(site)
    if ajax:
        for site in zap.get_sites():
            zap.start_ajax_spider(site)
    zap.start_ascan() #avvia il vulnerability mapping
    
    zap.print_report() #stampa il report
    zap.termZap()


def analyze_url( url:str, aggressive: bool, ajax:bool, custom_wordlist:str | None, recursion_depth: str, proxy=None):
    if aggressive:

        # crea una custom wordlist
        wordlist = cewl(url)
        # uniscila con la wordlist base
        wordlist = merge_wordlist(wordlist, custom_wordlist or SECLIST_WL, wordlist)
    
        #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        print("Avvio ferox...")
        url_scanned = fw.launch_ferox(url=url, wordlist=wordlist, proxy=proxy, recursion_depth=recursion_depth)
        print("FeroxBuster Terminato!")

        zap = ZAPWrapper(proxy=proxy)
        if ajax:
            print("Avvio di ajax spider...")

            zap.start_ajax_spider(url)
            print("Ajax spider completo!")

        # Avvia il waiting future
        # ... altri future
        
        print("Scanning terminato")
        
        print("Inizio preparativi per Active scan")
        zap.insert_url_in_context(url_scanned)
        print("Inizio active scan")
        
        zap.start_ascan()
        zap.print_report()
        zap.termZap()
    else:
        zap = ZAPWrapper(proxy=proxy)
        zap.start_spider(url)
        if ajax:
            zap.start_ajax_spider(url)


def main():
    parser = argparse.ArgumentParser(description="Analizzatore di URL", 
                prog="main.py", usage="%(prog)s -u URL [option]", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u","--url", help="URL da analizzare", required=False)
    parser.add_argument("-f","--file", help="File contenente gli URL da analizzare", required=False)
    parser.add_argument("-w","--wordlist", help="Wordlist di base da usare per la scansione. Se non inserito viene usata quella di default", required=False)
    parser.add_argument("--recursion-depth", help="Abilita la ricerca ricorsiva e specifica quanto deve andare in profondità (0 = infinita, )", type=str, required=False) #true se specificato, false altrimenti
    parser.add_argument("--proxy", help="<address:port>\t\tSpecifica il proxy da utilizzare ", required=False) #true se specificato, false altrimenti
    parser.add_argument("--aggressive-mode", help="Avvia in modaliità aggressiva (molto lenta)", action="store_true") #true se specificato, false altrimenti
    parser.add_argument("--ajax", help="Usa spiderAjax per l'analisi (for modern app)", action="store_true") #true se specificato, false altrimenti
    parser.add_argument("--report", help="Specifica il proxy da utilizzare ", required=False, type=str, default="html", choices=["html", "json", "xml"]) 
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        print("Devi specificare almeno un URL (--url) o un file di URL (--file).")
        sys.exit(1)
    print(f"\n\nURL: {args.url}")
    print(f"FILE: {args.file}")
    print(f"RECURSION_DEPTH: {args.recursion_depth}")
    print(f"PROXY: {args.proxy}")
    print(f"AGGRESSIVE_MODE: {args.aggressive_mode}")
    print(f"AJAX: {args.ajax}")
    print(f"WORDLIST: {args.wordlist or SECLIST_WL}")
    print(f"REPORT: {args.report}\n\n")



    if args.url:   
        if not args.url.startswith("http"):
            args.url = f"http://{args.url}"
            print(args.url) 
        analyze_url( url= args.url, aggressive= args.aggressive_mode, ajax= args.ajax, proxy= args.proxy, recursion_depth= args.recursion_depth, custom_wordlist= args.wordlist)
    elif args.file:
        path = Path(args.file)
        if path.is_file():
            # avvia analyze_from_file con il path assoluto
            analyze_urls_from_file(ZAPWrapper(proxy=args.proxy), path.resolve())
        else:
            print(f"Impossibile trovare il file {path.resolve()}")


if __name__ == "__main__":
    main()

