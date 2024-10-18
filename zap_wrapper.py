import time
import subprocess
import connection_manager as CM
from utility import progress_print

class ZAPWrapper:
    def __init__(self, proxy):
        self.connection = CM.ConnectionManager(proxy = proxy)
        self.zap = self.connection.zap

    def start_spider(self, url):
        scanID = self.zap.spider.scan(url)

        while int(self.zap.spider.status(scanID)) < 100:
            # Poll the status until it completes
            progress_print(process="ZAP SPIDER", progress=self.zap.spider.status(scanID))
            time.sleep(0.5)

        print('\nSpider has completed!')
        for res in self.zap.spider.results(scanID):
            print(res)


    def start_ajax_spider(self, url):
        scanID = self.zap.ajaxSpider.scan(url)

        timeout = time.time() + 60*2   # 2 minutes from now
        # Loop until the ajax spider has finished or the timeout has exceeded
        while self.zap.ajaxSpider.status == 'running':
            if time.time() > timeout:
                break
            print(f"\r {' '*50}", end ="")
            print(f'\rAjax Spider status: {self.zap.ajaxSpider.status}', end="" )
            time.sleep(0.5)

        print('\nAjax Spider completed')
        self.zap.ajaxSpider.results()
        
    def insert_url_in_context(self, urls):
        for url in urls:
            self.zap.core.access_url(url, followredirects=None)

    def get_nodes(self, url):
        for node in self.zap.core.child_nodes(self, url):
            print (node)
    # Inserisce la lista di url nel contesto di zap e procede con la scansione delle anomalie
    def start_ascan(self, urls = []):

        if len(urls) != 0:
            self.insert_url_in_context(urls)
        
        for site in self.zap.core.sites:
            
            scanID = self.zap.ascan.scan(site)

            try:
                while int(self.zap.ascan.status(scanID)) < 100:
                    progress_print(process="[Active Scan]", progress=self.zap.ascan.status(scanID))
                    time.sleep(5)

                print('\nActive Scan completed')
            except ValueError:
                print("[ValueError] Si è verificato un errore con l'ActiveScan...")
                print(f"scanID: {scanID}")
                print("Chiusura")
                self.connection.close()

            # Print vulnerabilities found by the scanning

    def print_report(self):
        REPORT_NAME = 'report.html'
        report = self.zap.core.htmlreport()

        with open( REPORT_NAME, 'w', encoding='utf-8') as report_file:
            report_file.write(report)
        print("Report creato!!")
        subprocess.Popen(["firefox", REPORT_NAME])


    def termZap(self):
        self.connection.close()