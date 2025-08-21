import os
import gradio as gr
import subprocess
import shutil

# === Tool Metadata ===
TOOL_NAME = "AI Powered Reconnaissance Automation and Report Generation Tool"
WARNING = "⚠️ This tool integrates AI & CLI utilities. Results may contain outdated, previous or incorrect records. Always cross-verify manually."

# === Core Execution ===
def run_recon(domain, sudo_password):
    if not domain.strip() or not sudo_password.strip():
        return "❌ Domain or password missing.", None, None

    domain = domain.strip().lower()
    txt_report = os.path.join("output", f"{domain}_report.txt")
    pdf_report = f"{domain}_report.pdf"

    try:
        result = subprocess.run(
            ["python3", "run_shell.py", domain, sudo_password],
            text=True,
            capture_output=True,
            timeout=1200  # 20 mins timeout
        )
        log_output = result.stdout + "\n" + result.stderr

        if not os.path.exists(txt_report):
            return "❌ Recon .txt report was not generated.", None, None
        if not os.path.exists(pdf_report):
            return "❌ PDF report was not generated.", None, None

        return f"✅ Recon completed for {domain}.\n\n{log_output}", txt_report, pdf_report

    except subprocess.TimeoutExpired:
        return f"❌ Process timed out after 20 minutes.", None, None
    except Exception as e:
        return f"❌ Error: {str(e)}", None, None


# === Gradio Interface ===
with gr.Blocks(title=TOOL_NAME) as demo:
    gr.Markdown(f"# 🧠 {TOOL_NAME}")
    gr.Markdown(WARNING)

    with gr.Row():
        domain_input = gr.Textbox(label="🔍 Target Domain or IP", placeholder="e.g., abc.com")
        password_input = gr.Textbox(label="🔐 Sudo Password", type="password", placeholder="Your system sudo password")

    run_btn = gr.Button("🚀 Run Recon + Generate PDF")
    output_log = gr.Textbox(label="🪵 Execution Log", lines=20, interactive=False)
    txt_file = gr.File(label="📄 Download TXT Report")
    pdf_file = gr.File(label="📑 Download PDF Report")

    run_btn.click(
        fn=run_recon,
        inputs=[domain_input, password_input],
        outputs=[output_log, txt_file, pdf_file]
    )

# === Launch the UI ===
if __name__ == "__main__":
    demo.launch(share=False)
