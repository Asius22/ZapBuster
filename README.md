# ZapBuster

ZapBuster is a powerful tool for web application security testing and reconnaissance. It performs a comprehensive analysis of the entire domain associated with the provided URL, regardless of the specific path given. The tool combines multiple scanning techniques to provide thorough analysis of web applications.

## Features

- Full domain scanning and analysis, regardless of the specific URL path provided
- Support for both single URL and bulk URL analysis from a file
- Integration with ZAP (Zed Attack Proxy) for vulnerability scanning
- Optional aggressive mode utilizing external tools for enhanced analysis
- Ajax spider capability for modern web applications
- Customizable recursion depth for thorough scanning
- Proxy support for network flexibility
- Multiple report formats (HTML, JSON, XML)

## Prerequisites

- Python 3.x
- ZAP (Zed Attack Proxy)
- FeroxBuster (for aggressive mode)
- CeWL (Custom Word List generator, for aggressive mode)

Ensure all dependencies are installed and properly configured before running the tool.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/asius22/ZapBuster.git
   cd ZapBuster
   ```

2. Install it by Makefile:
   ```
   make install
   ```

## Usage

Run the tool using the following command:

```
python main.py -u URL [options]
```

### Options

- `-u, --url URL`  
  Specify a single URL or web endpoint to analyze (the entire associated domain will be scanned).
- `-f, --file FILE`  
  Provide a file containing URLs to analyze (one URL per line). If both `--url` and `--file` are specified, only `--url` will be used.
- `-w, --wordlist WORDLIST`  
  Custom wordlist for scanning directories and hidden files. If not specified, the default wordlist is used (`SecList common.txt`).
- `--recursion-depth DEPTH`  
  Set the maximum recursion depth for the scan (0 for infinite depth, default: 2).
- `--proxy PROXY`  
  Specify a proxy to use in the format `address:port` (e.g., `127.0.0.1:8080`).
- `--aggressive-mode`  
  Enable aggressive mode by using additional tools (e.g., FeroxBuster and CeWL) for a deeper scan (this may slow down execution).
- `--spider`  
  Use the standard ZAP spider for scanning the URL. This parameter is ignored if `--aggressive-mode` is not provided.
- `--ajax`  
  Use the Ajax spider for analyzing modern web applications with heavy JavaScript interactions.
- `--report {html,json,xml}`  
  Specify the format of the final report (default: html).

> **Note:** If neither `--url` nor `--file` is provided, the tool will display a help message and exit.

### Examples

1. Analyze a single URL (scans entire associated domain) using ZAP spider:
   ```
   python main.py -u http://example.com/somepath
   ```

2. Import URLs from a file and run vulnerability scanning:
   ```
   python main.py -f urls.txt --aggressive-mode
   ```

3. Analyze a URL with custom wordlist:
   ```
   python main.py -u http://example.com -w custom_wordlist.txt 
   ```

4. Analyze a URL using merging zap and other tools:
   ```
   python main.py -u http://example.com --aggressive-mode --ajax 
   ```

5. Analyze a URL and print results in a json file:
   ```
   python main.py -u http://example.com --aggressive-mode --ajax --report json
   ```

## Scanning Modes

### Standard Mode
In standard mode, the tool uses ZAP (Zed Attack Proxy) to perform a comprehensive scan of the entire domain associated with the provided URL.

### Aggressive Mode
When the `--aggressive-mode` flag is used, the tool employs additional external programs alongside ZAP for an even more thorough analysis:

- **FeroxBuster**: Used for advanced directory and file enumeration.
- **CeWL**: Generates a custom wordlist based on the target website's content.
- **SecLists**: Provide the many up-to-date wordlist used as base wordlist and customized by CeWL results

Aggressive mode provides a more in-depth scan but may take longer and use more resources, if '--recursion-depth' is not provided by default will be 0 (infinite depth).

## Output

The tool will provide a detailed report of the analysis, including:
- Discovered URLs and directories across the entire domain
- Potential vulnerabilities
- Ajax-specific findings (if enabled)
- Results from external tools (in aggressive mode)

Reports are generated in the specified format (HTML, JSON, or XML).

## Caution

This tool is intended for authorized security testing only. Ensure you have permission to scan the target domains. Aggressive mode and deep recursion can be resource-intensive for both the scanner and the target server.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Disclaimer

This tool is for educational and ethical testing purposes only. The authors are not responsible for any misuse or damage caused by this program. Always obtain explicit permission before scanning any websites or networks that you do not own or have explicit permission to test.
