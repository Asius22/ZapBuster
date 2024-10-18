
from zap_wrapper import ZAPWrapper
import dirb_wrapper as df
from cewl_wrapper import launch_cewl as cewl
import argparse, sys, os
from utility import merge_wordlist

TARGET = "https://public-firing-range.appspot.com"
SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/big.txt"

"""
"feroxbuster -u <URL> -A -x pdf,js,html,php,txt,json,docx -k -d 0 -w <wordlist da usare> -E -B -g"

#TARGET = "https://iltrispizzeria.it"

custom_wordlist = cewl(TARGET)



zap.start_spider(TARGET)

dirb_urls = df.start_dirb(TARGET)
zap.insert_url_in_context(dirb_urls)
zap.start_ajax_spider(TARGET)


zap.start_ascan()
zap.print_report()




connection.close()

"""
def analyze_urls_from_file(zap: ZAPWrapper, file):
    try: 
        with open(file, "r") as urls_file:
            # importa gli url all'interno del context di zap
            for line in urls_file.readlines():
                if line.startswith("https://") or line.startswith("http://"):
                    zap.insert_url_in_context(line)
                else:
                    print(f"line:\n\t{line}\n not analyzed cause it seems to not be an url")
            zap.start_ascan() #avvia il vulnerability mapping
    except OSError:
        print(f"[Error] Could not open {file}")
        
    zap.zap_print_report() #stampa il report


def analyze_url(zap: ZAPWrapper, url, aggressive, ajax, ):
    print(f"Analyzing url {url} aggressive = {aggressive} ajax = {ajax}")
    
    if ajax:
        zap.start_ajax_spider(url)
    
    if aggressive:
        # crea una custom wordlist
        wordlist = cewl(url)
        # uniscila con la wordlist base
        wordlist = merge_wordlist(wordlist, SECLIST_WL, wordlist)


def main():
    parser = argparse.ArgumentParser(description="Analizzatore di URL")
    parser.add_argument("-u","--url", help="URL da analizzare", required=False)
    parser.add_argument("-f","--file", help="File contenente gli URL da analizzare", )
    parser.add_argument("--proxy", help="<address:port>\t\tSpecifica il proxy da utilizzare ", required=False) #true se specificato, false altrimenti
    parser.add_argument("--aggressive-mode", help="Avvia in modaliità aggressiva", action="store_true") #true se specificato, false altrimenti
    parser.add_argument("--ajax", help="Usa spiderAjax per l'analisi (for modern app)", action="store_true") #true se specificato, false altrimenti
    parser.add_argument("--report", help="Specifica il proxy da utilizzare ", required=False, type=str, default="html", choices=["html, json, xml"]) 
    args = parser.parse_args()
    
    if not args.url and not args.file:
        parser.print_help()
        print("Devi specificare almeno un URL (--url) o un file di URL (--file).")
        sys.exit(1)
    
    zap = ZAPWrapper(proxy=args.proxy)
    
    if args.url:    
        analyze_url(zap, args.url, args.aggressive_mode, args.ajax)
    
    if args.file:
        analyze_urls_from_file(zap, args.file)
        
    zap.termZap()


if __name__ == "__main__":
    main()

