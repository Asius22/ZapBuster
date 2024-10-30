
import argparse, sys, subprocess
import ferox_wrapper as fw
from pathlib import Path
from tabulate import tabulate
from zap_wrapper import ZAPWrapper
from utility import merge_wordlist, print_title, normalize_urls
from cewl_wrapper import launch_cewl as cewl
from sublister_wrapper import find_subdomains

SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/common.txt"
    

def analyze_urls_from_file(zap: ZAPWrapper, file:str, report_type:str, ajax:bool, spider:bool):
    """Perform the vulnerability scanning stariting from a file of urls

    Args:
        zap (ZAPWrapper): the zap process to use
        file (str): the ulrs file
        report_type (str): {html, json, xml} the desidered report type
        spider (bool): define the possibility to perform standard spidering
        ajax (bool): define the possibility to perform ajax spidering
    """
    zap.import_url_from_file(file)
    for site in zap.get_sites():
        perform_spidering(zap, url=site, ajax=ajax, spider=spider)
            
    perform_vulnerability_scan(zap, report_type=report_type)

def perform_ferox_crawl(url:str, url_list: set, output_dir:str, custom_wordlist:str, proxy:str, recursion_depth:str, rate_limit:bool=False):
    """perform a first visit to create a wordlist based on the site itslef, then merge it with {custom_wordlist} 
    or otherwise with the base wordlist (Seclists -> common.txt)

    Args:
        url (str): the url to crawl
        custom_wordlist (str): define a custom wordlist to merge with the wordlist created 
        proxy (str): (optional) the proxy to use
        recursion_depth (str): (Default 4) how much deep to dig

    Returns:
        set: the urls finded
    """
    # crea una custom wordlist usande Cewl
    wordlist = cewl(url)
    # uniscila con la wordlist base
    wordlist = merge_wordlist(wordlist, custom_wordlist or SECLIST_WL, wordlist)
    # Inizia la scansione
    print("Avvio FeroxBuster...")
    url_scanned = fw.launch_ferox(urls=url_list,output_dir=output_dir, wordlist=wordlist, proxy=proxy, recursion_depth=recursion_depth, rate_limit=rate_limit)
    print("FeroxBuster Terminato!")
    return url_scanned


def perform_spidering(zap: ZAPWrapper, url:str, spider:bool=False, ajax:bool=False):
    """perform spidering if ajax or spider are True
    do nothing if both are False

    Args:
        zap (ZAPWrapper): the Zap wrapper
        url (str): the url to spider
        spider (bool, optional): define if perform the standard spidering. Defaults to False.
        ajax (bool, optional): define if perform the ajax spidering. Defaults to False.
    """
    
    if spider:
        zap.start_spider()
    if ajax:
        zap.start_ajax_spider()


def perform_vulnerability_scan(zap: ZAPWrapper, report_type:str):
    """Perform the vulnerability mapping of Zap

    Args:
        zap (ZAPWrapper): the zap wrapper
        report_type (str): the report type desidered
    """
    print("Inizio active scan")
    zap.start_ascan()
    print("Active scan concluso. Genero il report...")
    zap.print_report(report_type)
    print("Report generato.")
    zap.termZap()


def main():
    parser = argparse.ArgumentParser(description="Analizzatore di URL", 
                prog="zapbuster", usage="%(prog)s -u URL [option]", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-u", "--url", help="Specify a single URL or web endpoint to analyze", required=False, type=str)
    parser.add_argument("-f", "--file", help="File containing a list of URLs to analyze (one URL per line)", required=False, type=str)
    parser.add_argument("-w", "--wordlist", help="Custom wordlist for scanning directories and hidden files. If not specified, a default wordlist will be used", required=False, type=str)
    parser.add_argument("-s","--subdomain", help="Perform subdomains search and analysis", action="store_true")
    parser.add_argument("-rl","--rate-limit", help="Limit crawl network to 200 request per second", action="store_true")
    parser.add_argument("--recursion-depth", help="Set the maximum recursion depth for the scan (0 for infinite depth, default: 2)",  required=False, default="0", type=str)
    parser.add_argument("--proxy", help="Specify a proxy to use for the analysis in the format <address:port> (e.g., 127.0.0.1:8080)", required=False, type=str)
    parser.add_argument("--aggressive-mode", help="Enable aggressive mode by using additional tools alongside ZAP for a deeper analysis (may slow down execution)", action="store_true")
    parser.add_argument("--spider", help="Use the standard ZAP spider for analyzing mthe url. If --aggressive is not provided this parameter will be ignored",required=False, action="store_true")
    parser.add_argument("--ajax", help="Use the Ajax spider for analyzing modern web applications with heavy JavaScript interactions", action="store_true")
    parser.add_argument("-r","--report", help="Specify the format of the final report (default: html)", required=False, type=str, default="html", choices=["html", "json", "xml"])
    parser.epilog = "Note: If both URL and file are specified, the file will be ignored"
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        print("Devi specificare almeno un URL (--url) o un file di URL (--file).")
        sys.exit(1)
    
    table_data = [
    ["URL", args.url or "/"],
    ["FILE", args.file or "/"],
    ["SUBDOMAIN", args.subdomain],
    ["RECURSION_DEPTH", args.recursion_depth],
    ["PROXY", args.proxy or "/"],
    ["AGGRESSIVE_MODE", args.aggressive_mode],
    ["SPIDER", args.spider],
    ["AJAX", args.ajax],
    ["WORDLIST", args.wordlist or SECLIST_WL],
    ["RATE LIMIT", args.rate_limit],
    ["REPORT", args.report]
]
    print(tabulate(table_data, headers=["Parameter", "Value"], tablefmt="github"), end="\n\n") 
    

    
    zap = ZAPWrapper(proxy= args.proxy)
    
    if args.url:   
        # crea gli url per ogni processo
        sublister_url, _, ferox_url = normalize_urls(args.url) 
        urls = set()
        output_dir= f"./result/{args.url.replace(".","_")}"
        subprocess.run(["mkdir", output_dir])
        
        if args.subdomain:
            url_set = find_subdomains(sublister_url, output_dir=output_dir)
            urls.update(url_set)
            
        
        if args.aggressive_mode:
            zap.insert_url_in_context(
                perform_ferox_crawl(url= ferox_url, url_list=urls, output_dir=output_dir, proxy= args.proxy, recursion_depth= args.recursion_depth, custom_wordlist= args.wordlist,)
            )
        
        if args.ajax or args.spider:
            perform_spidering(zap=zap, url=args.url, spider=args.spider, ajax=args.ajax)
        
        perform_vulnerability_scan(zap, report_type=args.report)
        
    elif args.file:
        path = Path(args.file)
        if path.is_file():
            # avvia analyze_from_file con il path assoluto
            analyze_urls_from_file(ZAPWrapper(proxy=args.proxy), path.resolve(), report_type = args.report, ajax=args.ajax, spider=args.spider)
        else:
            print(f"Impossibile trovare il file {path.resolve()}")


if __name__ == "__main__":
    print_title()
    main()

