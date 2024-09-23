#!/usr/bin/env python3

import sys
import socket
from datetime import datetime
import click
import concurrent.futures
import ipaddress
import json
import csv

def print_banner():
    banner = """
    ____            _   ____                    _           
   |  _ \ ___  _ __| |_|  _ \ _ __ _____      _| | ___ _ __ 
   | |_) / _ \| '__| __| |_) | '__/ _ \ \ /\ / / |/ _ \ '__|
   |  __/ (_) | |  | |_|  __/| | | (_) \ V  V /| |  __/ |   
   |_|   \___/|_|   \__|_|   |_|  \___/ \_/\_/ |_|\___|_|   
                                                            
    """
    click.echo(click.style(banner, fg='cyan', bold=True))
    click.echo(click.style("Welcome to PortProwler", fg='green', bold=True))
    click.echo(click.style("Stealthy and Swift Port Scanning by BigYarMean", fg='yellow'))
    click.echo(click.style("=" * 60, fg='blue'))

def print_usage_examples():
    click.echo(click.style("Usage Examples:", fg='green', bold=True))
    click.echo(click.style("1. Scan a single host:", fg='yellow'))
    click.echo("   python3 portprowler.py example.com")
    click.echo(click.style("\n2. Scan multiple hosts for a specific port range:", fg='yellow'))
    click.echo("   python3 portprowler.py 192.168.1.1 10.0.0.1 -p 80 443")
    click.echo(click.style("\n3. Scan an IP range for top 20 common ports:", fg='yellow'))
    click.echo("   python3 portprowler.py 192.168.1.0/24 --top-ports")
    click.echo(click.style("\n4. Scan with custom timeout and thread count, save results to a JSON file:", fg='yellow'))
    click.echo("   python3 portprowler.py example.com -t 0.5 -T 50 -o results.json")
    click.echo(click.style("\n5. Scan multiple targets and save results in CSV format:", fg='yellow'))
    click.echo("   python3 portprowler.py example.com 192.168.1.1 10.0.0.0/28 -o results.csv -f csv")
    click.echo(click.style("\n6. Perform a quick scan of top ports on multiple hosts:", fg='yellow'))
    click.echo("   python3 portprowler.py example.com 192.168.1.1 --top-ports -T 100")
    click.echo(click.style("\nFor more information on available options, use:", fg='green'))
    click.echo("python3 portprowler.py --help")

def scan_port(ip, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return port, True, service
            return port, False, None
    except:
        return port, False, None

def scan_target(target, ports, timeout, max_threads):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, target, port, timeout): port for port in range(ports[0], ports[1] + 1)}
        with click.progressbar(concurrent.futures.as_completed(future_to_port), length=ports[1]-ports[0]+1, 
                               label='Scanning ports', item_show_func=lambda p: f"Port {p.result()[0] if p else ''}") as bar:
            for future in bar:
                port, is_open, service = future.result()
                if is_open:
                    open_ports.append((port, service))
    return open_ports

def save_results(results, filename, format):
    if format == 'json':
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    elif format == 'csv':
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['IP', 'Port', 'Service'])
            for ip, ports in results.items():
                for port, service in ports:
                    writer.writerow([ip, port, service])

def display_results(results):
    for ip, open_ports in results.items():
        click.echo(click.style(f"\nScan Results for {ip}:", fg='cyan', bold=True))
        if open_ports:
            click.echo(click.style("Port\tService", fg='yellow', bold=True))
            for port, service in open_ports:
                click.echo(f"{port}\t{service}")
        else:
            click.echo(click.style("No open ports found.", fg='yellow'))

@click.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument('targets', nargs=-1)
@click.option('-p', '--ports', nargs=2, type=int, default=(1, 1024), 
              help='Port range to scan (start end)')
@click.option('-t', '--timeout', type=float, default=1.0,
              help='Timeout for each port scan')
@click.option('-T', '--threads', type=int, default=100,
              help='Maximum number of threads to use')
@click.option('-o', '--output', type=click.Path(),
              help='Output file to save results')
@click.option('-f', '--format', type=click.Choice(['json', 'csv']), default='json',
              help='Output format (json or csv)')
@click.option('--top-ports', is_flag=True, help='Scan only top 20 most common ports')
@click.pass_context
def main(ctx, targets, ports, timeout, threads, output, format, top_ports):
    """Enhanced port scanner with multiple targets and threading support"""
    if not targets:
        print_banner()
        print_usage_examples()
        return

    print_banner()
    
    if top_ports:
        ports = (1, 1024)
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    
    results = {}
    for target in targets:
        try:
            network = ipaddress.ip_network(target, strict=False)
            target_list = list(network.hosts())
        except ValueError:
            target_list = [target]

        for single_target in target_list:
            try:
                target_ip = socket.gethostbyname(str(single_target))
            except socket.gaierror:
                click.echo(click.style(f"Error: Hostname {single_target} could not be resolved.", fg='red', bold=True))
                continue

            click.echo(click.style(f"\nScanning target: {target_ip}", fg='green', bold=True))
            click.echo(f"Port range: {ports[0]}-{ports[1]}")
            click.echo(f"Timeout: {timeout} seconds")
            click.echo(f"Max threads: {threads}")
            click.echo(f"Time started: {datetime.now()}")
            click.echo(click.style("=" * 60, fg='blue'))

            if top_ports:
                open_ports = scan_target(target_ip, (min(common_ports), max(common_ports)), timeout, threads)
                open_ports = [port for port in open_ports if port[0] in common_ports]
            else:
                open_ports = scan_target(target_ip, ports, timeout, threads)

            results[target_ip] = open_ports

    display_results(results)

    if output:
        save_results(results, output, format)
        click.echo(click.style(f"\nResults saved to {output}", fg='green', bold=True))

    click.echo(click.style("\nScan completed.", fg='green', bold=True))

if __name__ == "__main__":
    main()