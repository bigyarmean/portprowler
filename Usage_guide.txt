Port Prowler Usage Guide
This guide will help you understand how to use the Port Prowler tool effectively.
Basic Usage
The basic syntax for using the port scanner is:
python3 portprowler.py [TARGET(S)] [OPTIONS]
Where [TARGET(S)] can be one or more IP addresses, hostnames, or IP ranges, and [OPTIONS] are additional parameters to customize the scan.
Options

-p, --ports: Specify the port range to scan. Default is 1-1024.
Example: -p 1 100 scans ports 1 to 100.
-t, --timeout: Set the timeout for each port scan in seconds. Default is 1.0.
Example: -t 0.5 sets a 0.5 second timeout.
-T, --threads: Set the maximum number of threads to use. Default is 100.
Example: -T 50 uses a maximum of 50 threads.
-o, --output: Specify an output file to save results.
Example: -o results.json saves the results to a file named results.json.
-f, --format: Choose the output format (json or csv). Default is json.
Example: -f csv saves the results in CSV format.
--top-ports: Scan only the top 20 most common ports.

Examples

Scan a single host:
python3 portprowler.py example.com

Scan multiple hosts for a specific port range:
python3 portprowler.py 192.168.1.1 10.0.0.1 -p 80 443

Scan an IP range for top 20 common ports:
python3 portprowler.py 192.168.1.0/24 --top-ports

Scan with custom timeout and thread count, save results to a JSON file:
python3 portprowler.py example.com -t 0.5 -T 50 -o results.json

Scan multiple targets and save results in CSV format:
python3 portprowler.py example.com 192.168.1.1 10.0.0.0/28 -o results.csv -f csv

Perform a quick scan of top ports on multiple hosts:
python3 portprowler.py example.com 192.168.1.1 --top-ports -T 100


Understanding the Output
The scanner will display a progress bar during the scan and then show the results for each target. Open ports will be listed along with the service name (if known).
If you've specified an output file, the results will also be saved in the chosen format (JSON or CSV).
Tips

Use the --top-ports option for quicker scans of the most common ports.
Adjust the timeout (-t) and thread count (-T) based on your network conditions and the number of targets.
When scanning multiple targets or large IP ranges, consider saving the output to a file for easier analysis.

Remember to use this tool responsibly and only on networks and systems you have permission to scan.