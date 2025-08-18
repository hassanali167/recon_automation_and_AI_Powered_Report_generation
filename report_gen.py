import os
import sys
import time
import requests
import textwrap
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# === Load API Keys from .env ===
load_dotenv()
API_KEYS = os.getenv("GROQ_KEYS", "").split(",")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"
CHUNK_CHAR_LIMIT = 5000

# === Utility Functions ===
def split_text(text, limit=CHUNK_CHAR_LIMIT):
    return textwrap.wrap(text, limit, break_long_words=False, break_on_hyphens=False)

def clean_text(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        l = line.strip().lower()
        if any(x in l for x in ["skipped due to", "timeout", "error", "rate limit"]):
            continue
        if "unable to find wordpress" in l:
            cleaned.append("This website does not use WordPress.")
        elif "not found" in l or "unable to detect" in l:
            continue
        else:
            cleaned.append(line)
    return "\n".join(cleaned)

def send_to_groq(chunk, domain, key):
    prompt = f"""
You are a cybersecurity expert creating a structured red-team recon report.

TASK:
Convert this raw recon data for domain \"{domain}\" into a single table format with key-value pairs. The table should not contain duplicate keys or repeated values.

Format:
| Key       | Value |
|-----------|-------|
| Target    | techniknest.tech |
| IP        | 76.76.21.21      |
... etc.

At the end, add a section listing all the tools used.

INPUT:
{chunk}
"""
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You write well-structured technical recon reports with professional tone."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(GROQ_URL, headers=headers, json=data)
    if response.status_code == 429:
        return "RATE_LIMIT"
    elif response.status_code != 200:
        print(f"❌ API ERROR {response.status_code}: {response.text}")
        return None
    return response.json()['choices'][0]['message']['content']

def extract_table(md_text):
    rows = []
    for line in md_text.strip().splitlines():
        if "|" in line and not "---" in line:
            parts = [col.strip() for col in line.split("|") if col.strip()]
            if len(parts) == 2:
                rows.append(parts)
    return rows

def extract_tool_list(md_text):
    lines = md_text.strip().splitlines()
    tools = []
    for line in lines:
        if line.lower().startswith("tools used"):
            tools.extend([x.strip() for x in line.split(":")[-1].split(",")])
    return list(set(tools))

def generate_pdf(table_data, ordered_tools, domain):
    file_name = f"{domain}_report.pdf"
    doc = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"<b>AI-Powered Reconnaissance Report</b>", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Target Domain:</b> {domain}", styles['Normal']))

    ip = next((val for key, val in table_data if key.lower() == "ip"), "N/A")
    story.append(Paragraph(f"<b>IP Address:</b> {ip}", styles['Normal']))
    story.append(Spacer(1, 12))

    seen_keys = set()
    filtered = []
    for key, value in table_data:
        if key.lower() not in seen_keys:
            seen_keys.add(key.lower())
            filtered.append([key, value])

    table = Table(filtered, colWidths=[180, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    tools = [
        "whois", "dnsenum", "dnsrecon", "dig", "fierce", "sublist3r", "theHarvester",
        "nmap", "whatweb", "wafw00f", "nikto", "shodan", "curl", "host",
        "nslookup", "wpscan", "dirsearch",
        " ",
        " ",
        " ",
        "This tool integrates AI & CLI utilities. Results may contain outdated, previous or incorrect records. Always cross-verify manually."
    ]
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Tools Used:</b>", styles['Heading3']))
    story.append(Spacer(1, 6))
    tool_list = ", ".join(tools)
    story.append(Paragraph(tool_list, styles['Normal']))

    doc.build(story)
    print(f"✅ Report saved: {file_name}")

def read_raw_report(path):
    with open(path, 'r') as f:
        return f.read()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 report_gen.py <raw_report.txt>")
        return

    file_path = sys.argv[1]
    domain = os.path.basename(file_path).replace("_report.txt", "").replace(".txt", "")
    print(f"📂 Generating recon report for: {domain}")

    raw_text = read_raw_report(file_path)
    chunks = split_text(raw_text)
    all_rows = []
    all_tools = []

    for i, chunk in enumerate(chunks):
        print(f"⚙ Processing chunk {i+1}/{len(chunks)}...")
        chunk = clean_text(chunk)
        key = API_KEYS[i % len(API_KEYS)]

        result = send_to_groq(chunk, domain, key)

        if result == "RATE_LIMIT":
            print("⚠ Rate limit hit. Waiting 5 seconds...")
            time.sleep(5)
            key = API_KEYS[(i + 1) % len(API_KEYS)]
            result = send_to_groq(chunk, domain, key)

        if result and result != "RATE_LIMIT":
            rows = extract_table(result)
            tools = extract_tool_list(result)
            all_rows.extend(rows)
            all_tools.extend(tools)
        else:
            print(f"⚠ Skipped chunk {i+1} due to repeat API limits.")

    generate_pdf(all_rows, sorted(set(all_tools)), domain)

if __name__ == "__main__":
    main()
