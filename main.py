
import zap_functions as zf
import dirb_function as df
from cewl_function import launch_cewl as cewl


SECLIST_WL="/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt"

TARGET = "https://iltrispizzeria.it"

custom_wordlist = cewl(TARGET)


print(custom_wordlist)
"""
connection = zf.connection
zap = connection.zap

zf.zap_start_spider(TARGET)
dirb_urls = df.start_dirb(TARGET)
zf.zap_insert_url_in_context(dirb_urls)
zf.zap_start_ajax_spider(TARGET)



zf.zap_start_ascan()
zf.zap_print_report()


connection.close()

"""

