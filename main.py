
import zap_functions as zf
import dirb_function as df
from cewl_function import launch_cewl as cewl
import argparse, sys, os

TARGET = "https://public-firing-range.appspot.com"

"""
"feroxbuster -u <URL> -A -x pdf,js,html,php,txt,json,docx -k -d 0 -w <wordlist da usare> -E -B -g"
SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt"

#TARGET = "https://iltrispizzeria.it"

custom_wordlist = cewl(TARGET)



zf.zap_start_spider(TARGET)

dirb_urls = df.start_dirb(TARGET)
zf.zap_insert_url_in_context(dirb_urls)
zf.zap_start_ajax_spider(TARGET)


zf.zap_start_ascan()
zf.zap_print_report()




connection.close()

"""
def analyze_urls_from_file(file):
    try: 
        with open(file, "r") as urls_file:
            # importa gli url all'interno del context di zap
            for line in urls_file.readlines():
                if line.startswith("https://") or line.startswith("http://"):
                    zf.zap_insert_url_in_context(line)
                else:
                    print(f"line:\n\t{line}\n not analyzed cause it seems to not be an url")
            zf.zap_start_ascan() #avvia il vulnerability mapping
    except OSError:
        print(f"[Error] Could not open {file}")
        
    zf.zap_print_report() #stampa il report
    
def analyze_url(url, aggressive, ajax):
    print(f"Analyzing url {url} aggressive = {aggressive} ajax = {ajax}")
    wordlist = cewl(url)
            
def main():
    parser = argparse.ArgumentParser(description="Analizzatore di URL")
    parser.add_argument("--url", help="URL da analizzare", required=False)
    parser.add_argument("--aggressive", help="Modalità di scansione", action="store_true") #true se specificato, false altrimenti
    parser.add_argument("--file", help="File contenente gli URL da analizzare")
    parser.add_argument("--ajax", help="Usa spiderAjax per l'analisi", action="store_true") #true se specificato, false altrimenti

    args = parser.parse_args()

    if not args.url and not args.file:
        print("Devi specificare almeno un URL (--url) o un file di URL (--file).")
        sys.exit(1)


    if args.url:
        analyze_url(args.url, args.aggressive, args.ajax)
    
    if args.file:
        analyze_urls_from_file(args.file)


    zf.termZap()
if __name__ == "__main__":
    main()

