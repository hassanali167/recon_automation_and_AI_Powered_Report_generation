import os
import sys
import subprocess

def run_with_sudo(script_path, sudo_password, extra_args=None):
    cmd = ["sudo", "-S", "bash", script_path]
    if extra_args:
        cmd.append(extra_args)

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=sudo_password + "\n")
    print(stdout)
    if stderr:
        print("⚠️ ERROR:", stderr)
    if process.returncode != 0:
        print(f"❌ Script {script_path} failed.")
        sys.exit(process.returncode)

def run_report_generator(domain):
    report_path = os.path.join("output", f"{domain}_report.txt")
    if not os.path.exists(report_path):
        print(f"❌ Report file not found: {report_path}")
        return
    print(f"📄 Running AI report generation on: {report_path}")
    subprocess.run(["python3", "report_gen.py", report_path])

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 run_shell.py <target_domain> <sudo_password>")
        return

    domain = sys.argv[1]
    sudo_password = sys.argv[2]

    install_script = os.path.abspath("install_recon_tools.sh")
    recon_script = os.path.abspath("recon_automate.sh")

    print("🔧 Step 1: Installing tools...")
    run_with_sudo(install_script, sudo_password)

    print("🔍 Step 2: Running reconnaissance...")
    run_with_sudo(recon_script, sudo_password, domain)

    print("📊 Step 3: Generating AI-enhanced PDF report...")
    run_report_generator(domain)

    print("✅ All done!")

if __name__ == "__main__":
    main()
