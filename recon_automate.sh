#!/bin/bash

# Accept domain name as a command-line argument
domain="$1"

# Create output folder if it doesn't exist
mkdir -p output

# Define output path
output_file="output/${domain}_report.txt"

# Get IP of target
ip=$(dig +short "$domain" | head -n 1)
successful_tools=()

echo "Reconnaissance Report for $domain" > "$output_file"
echo "Resolved IP: $ip" >> "$output_file"
echo "Generated on: $(date)" >> "$output_file"
echo "========================================" >> "$output_file"

# Semaphore to control parallel jobs (2 at a time)
semaphore=2

run_tool() {
  local label="$1"
  local command="$2"
  local tool="$3"
  local timeout_sec="$4"

  (
    echo -e "\n[+] Running: $label" | tee -a "$output_file"

    if [[ "$timeout_sec" -gt 0 ]]; then
      timeout "$timeout_sec"s bash -c "$command" >> "$output_file" 2>&1
    else
      bash -c "$command" >> "$output_file" 2>&1
    fi

    if [[ $? -eq 0 ]]; then
      successful_tools+=("$tool")
    else
      echo "[!] Skipped '$tool' due to timeout or error." >> "$output_file"
    fi
  ) &

  ((--semaphore))
  while [ $semaphore -le 0 ]; do sleep 1; done
  ((++semaphore))
}

# === Reconnaissance Tools (2 at a time) ===
run_tool "WHOIS Lookup" "whois $domain" "whois" 40
run_tool "DNSENUM" "dnsenum $domain" "dnsenum" 40
run_tool "DNSRECON" "dnsrecon -d $domain" "dnsrecon" 40
run_tool "DIG Queries" "dig $domain any; dig A $domain; dig MX $domain; dig NS $domain; dig TXT $domain; dig CNAME www.$domain" "dig" 40
run_tool "HOST lookups" "host $domain; host -t mx $domain; host -t ns $domain" "host" 40
run_tool "NSLOOKUP" "nslookup $domain" "nslookup" 40
run_tool "Sublist3r" "sublist3r -d $domain" "sublist3r" 40
run_tool "TheHarvester" "theHarvester -d $domain -b duckduckgo" "theHarvester" 40
run_tool "Fierce" "fierce --domain $domain" "fierce" 40
run_tool "WhatWeb" "whatweb $domain" "whatweb" 40
run_tool "WAFW00F" "wafw00f http://$domain; wafw00f -v http://$domain" "wafw00f" 40
run_tool "Nikto" "nikto -h http://$domain" "nikto" 40
run_tool "Curl Headers" "curl -I http://$domain" "curl" 40
run_tool "WPScan Basic" "wpscan --url https://$domain" "wpscan" 40
run_tool "WPScan Enum" "wpscan --url https://$domain --enumerate u,vp,vt" "wpscan-enum" 40
run_tool "Dirsearch" "dirsearch -u https://$domain" "dirsearch" 40
run_tool "SSL Checker" "shcheck https://$domain" "shcheck" 40
run_tool "Shodan Host" "shodan host $ip" "shodan" 40

# === Run Nmap (sequentially) ===
echo -e "\n[+] Running: Nmap Basic" | tee -a "$output_file"
nmap "$domain" >> "$output_file" 2>&1 && successful_tools+=("nmap") || echo "[!] Nmap basic failed." >> "$output_file"

echo -e "\n[+] Running: Nmap Service & OS Detection" | tee -a "$output_file"
nmap -sV -O "$domain" >> "$output_file" 2>&1 && successful_tools+=("nmap-service") || echo "[!] Nmap service detection failed." >> "$output_file"

# Wait for all parallel tools to complete
wait

# Summary Section
echo -e "\n\n==== Summary ====" >> "$output_file"
echo "Tools Successfully Used:" >> "$output_file"
for tool in "${successful_tools[@]}"; do
  echo "- $tool" >> "$output_file"
done

echo -e "\n✅ Report saved at: $output_file"
