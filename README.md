# PortProwler

## Overview

PortProwler is a powerful, Python-based port scanning tool designed for network administrators and security professionals. It offers swift, efficient scanning of multiple targets with various customization options.

## Features

- Scan multiple targets (IP addresses, hostnames, or IP ranges)
- Multithreaded scanning for high-speed performance
- Option to scan only the top 20 most common ports
- Customizable port range, timeout, and thread count
- Save results in JSON or CSV format
- Colorful and informative console output

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.

2. Clone this repository or download the `portprowler.py` file.

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Basic Usage

Run PortProwler with:

```
python3 portprowler.py [TARGET(S)] [OPTIONS]
```

For example:

```
python3 portprowler.py example.com 192.168.1.0/24 -p 1 1000 -T 200 --top-ports -o results.json
```

This command scans example.com and the 192.168.1.0/24 network, focusing on the top 20 ports within the range 1-1000, using 200 threads, and saves the results to a JSON file.

## Options

- `-p, --ports`: Specify port range (default: 1-1024)
- `-t, --timeout`: Set scan timeout in seconds (default: 1.0)
- `-T, --threads`: Set maximum number of threads (default: 100)
- `-o, --output`: Specify output file for results
- `-f, --format`: Choose output format (json or csv, default: json)
- `--top-ports`: Scan only top 20 common ports

For a full list of options and examples, refer to the [Usage Guide](USAGE.md).

## Contributing

Contributions to PortProwler are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

PortProwler is for educational and professional use only. Always ensure you have permission before scanning any networks or systems that you do not own or have explicit permission to test.
