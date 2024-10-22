
import argparse, sys
import threading
import concurrent.futures
import ferox_wrapper as fw
from pathlib import Path
from zap_wrapper import ZAPWrapper
from utility import merge_wordlist, waiting_print
from cewl_wrapper import launch_cewl as cewl

SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/common.txt"


def analyze_urls_from_file(zap: ZAPWrapper, file:str, report_type:str, ajax:bool=False, ):
    
    zap.import_url_from_file(file)
    for site in zap.get_sites():
        zap.start_spider(site)
    if ajax:
        for site in zap.get_sites():
            zap.start_ajax_spider(site)
    zap.start_ascan() #avvia il vulnerability mapping
    
    zap.print_report(report_type) #stampa il report
    zap.termZap()


def analyze_url( url:str, aggressive: bool, ajax:bool, spider:bool, custom_wordlist:str | None, recursion_depth: str, report_type:str, proxy=None):
    """Starts the analysis procedure starting with the creation of a custom wordlist using cewl, 
    then there is the forced browsing step, using feroxbuster tool and [optional] ajax-spider and zap-spider (if relative flagss are setted)
    and finally starts the active scan and print report scan 

    Args:
        url (str): the url to analyze
        aggressive (bool): specify if use other tools with zap ones
        ajax (bool): specify in during aggressive procedure use also ajax spier
        spider (bool): specify if during aggressive scan use also traditional zap spider
        custom_wordlist (str | None): specify if use a custom wordlist with cewl one or use the standard one (common)
        recursion_depth (str): Depth to spider to 
        report_type (str): {html, json, xml} the output file expected
        proxy (str, optional): the proxy string to use during analysis. Defaults to None.
    """
    if aggressive:
        # crea una custom wordlist usande Cewl
        wordlist = cewl(url)
        # uniscila con la wordlist base
        wordlist = merge_wordlist(wordlist, custom_wordlist or SECLIST_WL, wordlist)
        # Inizia la scansione
        print("Avvio FeroxBuster...")
        url_scanned = fw.launch_ferox(url=url, wordlist=wordlist, proxy=proxy, recursion_depth=recursion_depth)
        print("FeroxBuster Terminato!")
        
        zap = ZAPWrapper(proxy=proxy)
        print("Avvio spider...")
        zap.start_spider(url)
        
        if spider:
            print("Avvio lo spider...")
            zap.start_spider(url)
            print("Spidering completo")
        
        if ajax:
            print("Avvio di ajax spider...")
            zap.start_ajax_spider(url)
            print("Ajax spider completo!")

        # Avvia il waiting future
        # ... altri future
        
        print("Scanning terminato")
        
        print("Inizio preparativi per Active scan")
        zap.insert_url_in_context(url_scanned)
    else:
        zap = ZAPWrapper(proxy=proxy)
        zap.start_spider(url)
        if ajax:
            zap.start_ajax_spider(url)
    
    print("Inizio active scan")
    zap.start_ascan()
    print("Active scan concluso. Genero il report...")
    zap.print_report(report_type)
    print("Report generato.")
    zap.termZap()


def main():
    parser = argparse.ArgumentParser(description="Analizzatore di URL", 
                prog="main.py", usage="%(prog)s -u URL [option]", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u", "--url", help="Specify a single URL or web endpoint to analyze", required=False, type=str)
    parser.add_argument("-f", "--file", help="File containing a list of URLs to analyze (one URL per line)", required=False, type=str)
    parser.add_argument("-w", "--wordlist", help="Custom wordlist for scanning directories and hidden files. If not specified, a default wordlist will be used", required=False, type=str)
    parser.add_argument("--recursion-depth", help="Set the maximum recursion depth for the scan (0 for infinite depth, default: 2)",  required=False, default="0", type=str)
    parser.add_argument("--proxy", help="Specify a proxy to use for the analysis in the format <address:port> (e.g., 127.0.0.1:8080)", required=False, type=str)
    parser.add_argument("--aggressive-mode", help="Enable aggressive mode by using additional tools alongside ZAP for a deeper analysis (may slow down execution)", action="store_true")
    parser.add_argument("--spider", help="Use the standard ZAP spider for analyzing mthe url. If --aggressive is not provided this parameter will be ignored",required=False, action="store_true")
    parser.add_argument("--ajax", help="Use the Ajax spider for analyzing modern web applications with heavy JavaScript interactions", action="store_true")
    parser.add_argument("--report", help="Specify the format of the final report (default: html)", required=False, type=str, default="html", choices=["html", "json", "xml"])
    parser.epilog = "Note: If both URL and file are specified, the file will be ignored"
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
    print(f"SPIDER: {args.spider}")
    print(f"AJAX: {args.ajax}")
    print(f"WORDLIST: {args.wordlist or SECLIST_WL}")
    print(f"REPORT: {args.report}\n\n")
    
    if args.url:   
        if not args.url.startswith("http"):
            args.url = f"http://{args.url}"
            print(args.url) 
        analyze_url( url= args.url, aggressive= args.aggressive_mode, ajax= args.ajax,spider=args.spider, proxy= args.proxy, recursion_depth= args.recursion_depth, custom_wordlist= args.wordlist, report_type = args.report)
    elif args.file:
        path = Path(args.file)
        if path.is_file():
            # avvia analyze_from_file con il path assoluto
            analyze_urls_from_file(ZAPWrapper(proxy=args.proxy), path.resolve(), report_type = args.report)
        else:
            print(f"Impossibile trovare il file {path.resolve()}")


if __name__ == "__main__":
    main()

