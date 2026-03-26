# Java-Project-Manager-Practical-Generator
A powerful Python-based automation tool that helps manage Java programs, compile & execute them intelligently, fetch files from GitHub, and generate professional HTML practical reports with source code and output.

🚀 Features
🔥 Smart Java Runner (handles packages, inputs, arguments)
📥 Download Java files directly from GitHub
🌐 Convert source code to HTML with syntax highlighting
📄 Generate practical report (HTML/PDF-ready format)
🧠 Auto-detect input types (Scanner-based programs)
🖥️ Interactive shell interface for command execution
🧠 Code Explanation (Short)

This script automates Java program execution and report generation by compiling, running, detecting inputs, fetching files from GitHub, and converting results into a structured HTML practical report.

⚙️ How to Run the Code
✅ Required Libraries

Install the following Python libraries before running:

pip install requests pygments
🧩 Required Extensions / Tools

Make sure you have:

✅ Python 3.x installed
✅ Java JDK installed (javac & java commands available in PATH)
✅ VS Code (Recommended)
Python Extension
Code Runner (optional but useful)
✅ Web Browser (for opening generated HTML reports)
▶️ Steps to Run (Exactly 3 Steps)

Clone or Download the Repository

git clone https://github.com/your-username/your-repo.git
cd your-repo

**Install Required Libraries

-> pip install requests pygments

Run the Script

python your_script_name.py

**-> 💡BEFORE RUNNING THIS CODE ADD THE LOGO IMAGE IN EACH AND EVERY FOLDER.
  ->💡BEFORE RUNNING THIS CODE IF YOU WANT TO CHANGE YOUR ENROLLMENT NUMBER THEN CHANGE IT FROM MAIN PROGRAM AT LINE 168

Then use commands like:

💡setrepo <user> <repo> <branch> → Change GitHub source
(eg: setrepo Nihar42002 JAVA-PROJECTS main)

💡getfile <path> → Download Java file from GitHub
(eg: getfile practice_set1/ATM.java) for normal progarms
(eg: getfile practice_set8/Fileoperation8_4/fileoperations.java) for file operations

💡practical <java_file> [logo] → Generate report
(eg: practical practice_set1/ATM.java logo.jpg.jpeg)
(eg: practical  practice_set8/Fileoperation8_4/fileoperations.java logo.jpg.jpeg)

cd <folder> → Change directory

➡️ Generates a formatted HTML practical report with:

Source Code
Program Output
College Header + Logo

📂 Output
*.html → Syntax-highlighted code view
practical_output.html → Final practical report
🛠️ Technologies Used
Python
Java (JDK)
Pygments (for syntax highlighting)
Requests (for GitHub file fetching)
HTML/CSS (for report generation)

⚠️ Notes
Ensure Java files are correctly structured (especially packages)
Input prompts are auto-detected but may vary depending on code complexity
Script runs commands in a shell-like interface
