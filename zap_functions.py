import time
import subprocess
import connection_manager as CM
from utility import progress_print

connection = CM.ConnectionManager()
zap = connection.zap

def zap_start_spider(url):
    scanID = zap.spider.scan(url)

    while int(zap.spider.status(scanID)) < 100:
        # Poll the status until it completes
        progress_print(process="ZAP SPIDER", progress=zap.spider.status(scanID))
        time.sleep(0.5)

    print('\nSpider has completed!')


def zap_start_ajax_spider(url):
    scanID = zap.ajaxSpider.scan(url)

    timeout = time.time() + 60*2   # 2 minutes from now
    # Loop until the ajax spider has finished or the timeout has exceeded
    while zap.ajaxSpider.status == 'running':
        if time.time() > timeout:
            break
        print(f"\r {' '*50}", end ="")
        print(f'\rAjax Spider status: {zap.ajaxSpider.status}', end="" )
        time.sleep(0.5)

    print('\nAjax Spider completed')
    zap.ajaxSpider.results()
    
def zap_insert_url_in_context(urls):
    for url in urls:
        zap.core.access_url(url, followredirects=None)

def zap_get_nodes(url):
    for node in zap.core.child_nodes(url):
        print (node)
# Inserisce la lista di url nel contesto di zap e procede con la scansione delle anomalie
def zap_start_ascan(urls = []):

    if len(urls) != 0:
        zap_insert_url_in_context(urls)
    
    for site in zap.core.sites:
        
        scanID = zap.ascan.scan(site)

        try:
            while int(zap.ascan.status(scanID)) < 100:
                progress_print(process="[Active Scan]", progress=zap.ascan.status(scanID))
                time.sleep(5)

            print('\nActive Scan completed')
        except ValueError:
            print("[ValueError] Si è verificato un errore con l'ActiveScan...")
            print(f"scanID: {scanID}")
            print("Chiusura")
            connection.close()

        # Print vulnerabilities found by the scanning

def zap_print_report():
    REPORT_NAME = 'zap_report.html'
    report = zap.core.htmlreport()

    with open( REPORT_NAME, 'w', encoding='utf-8') as report_file:
        report_file.write(report)
    print("Report creato!!")
    subprocess.Popen(["firefox", REPORT_NAME])
