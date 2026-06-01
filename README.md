# 🛡️ SentinelTask: Multi-User CLI Task Manager

<p align="center">
  <b>A secure, multi-user command-line task management system engineered in Python.</b><br>
  Optimised for speed, security, and direct execution via the terminal.
</p>

---

<h2>📘 Project Overview</h2>

<p>
<b>SentinelTask</b> is an advanced command-line interface (CLI) task tracking tool designed to allow multiple users to securely manage their tasks independently on a single terminal environment. This repository was developed specifically as a solution for the <b><a href="https://roadmap.sh/projects/task-tracker" target="_blank">Task Tracker</a></b> project on <b>roadmap.sh</b>.
</p>

<p>
Unlike basic single-user scripts, SentinelTask implements robust multi-user isolation by utilising secure cryptographic hashing algorithms. Each user's data is isolated, and tasks are strictly mapped to their unique user accounts. No interactive menus are used; instead, it relies entirely on direct, fast command-line arguments passed via the terminal for slick automation and scriptability.
</p>

---

<h2>🔄 Evolution: Differences from the Old Version</h2>

<p>
SentinelTask is a complete architectural rewrite of the previous single-user <b><a href="https://github.com/Sheikh-H/TaskManager" target="_blank">Task Manager (CLI Edition)</a></b>. Here is a breakdown of the structural upgrades:
</p>

<table width="100%">
  <thead>
    <tr style="background-color: #376e00; color: white;">
      <th style="padding: 10px; text-align: left;">Feature</th>
      <th style="padding: 10px; text-align: left;">Old Version (<a href="https://github.com/Sheikh-H/TaskManager" style="color: white; text-decoration: underline;">Task Manager</a>)</th>
      <th style="padding: 10px; text-align: left;">New Version (SentinelTask)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>User Support</b></td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">Single-user only. Anyone with script access manages the same list.</td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Multi-user workspace</b> with explicit individual account ownership.</td>
    </tr>
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Security</b></td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">None. No authentication or encryption mechanism was present.</td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>High security.</b> Accounts are verified using <code>hashlib</code> and unique salts.</td>
    </tr>
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Interface Design</b></td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">Interactive looped menus using blocking <code>input()</code> prompts.</td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Direct CLI invocation</b> passing command arguments in one line.</td>
    </tr>
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Task Statuses</b></td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">Binary state: Completed (<code>True</code>) or Incomplete (<code>False</code>).</td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">Tri-state tracking: <code>To-Do</code>, <code>In-Progress</code>, and <code>COMPLETED</code>.</td>
    </tr>
    <tr>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Task Identifiers</b></td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;">Global application ID counters across the entire file.</td>
      <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>User-scoped IDs</b> (`User A` and `User B` can both have a `Task ID #1`).</td>
    </tr>
  </tbody>
</table>

---

<h2>🧩 Folder Structure</h2>

<pre>
SentinelTask/
│
├── task-cli.py         # Application entry point & main script
├── README.md           # Project documentation
├── users.json          # Database file holding hashed credentials (auto-generated)
└── tasks.json          # Database file holding individual task records (auto-generated)
</pre>

---

<h2>🚀 How to Run</h2>

<ol>
  <li>Ensure you have <b>Python 3.8 or above</b> installed on your operating system.</li>
  <li>Clone or download this repository locally:
    <pre>git clone https://github.com/Sheikh-H/Sentinel-Task.git</pre>
  </li>
  <li>Navigate directly into the project directory:
    <pre>cd SentinelTask</pre>
  </li>
  <li>Execute commands using the syntax options defined below. You can view the syntax manual at any time by running:
    <pre>python task-cli.py --help</pre>
  </li>
</ol>

---

<h2>🖥️ Detailed Usage & Command Manual</h2>

<p>
Since this script acts as a true CLI tool responding to arguments, execute your desired operational tasks by passing arguments directly following the script path.
</p>

<h3>1. User Account Operations</h3>
<ul>
  <li><b>Register a New User:</b>
    <pre>python task-cli.py new-user [username] [password]</pre>
  </li>
  <li><b>Change an Account Password:</b>
    <pre>python task-cli.py change-password [username] [old_password] [new_password]</pre>
  </li>
</ul>

<h3>2. Task Manipulation Operations</h3>
<ul>
  <li><b>Create a New Task:</b>
    <pre>python task-cli.py [username] [password] add-task "Your task title here"</pre>
  </li>
  <li><b>Update an Existing Task Title:</b>
    <pre>python task-cli.py [username] [password] update-task [task_id_or_title] "New task title"</pre>
  </li>
  <li><b>Delete an Active Task:</b>
    <pre>python task-cli.py [username] [password] delete-task [task_id_or_title]</pre>
  </li>
</ul>

<h3>3. Task Tracking Lifecycle Statuses</h3>
<ul>
  <li><b>Mark a Task as In-Progress:</b>
    <pre>python task-cli.py [username] [password] mark-in-progress [task_id_or_title]</pre>
  </li>
  <li><b>Mark a Task as Complete:</b>
    <pre>python task-cli.py [username] [password] mark-complete [task_id_or_title]</pre>
  </li>
</ul>

<h3>4. Comprehensive Viewing & Filtering Options</h3>
<ul>
  <li><b>View All Tasks:</b>
    <pre>python task-cli.py [username] [password] view</pre>
  </li>
  <li><b>Filter by Category Type:</b>
    <pre>python task-cli.py [username] [password] view [filter_phrase]</pre>
    <i>Supported phrases include:</i>
    <ul>
      <li><b>Completed tasks:</b> <code>done</code>, <code>complete</code>, <code>completed</code>, <code>finished</code></li>
      <li><b>Active tasks:</b> <code>doing</code>, <code>current</code>, <code>currently active</code>, <code>active</code>, <code>in-progress</code></li>
      <li><b>Awaiting tasks:</b> <code>new</code>, <code>to-do</code>, <code>todo</code>, <code>recent</code>, <code>just added</code></li>
    </ul>
  </li>
</ul>

<p>⚠️ <b>Note:</b> If your task title or filtering phrase contains spaces, always wrap it inside quotation marks (e.g. <code>"Buy groceries"</code>) so the CLI interprets it correctly as a single parameter.</p>

---

<h2>⚙️ Code Architecture & Function Breakdown</h2>

<p>
This section details how the script processes data and explains exactly what each function does under the hood:
</p>

<h3>Data Persistence</h3>
<ul>
  <li><code>load_data(filename)</code>: Checks for the targeted JSON database file. If missing, it writes an empty array structure to initialise it cleanly. It opens, parses, and returns the stored data records.</li>
  <li><code>save_data(data, filename)</code>: Flushes current in-memory global state modifications to disk using an automated two-space structural indentation layout.</li>
</ul>

<h3>Security Engine</h3>
<ul>
  <li><code>new_user(username, password)</code>: Handles registration logic. It safeguards details by generating a random cryptographically secure 16-byte hex value using the <code>secrets</code> module. It applies a <code>PBKDF2-HMAC-SHA256</code> key derivation path running 100,000 algorithmic cycles before preserving the resulting unique hash string.</li>
  <li><code>user_login(username, password)</code>: Authenticates operational tasks. It fetches the exact individual user record, pairs the provided password attempt against the user's stored salt value, executes matching key processing iteration settings, and explicitly halts script loop flow via the <code>error()</code> function if mismatched.</li>
</ul>

<h3>Core Task Processing</h3>
<ul>
  <li><code>add_task(username, password, task_title)</code>: Validates credentials via <code>user_login()</code>, checks for duplicate naming conflicts across active records, calculates a user-scoped incrementing identifier index, and maps a complete task entity containing creation timestamps.</li>
  <li><code>update_task(username, password, task_search, new_title)</code>: Evaluates if <code>task_search</code> is a numerical entry or an explicit string pattern. If string matching yields ambiguous multiple results, the utility returns an intuitive prompt telling the user to use the unique numerical task ID instead</li>
  <li><code>delete_task(username, password, task_id)</code>: Iterates sequentially over global storage scopes, maps entries containing matching ownership attributes, and removes indices targeting matching records.</li>
  <li><code>list_task(username, password, list_type)</code>: Acts as an entry dispatcher. It processes multiple human-readable string inputs into standardised categories before querying output formatting streams.</li>
  <li><code>view_tasks_print(user, category)</code>: Evaluates parameters to layout information fields explicitly framed inside systematic ASCII table layouts, tracing parameters like creation dates and precise adjustment timestamps.</li>
</ul>

---

<h2>📂 JSON Storage Architecture</h2>

<p>
The storage layout separates users from user tasks into distinct files, tracking precise ownership keys across lists:
</p>

<h3>User Accounts File (<code>users.json</code>)</h3>
<pre>
[
  {
    "id": 1,
    "username": "sheikh",
    "password": "a1b2c3d4e5f6g7h8i9j0...",
    "created_at": "2026-05-23 16:30:00",
    "salt": "f37a28e9d8c21b5a...",
    "last_updated": null
  }
]
</pre>

<h3>Task Records File (<code>tasks.json</code>)</h3>
<pre>
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Complete Roadmap Project",
    "status": "IN-PROGRESS",
    "created_at": "2026-05-23 16:35:00",
    "updated_at": "2026-05-23 16:40:12"
  }
]
</pre>

---

<h2>🧰 Requirements & Dependencies</h2>

<ul>
  <li><b>Python Runtime:</b> version 3.8 or above.</li>
  <li><b>External Libraries:</b> Completely dependency-free! Built completely using internal standard libraries (<code>sys</code>, <code>json</code>, <code>os</code>, <code>time</code>, <code>datetime</code>, <code>hashlib</code>, and <code>secrets</code>).</li>
</ul>

---

<h2>📄 Licence</h2>

<p>
  This project is licensed under the <b>MIT Licence</b> — see the <a href="./LICENCE">LICENCE</a> file for details.
</p>

<pre>
MIT Licence

Copyright (c) 2026 Sheikh Hussain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</pre>

---

## Footnote

<div align="center" style="border: 1px solid green; padding: 10px; border-radius: 5px;">
  <p>🗣️ Feel free to follow, connect, and chat!</p>
  <a class="header-badge" target="_blank" href="https://github.com/Sheikh-H"><img src="https://img.shields.io/badge/GitHub-376e00?style=flat&logo=github&logoColor=white" alt="GitHub">
  </a><a class="header-badge" target="_blank" href="https://www.linkedin.com/in/sheikh-hussain/"><img src="https://img.shields.io/badge/LinkedIn-376e00?style=flat&logo=LinkedIn&logoColor=white" alt="LinkedIn">
  </a><a class="header-badge" target="_blank" href="mailto:sheikh.hussain1155@gmail.com"><img src="https://img.shields.io/badge/Gmail-376e00?style=flat&logo=gmail&logoColor=white" alt="Gmail">
  </a><a class="header-badge" target="_blank" href="https://sheikh-h.github.io/"><img src="https://img.shields.io/badge/Portfolio-376e00?style=flat&logo=github&logoColor=white" alt="Portfolio">
  </a>
</div>

<div align="center">
  <a href="https://www.linkedin.com/in/sheikh-hussain/" target="_blank">By Sheikh Hussain 💚</a>  
</div>

---

<h2 align="center">⭐ If you like this project, please give it a star on GitHub!</h2>
