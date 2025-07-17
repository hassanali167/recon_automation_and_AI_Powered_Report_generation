# 🛡️ AI-Powered Reconnaissance Automation and Report Generation Tool

A fully automated Python-based recon workflow that collects information using industry-standard tools, processes the results with AI (Groq LLaMA-3 70B), and generates structured, deduplicated, and professional PDF reports.

> ✨ **Project Target Example**: `abc.com`

---

## 📁 Project Structure

```
recon-tool/
├── .env                      # API key storage (NOT to be committed)
├── report_gen.py            # Main recon data cleaner and PDF generator
├── requirements.txt         # Python dependencies
├── sample_input/            # Example raw recon input files
│   └── ebc.com_report.txt
├── generated_reports/       # Final generated PDF reports
│   └── ebc.com_report.pdf
└── README.md
```

---

## 🚧 Features

- ✅ Supports large recon files (auto-splitting to fit token limits)
- ✅ Handles rate limits with multiple API keys
- ✅ Cleans errors, timeouts, and irrelevant data
- ✅ Detects WordPress usage with proper formatting
- ✅ Outputs PDF with:
  - Title + Domain + IP
  - Cleaned deduplicated recon key-value table
  - List of tools used
- ✅ Beautifully styled table with spacing, padding, and grid lines
- ✅ Command-line based usage for automation or scripting

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/recon_automation_and_AI_Powered_Report_generation
cd ai-recon-reporter
```

### 2. Install Python Requirements

```bash
sudo pip install -r requirements.txt --break-system-packages
```

### 3. Setup `.env` File

Create a file named `.env` in the root folder:

```
GROQ_KEYS=your_api_key1,your_api_key2,your_api_key3
```

### 4. run tool
 if you need just cli tool so run 
```bash
sudo python3 run_shell.py
```
if you need a web based interface run gradio_app.py  or  gradio_app_2.py


> ⚠️ Do NOT commit your `.env` to GitHub. Add it to `.gitignore`

You can get API keys from [Groq Console](https://console.groq.com/)

---

## 📄 Sample Recon File Format

Example raw input file: `sample_input/ebc.com_report.txt`

```
whois ebc.com
nmap -sV ebc.com
wpscan --url ebc.com
dig ebc.com
nslookup ebc.com
```

---

## ⚡ Run the Tool

```bash
python3 report_gen.py sample_input/ebc.com_report.txt
```

Output:
```
📂 Generating recon report for: ebc.com
🛠️ Processing chunk 1/3...
🔹 Report saved: generated_reports/ebc.com_report.pdf
```

---

## 📕 Example Report Output (PDF)

- Title: AI-Powered Reconnaissance Report
- Target Domain: ebc.com
- IP Address: 192.0.2.1

| Key           | Value                                |
|----------------|----------------------------------------|
| Target        | ebc.com                              |
| IP            | 192.0.2.1                            |
| Web Server    | nginx/1.23.4                         |
| WordPress     | This website does not use WordPress. |
| ...           | ...                                  |

**Tools Used:**
`whois, dig, nmap, wpscan, dnsenum, sublist3r, whatweb, theHarvester, dirsearch`

---

## 🔧 Supported Recon Tools

You can use the output of any of the following tools:

- Whois
- DNS (dig, dnsrecon, dnsenum, nslookup, host)
- Port scanners (nmap, masscan)
- Web tech scanner (whatweb)
- CMS scanner (wpscan)
- Directory bruteforcers (dirsearch)
- Passive intel (sublist3r, theHarvester)
- Vulnerability scanners (nikto, wafw00f, curl, etc.)

---

## 🖋️ Notes

- This tool integrates **AI models**, which may hallucinate or generalize.
- Ensure your recon data is up-to-date before report generation.
- If WordPress is not detected, the tool will say: `This website does not use WordPress.`
- API keys rotate automatically if one exceeds its rate limit.
- If you need more clarification about this tool how to use them ---- then make aure to read use.txt

---

## 📖 License

This project is released under the **MIT License**. For academic, research, and commercial use.

---

## ✨ Credits

- Built with Python, ReportLab, Groq LLaMA-3 API
- Maintained by [Hassan Ali](https://github.com/hassanali167)

---

## 🚨 Disclaimer

> This tool uses generative AI. The recon output may not always reflect the current state of a target.
> Use responsibly and verify manually when needed.

