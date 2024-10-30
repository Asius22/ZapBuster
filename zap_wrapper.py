import os
import time
import connection_manager as CM
import concurrent.futures 
from utility import progress_print

THREADS = 40
HOSTS = 2
TIMEOUT = 2
class ZAPWrapper:
    def __init__(self, proxy=None):
        self.connection = CM.ConnectionManager(proxy = proxy)
        self.zap = self.connection.zap
        #self.zap.network.add_rate_limit_rule("ZapBusterLimit", enabled=True, )

    def start_spider(self):
        try:
            for url in self.zap.core.sites:
                print(f"Start spider for {url}:")

                scanID = self.zap.spider.scan(url)
                while int(self.zap.spider.status(scanID)) < 100:
                    # Poll the status until it completes
                    progress_print(process="ZAP SPIDER", progress=self.zap.spider.status(scanID))
                    time.sleep(0.3)
                progress_print(process="ZAP SPIDER", progress=100)
        except KeyboardInterrupt:
            print("KeyboardInterrupt intercettato: passo alla prossima fase")
            
            self.zap.spider.stop_all_scans()
            
        print('\nSpider has completed!')


    def start_ajax_spider(self, url):
        self.zap.ajaxSpider.set_option_max_duration(TIMEOUT)
        self.zap.ajaxSpider.set_option_max_crawl_states(20)
        self.zap.ajaxSpider.set_option_number_of_browsers(20)
        try:  
            for url in self.zap.core.sites:
                print(f"Start ajax spider for {url}:")
                self.zap.ajaxSpider.scan(url)
                # Loop until the ajax spider has finished or the timeout has exceeded
                
                while self.zap.ajaxSpider.status == 'running':
                    print(f"\r {' '*50}", end ="")
                    print(f'\rAjax Spider status: {self.zap.ajaxSpider.status}', end="" )
                    time.sleep(2)
        except KeyboardInterrupt:
            print("KeyboardInterrupt intercettato: passo alla prossima fase")
            self.zap.ascan.stop_all_scans()
        print('\nAjax Spider completed')


    def import_url_from_file(self, filepath):
        self.zap.exim.import_urls(filepath)


    def access_url(self, url):
        self.zap.core.access_url(url, followredirects=None)


    def insert_url_in_context(self, urls):
        """Insert a set of urls inside the zap context
        Args:
            urls (set_of_strings): the set of urls to insert inside zap context
        """        
        print("Inserisco gli url trovati nel context di zap:")
        # Determine optimal number of threads
        max_workers = max(32, os.cpu_count() * 10)  
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.access_url, url) for url in urls]
            for future in concurrent.futures.as_completed(futures):
                future
        print("Completato!")



    def get_nodes(self, url):
        for node in self.zap.core.child_nodes(url):
            print (node)
        print(len(self.zap.core.child_nodes(url)))


    def get_sites(self):
        return self.zap.core.sites


    # Inserisce la lista di url nel contesto di zap e procede con la scansione delle anomalie
    def start_ascan(self, urls = []):
        scanner = self.zap.ascan
        scanner.set_option_thread_per_host(THREADS)
        scanner.set_option_host_per_scan(HOSTS)
        
        if len(urls) != 0:
            self.insert_url_in_context(urls)
        print(f"Avvio active scan {self.zap.core.sites}")
        try: 
            for site in self.zap.core.sites:
                try:
                    scanID = scanner.scan(site, recurse=True)
                    
                    try:
                        while int(scanner.status(scanID)) < 100:
                            progress_print(process="[Active Scan]", progress=self.zap.ascan.status(scanID))
                            time.sleep(10)
                        progress_print(process="[Active Scan]", progress=100)
                        print('\nActive Scan completed')
                    except ValueError:
                        print("[ValueError] Si è verificato un errore con l'ActiveScan...")
                        print(f"scanID: {scanID}")
                        print("Chiusura")
                        self.connection.close() 
                except KeyboardInterrupt:
                    scanner.stop(scanid=scanID)
                    print("KeyboardInterrupt: passo al prossimo sito")
            # Print vulnerabilities found by the scanning
                time.sleep(1)
        except KeyboardInterrupt:
            print("keyboardinterrupt: creo il report")


    def print_report(self, type:str = "html"):    
        match type:
            case "html":
                REPORT_NAME = "report.html"
                report = self.zap.core.htmlreport()
            case "xml":
                REPORT_NAME = "report.xml"
                report = self.zap.core.xmlreport()
            case _:
                REPORT_NAME = "report.json"
                report = self.zap.core.jsonreport()
        with open( REPORT_NAME, 'w', encoding='utf-8') as report_file:
            report_file.write(report)
        print("Report creato!!")


    def termZap(self):
        self.connection.close()