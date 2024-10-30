import os, time, requests, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


# Funzione per verificare se un URL è raggiungibile
def is_reachable(url, timeout=1):
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code < 400
    except requests.RequestException:
        return False

# Funzione per eseguire Sublist3r e trovare i sottodomini
def find_subdomains(url:str, output_dir:str):
    # Esegui Sublist3r per trovare i sottodomini
    max_workers = os.cpu_count() * 3
    # crea la cartella di ooutput
    output_file = f"{output_dir}/subdomains.txt"

    print(f"Starting {url} subdomains enumeration...")
    process = subprocess.Popen(['sublist3r', '-d', url, "-t", f"{max_workers}", "-o", output_file], stdout=subprocess.DEVNULL)
    
    while process.poll() is None:
        time.sleep(5)
    
    with open(output_file, mode="r") as file:
        subdomains = {line.strip() for line in file.readlines()}
        file.close()

    # Calcola max_workers in base al numero di CPU * 3
    max_workers = os.cpu_count() * 3

    # Test di raggiungibilità dei sottodomini in parallelo
    reachable_domains = set()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(is_reachable, f"http://{subdomain}"): subdomain for subdomain in subdomains}
        
        for future in as_completed(futures):
            subdomain = futures[future]
            url = f"http://{subdomain}"
            try:
                if future.result():  # Se il risultato è True, il sottodominio è raggiungibile
                    reachable_domains.add(url)
                    print(f"{url} is reachable")
            except Exception as e:
                print(f"Error testing {url}: {e}")

    print(f"\n\n{len(reachable_domains)}/{len(subdomains)} reachable domains finded", end="\n\n")
    return reachable_domains

if __name__ == "__main__":
    # Esempio di utilizzo
    url = "example.com"
    result = find_subdomains(url)
    print("\nReachable subdomains:")
    print(result)
