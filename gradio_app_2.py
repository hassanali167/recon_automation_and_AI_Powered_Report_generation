import os
import gradio as gr
import subprocess


TOOL_NAME = "AI Powered Reconnaissance Automation and Report Generation Tool"
WARNING = "⚠️ This tool integrates AI & CLI utilities. Results may contain outdated, previous or incorrect records. Always cross-verify manually."

def run_recon(domain, sudo_password):
    if not domain.strip() or not sudo_password.strip():
        return "❌ Domain or password missing.", None, None, gr.update(visible=False), gr.update(visible=False)

    domain = domain.strip().lower()
    txt_report = os.path.join("output", f"{domain}_report.txt")
    pdf_report = f"{domain}_report.pdf"

    try:
        result = subprocess.run(
            ["python3", "run_shell.py", domain, sudo_password],
            text=True,
            capture_output=True,
            timeout=1200  # 20 min
        )
        log_output = result.stdout + "\n" + result.stderr

        txt_exists = os.path.exists(txt_report)
        pdf_exists = os.path.exists(pdf_report)

        return (
            f"✅ Recon completed for {domain}.\n\n{log_output}",
            txt_report if txt_exists else None,
            pdf_report if pdf_exists else None,
            gr.update(visible=txt_exists),
            gr.update(visible=pdf_exists)
        )

    except subprocess.TimeoutExpired:
        return "❌ Process timed out after 20 minutes.", None, None, gr.update(visible=False), gr.update(visible=False)
    except Exception as e:
        return f"❌ Error: {str(e)}", None, None, gr.update(visible=False), gr.update(visible=False)


with gr.Blocks(title=TOOL_NAME, css="""
h1, h2 { text-align: center; }
.gr-button.download {
    background-color: #0f172a;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 10px;
    margin-top: 10px;
}
""") as demo:
    # Header
    gr.Markdown(f"<h1>{TOOL_NAME}</h1>", elem_id="title")
    gr.Markdown(f"<h4>{WARNING}</h4>", elem_id="subtitle")

    # Input Section
    with gr.Row():
        domain_input = gr.Textbox(label="🔍 Target Domain or IP", placeholder="e.g., abc.com")
        password_input = gr.Textbox(label="🔐 Sudo Password", type="password", placeholder="Your system sudo password")

    # Button to Start Recon
    run_btn = gr.Button("🚀 Run Recon + Generate PDF")

    # Output Log
    output_log = gr.Textbox(label="🪵 Execution Log", lines=20, interactive=False)

    # Download Buttons (initially hidden)
    with gr.Row():
        txt_file = gr.File(label="📄 Download TXT Report", visible=False, interactive=False, elem_classes=["download"])
        pdf_file = gr.File(label="📑 Download PDF Report", visible=False, interactive=False, elem_classes=["download"])

    # Button action
    run_btn.click(
        fn=run_recon,
        inputs=[domain_input, password_input],
        outputs=[output_log, txt_file, pdf_file, txt_file, pdf_file]
    )

# Run
if __name__ == "__main__":
    demo.launch()
