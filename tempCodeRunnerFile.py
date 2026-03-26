import base64
import html
import mimetypes
import os
import subprocess
import requests
import webbrowser
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
import shlex
import re

history = []

GITHUB_USER = "Nihar42002"
GITHUB_REPO = "JAVA-PROJECTS"
BRANCH = "main"


# 🔥 UNIVERSAL SMART JAVA RUNNER
# Handles: Packages, Args, Scanner (Type & Count), Threads, and File I/O
def run_java_file(filename):
    if not os.path.exists(filename):
        return f"Error: File '{filename}' not found."

    try:
        # Get absolute path and project root
        abs_filepath = os.path.abspath(filename)
        
        file_dir = os.path.dirname(abs_filepath)
        if not file_dir:
         file_dir = os.getcwd()
        # We assume the project root is where the script is running (cwd)
        project_root = os.getcwd()
        
        # 1. Detect Package & Class Information
        package_prefix = ""
        with open(abs_filepath, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
            package_match = re.search(r'package\s+([\w\.]+);', code)
            if package_match:
                package_prefix = package_match.group(1) + "."

        base_name = os.path.splitext(os.path.basename(filename))[0]
        fqcn = package_prefix + base_name

        # 2. UNIVERSAL COMPILATION
        # We compile from the project root so all imports like 'ClassProject.bpack.B' work
        print(f"🔨 Compiling {fqcn} from project root...")
        compile_proc = subprocess.run(
    ["javac", abs_filepath],
    capture_output=True,
    text=True,
    cwd=file_dir
)

        if compile_proc.returncode != 0:
            return "Compilation Error:\n" + compile_proc.stderr

        # 3. Analyze Code for Input Requirements
        code_lower = code.lower()
        uses_args = any(x in code_lower for x in ["args[", "args.length"])
        
        input_map = [
            (r'\.nextInt\s*\(', "Integer (int)"),
            (r'\.nextDouble\s*\(', "Double (double)"),
            (r'\.nextFloat\s*\(', "Float (float)"),
            (r'\.nextLong\s*\(', "Long (long)"),
            (r'\.nextLine\s*\(', "String (Line)"),
            (r'\.next\s*\(', "String (Word)"),
            (r'\.nextBoolean\s*\(', "Boolean (true/false)")
        ]

        detected_inputs = []
        for pattern, label in input_map:
            matches = re.findall(pattern, code)
            for _ in matches: detected_inputs.append(label)

        # 4. Prepare Command
        cmd = ["java", "-cp", project_root, fqcn]
        formatted_input_data = None

        if uses_args:
            print(f"\n🔎 Args required for {base_name}.")
            user_args = input("👉 Enter arguments: ")
            if user_args.strip(): cmd.extend(shlex.split(user_args))

        if detected_inputs:
            print(f"\n🔎 {len(detected_inputs)} inputs detected.")
            prompts = re.findall(r'System\.out\.print(?:ln)?\("(.*?)"\)', code)
            user_vals = []
            for i, dtype in enumerate(detected_inputs):
                p_text = prompts[i] if i < len(prompts) else f"Input {i+1}"
                val = input(f"❓ {p_text} ({dtype}): ")
                user_vals.append(val)
            formatted_input_data = "\n".join(user_vals) + "\n"

        # 5. EXECUTE FROM PROJECT ROOT
        print(f"\n🚀 Running {fqcn}...")
        run = subprocess.run(
            cmd,
            input=formatted_input_data,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=file_dir # Run from root to satisfy package structure
        )

        if run.stderr:
            return "Runtime Error:\n" + run.stderr

        return run.stdout.strip() if run.stdout else "Program executed successfully."

    except subprocess.TimeoutExpired:
        return "Error: Execution Timeout."
    except Exception as e:
        return f"System Error: {str(e)}"

# 🔹 Convert code to HTML (for viewing)
def code_to_html(filename):
    try:
        with open(filename, "r", encoding="utf-8", errors='replace') as f:
            code = f.read()
        lexer = guess_lexer(code)
        formatter = HtmlFormatter(full=True, linenos=True)
        html_code = highlight(code, lexer, formatter)
        html_file = filename + ".html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_code)
        print(f"HTML created: {html_file}")
        webbrowser.open(f"file://{os.path.abspath(html_file)}")
    except Exception as e:
        print(f"Error creating HTML: {e}")


# 🔹 Download from GitHub
def get_file(filepath):
    url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{filepath}"
    print("Fetching:", url)
    resp = requests.get(url)
    if resp.status_code == 200:
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        print(f"Downloaded: {filepath}")
        code_to_html(filepath)
    else:
        print(f"File not found! (Status: {resp.status_code})")


# 🔹 Helper for Logo Embedding
def _embed_logo_html(logo_path):
    if not logo_path or not os.path.isfile(logo_path):
        return '<div class="logo">Logo</div>'
    try:
        mime, _ = mimetypes.guess_type(logo_path)
        with open(logo_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('ascii')
        return f'<img src="data:{mime or "image/jpeg"};base64,{data}" style="width:90px;height:90px;object-fit:contain;border:1px dashed #999">'
    except:
        return '<div class="logo">Logo</div>'


# 🔥 GENERATE FINAL PRACTICAL PDF-READY HTML
def generate_practical_html(code_path, logo_path=None, enroll="240410107092"):
    if os.path.isfile(code_path):
        with open(code_path, "r", encoding="utf-8", errors="replace") as f:
            code_text = f.read()
    else:
        code_text = "// File not found"

    # Execute the Java code and capture output
    output_text = run_java_file(code_path)

    escaped_code = html.escape(code_text)
    escaped_output = html.escape(output_text)
    logo_html = _embed_logo_html(logo_path)

    content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Practical Report</title>
  <style>
    body {{ font-family: Calibri, Arial, sans-serif; margin: 40px; color: black; line-height: 1.4; }}
    .top {{ display:flex; align-items:center; gap:20px; border-bottom: 2px solid #000; padding-bottom: 10px; }}
    .header {{ text-align:center; flex:1 }}
    .college {{ font-size:16pt; font-weight:bold }}
    .subject {{ font-size:14pt; margin-top: 5px; }}
    .practical-title {{ font-family: 'Times New Roman'; font-size:18pt; margin-top:20px; text-align:center; font-weight:bold; text-decoration: underline; }}
    .section {{ margin-top:20px }}
    .code, .output {{ font-family: 'Consolas', 'Courier New'; font-size:10pt; border:1px solid #333; padding:15px; white-space:pre-wrap; background: #f9f9f9; }}
    .meta {{ text-align:right; font-size:12pt; font-weight: bold; margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="top">
    {logo_html}
    <div class="header">
      <div class="college">SARDAR VALLABHBHAI PATEL INSTITUTE OF TECHNOLOGY</div>
      <div class="subject">SUB: Object Oriented Programming | CODE: BE04000231</div>
    </div>
  </div>
  <div class="practical-title">Practical Session Report</div>
  <div class="section">
    <strong>SOURCE CODE:</strong>
    <div class="code">{escaped_code}</div>
  </div>
  <div class="section">
    <strong>PROGRAM EXECUTION OUTPUT:</strong>
    <div class="output">{escaped_output}</div>
  </div>
  <div class="meta">ENROLLMENT NO: {enroll}</div>
</body>
</html>"""

    output_filename = "practical_output.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Success: {output_filename} generated.")
    webbrowser.open("file://" + os.path.abspath(output_filename))


# 🔥 SHELL INTERFACE
if __name__ == '__main__':
    print("--- Java Project Manager & Practical Generator ---")
    while True:
        cwd = os.getcwd()
        command = input(f"{cwd} > ").strip()

        if not command or command == "exit":
            break

        history.append(command)

        if command.startswith("setrepo"):
            parts = command.split()
            if len(parts) == 4:
                GITHUB_USER, GITHUB_REPO, BRANCH = parts[1], parts[2], parts[3]
                print(f"Repo updated: {GITHUB_USER}/{GITHUB_REPO}")
            else:
                print("Usage: setrepo <user> <repo> <branch>")

        elif command == "showrepo":
            print(f"Current: {GITHUB_USER}/{GITHUB_REPO} ({BRANCH})")

        elif command.startswith("getfile"):
            parts = command.split(" ", 1)
            if len(parts) == 2: get_file(parts[1])

        elif command.startswith("cd"):
            try: os.chdir(command.split(" ", 1)[1])
            except: print("Invalid path")

        elif command.startswith("practical"):
            parts = shlex.split(command)
            if len(parts) >= 2:
                generate_practical_html(parts[1], parts[2] if len(parts) >= 3 else None)
            else:
                print("Usage: practical <java_file> [logo_path]")

        else:
            subprocess.run(command, shell=True)