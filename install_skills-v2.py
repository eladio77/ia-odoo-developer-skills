#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTiEG Odoo Cline Skills Installer
---------------------------------
This script automatically generates the complete, professional folder structure
for the Odoo Cline Skills repository as defined in the "Agent Skills_Day_3" runbook.
It implements the Progressive Disclosure design pattern by creating dedicated
subdirectories for each skill, containing SKILL.md, references, and template assets.

Author: CTiEG (hola@ctieg.com | www.ctieg.com)
Copyright: (c) 2026 CTiEG
License: MIT
"""

import os
import sys

# Define color helper functions for terminal output
def print_success(msg):
    print(f"\033[92m[✓] {msg}\033[0m")

def print_info(msg):
    print(f"\033[94m[*] {msg}\033[0m")

def print_error(msg):
    print(f"\033[91m[✗] {msg}\033[0m")

def print_banner():
    banner = """
======================================================================
  ██████╗████████╗██╗███████╗ ██████╗      ██████╗ ██████╗  ██████╗  ██████╗ 
 ██╔════╝╚══██╔══╝██║██╔════╝██╔════╝     ██╔═══██╗██╔══██╗██╔═══██╗██╔═══██╗
 ██║        ██║   ██║█████╗  ██║  ███╗    ██║   ██║██║  ██║██║   ██║██║   ██║
 ██║        ██║   ██║██╔══╝  ██║   ██║    ██║   ██║██║  ██║██║   ██║██║   ██║
 ╚██████╗   ██║   ██║███████╗╚██████╔╝    ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝
  ╚══════╝   ╚═╝   ╚═╝╚══════╝ ╚═════╝      ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ 
                      CLINE SKILLS REPOSITORY SCAFFOLDER
======================================================================
Owner: CTiEG - hola@ctieg.com - www.ctieg.com
Standard: Agent Skills Day 3 (agentskills.io)
Target: Odoo 16.0 - 19.0 & OCA Compliance
======================================================================
"""
    print(banner)

# Dictionary of all files and their contents
FILES_DATA = {}

# ==============================================================================
# ROOT LEVEL FILES
# ==============================================================================

# 1. .gitignore
FILES_DATA[".gitignore"] = """# Python compiled files
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Secrets and local configurations
.env
secrets.json

# IDEs and editors
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Cline / Claude local runtime files
.cline/history/
.cline/scratch/
"""

# 2. LICENSE
FILES_DATA["LICENSE"] = """MIT License

Copyright (c) 2026 CTiEG

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
"""

# 3. CONTRIBUTING.md
FILES_DATA["CONTRIBUTING.md"] = """# Contributing to Odoo Cline Skills

We welcome contributions from developers, architects, and Odoo specialists around the world! By contributing, you help make AI-assisted Odoo development safer, faster, and more robust for the entire open-source community.

This repository is maintained and governed by **CTiEG** (hola@ctieg.com | [www.ctieg.com](https://www.ctieg.com)).

## Governance & Code of Conduct

1. **Maintain OCA & Odoo 19 Standards**: All technical additions, templates, or instructions must align with official Odoo 19.0+ standards and Odoo Community Association (OCA) coding guidelines.
2. **Adhere to the Day 3 Runbook**: Skills must be written under the **Progressive Disclosure** pattern. Keep `SKILL.md` slim (focusing on metadata, triggers, and the primary high-level workflow), and move raw guides, deprecation lists, or detailed schemas to the `references/` directory. Deterministic code, XML views, or scripts must be bundled inside the `assets/` or `scripts/` directories instead of bloating the prompt context.
3. **Respect License and Copyright**: This project is licensed under the MIT License. Contributions are automatically licensed under the same terms. All copyright notices must preserve the ownership of **CTiEG**.

## How to Contribute

### 1. Propose an Issue
Before writing any code or markdown, open an Issue to discuss your idea. Describe the specific "use-case" or "runbook" you want the AI agent to master, why it's recurring, and what the expected triggers/anti-triggers are.

### 2. Fork and Clone
Fork this repository under your GitHub account, clone it locally, and set up your workspace:
```bash
git clone https://github.com/your-username/odoo-cline-skills.git
cd odoo-cline-skills
```

### 3. Create a Local Branch
Use a clear, descriptive branch name:
```bash
git checkout -b add-skill-managing-backups
```

### 4. Implement the Skill Structure
Ensure your new skill is created as a folder inside `.cline/skills/` following our strict structure:
```text
.cline/skills/your_new_skill_name/
├── SKILL.md                  # Frontmatter + triggers + 7 mandatory sections
├── references/               # Detailed documentation files
└── assets/                   # Reusable code, manifests, or XML templates
```
*Note: The directory name must use `snake_case`, the skill name in YAML must use `kebab-case` and a gerund form (e.g., `managing-backups`).*

### 5. Validate Your Skill
Run our local validation suite before committing to make sure your frontmatter lints correctly and no passwords/secrets are leaked:
```bash
python3 validate_all.py
```

### 6. Open a Pull Request (PR)
Push your changes to your fork and submit a PR against our `main` branch. Provide:
* A clear description of the new capability.
* At least 3 positive and 3 negative triggers tested during your local runs with Cline/VS Code.
* Confirmation that your validation script passes cleanly.

## Need Help?
If you have any questions, feedback, or would like to coordinate commercial AI integrations, feel free to contact us:
* **Email**: hola@ctieg.com
* **Website**: [www.ctieg.com](https://www.ctieg.com)

Thank you for helping us shape the future of agentic Odoo development!
"""

# 4. README.md
FILES_DATA["README.md"] = """# Odoo Cline Skills Suite

[![Odoo Version](https://img.shields.io/badge/Odoo-16.0%20%7C%2017.0%20%7C%2018.0%20%7C%2019.0-purple.svg)](https://www.odoo.com)
[![Cline Standard](https://img.shields.io/badge/Standard-Agent%20Skills%20Day%203-blue.svg)](https://agentskills.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Maintained%20by-CTiEG-orange.svg)](https://www.ctieg.com)

A collection of professional, highly-optimized **Cline Habilidades (Skills)** designed specifically for autonomous software engineering, database query optimization, and external API integration in Odoo ERP (v16.0 to v19.0). 

Developed and maintained by **CTiEG** (hola@ctieg.com | [www.ctieg.com](https://www.ctieg.com)), this repository is engineered under the strict **"Agent Skills_Day_3"** Progressive Disclosure standard. It prevents LLM context overflow ("context rot") by separating routing metadata from thick reference material and templates, enabling Cline in Visual Studio Code to deliver flawless Odoo development trajectories without bloating your session tokens.

---

## 📂 Repository Structure

The suite is structured into folder-contained, progressive-disclosure skills under the `.cline/skills/` directory:

```text
odoo-cline-skills/
├── .cline/
│   └── skills/
│       ├── querying_odoo_xmlrpc/     # Skill 1: JSON-2, XML-RPC & Relational Commands
│       │   ├── SKILL.md              # Triggers & Connection Workflow
│       │   ├── references/           # External API & Auth Key Guides
│       │   └── assets/               # Ready-to-run Client Templates
│       │
│       ├── architecting_odoo_orm/    # Skill 2: Database Performance, Cache & SQL
│       │   ├── SKILL.md              # Prefetching rules & N+1 Prevention
│       │   ├── references/           # Cache flushing, odoo.tools.SQL, & Deprecations
│       │   └── assets/               # Ref. Odoo 19 Task Optimizer Model
│       │
│       └── developing_odoo_modules/  # Skill 3: OCA addon modular scaffolding
│           ├── SKILL.md              # Architecture, views list, & manifest rules
│           ├── references/           # Layered Decoupling, XML & Coding Standards
│           └── assets/               # Security files, templates & views scaffold
│
├── .gitignore                        # Standard Python and Odoo ignore filters
├── LICENSE                           # Official MIT License
├── CONTRIBUTING.md                   # Contribution guides & CTiEG governance
├── test_odoo_xmlrpc.py               # Production-ready safe client script
└── install_skills.py                 # Automatic project scaffolder script
```

---

## ⚡ Installation Instructions

### Prerequisites
* **Visual Studio Code** installed.
* **Cline** extension installed and enabled.
* Active LLM configured in Cline (Claude 3.5 Sonnet or Gemini 1.5 Pro recommended).

### Automated Installation
To install the complete suite directly into your local project in a single command, download and run our installer script:

```bash
python3 install_skills.py
```

This will automatically create the `.cline/skills/` directory structure, write all files, reference documents, and assets, and output a confirmation trace.

### Manual Verification
1. Open the Cline settings panel in VS Code.
2. Go to **Advanced Features** and ensure **Enable Skills** is toggled **ON**.
3. Verify that the three subdirectories (`querying_odoo_xmlrpc`, `architecting_odoo_orm`, `developing_odoo_modules`) exist under your project root `.cline/skills/`.
4. Cline will automatically discover and load these skills on-demand whenever your chat instructions trigger Odoo API, ORM, or modular development keywords!

---

## 🛠️ The Skills Library in Detail

### 1. Querying Odoo XML-RPC & JSON-2 (`querying_odoo_xmlrpc`)
Teaches Cline to integrate with Odoo databases externally.
* **Triggers**: "Connect via XML-RPC", "Odoo external API", "JSON-2 API endpoint", "Create partner remotely".
* **Key capabilities**: Protocol-compliance with Odoo 19's new **JSON-2 HTTP API** (`/json/2`), deprecation mapping of traditional XML-RPC (scheduled for removal in Odoo 22), programmatic API key creation/rotation, and the complete 3-element tuple relation commands (e.g. `(6, 0, [IDs])`).

### 2. Architecting Odoo ORM (`architecting_odoo_orm`)
Instructs Cline on advanced Odoo database engineering and performance optimization.
* **Triggers**: "Optimize Odoo query", "ValidationError constraint", "SQL execution in Odoo 19", "Compute display name".
* **Key capabilities**: Mitigating the N+1 database call problem through recordsets and prefetching, using PostgreSQL group aggregations via `_read_group()`, writing safe, parameterized SQL via the Odoo 19 `execute_query()` and `odoo.tools.SQL` wrapper, and controlling the transactional cache (flushing, invalidation, and dependency tracking).

### 3. Developing Odoo Modules (`developing_odoo_modules`)
Rules for building clean, maintainable Odoo addons following OCA standards.
* **Triggers**: "Scaffold new OCA module", "Create Odoo views list", "Manifest with depends_if_installed", "Security groups XML".
* **Key capabilities**: Implementing a **two-layer decoupling strategy** (separating persistent fields in `_data` modules from XPath views in `_app` modules to survive major-version migrations), renaming `<tree>` views to `<list>` in Odoo 18+, and standardizing XML External IDs and access CSV matrices.

---

## 🤝 Community & Support

This suite is implemented, packaged, and published by **CTiEG**. We are committed to empowering organizations with automated, high-performance, and secure AI-assisted software engineering. 

If you are looking for custom AI agents, ERP integrations, or Odoo consulting, please connect with us:

* **Email**: hola@ctieg.com
* **Website**: [www.ctieg.com](https://www.ctieg.com)
* **Contributions**: Please check out `CONTRIBUTING.md` before submitting Pull Requests.

---

*Copyright (c) 2026 CTiEG. Licensed under the MIT License.*
"""

# 5. test_odoo_xmlrpc.py
FILES_DATA["test_odoo_xmlrpc.py"] = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
CTiEG Odoo XML-RPC Integration Test Client
-------------------------------------------
This script demonstrates safe, optimized external connection to an Odoo database.
Following the querying-odoo-xmlrpc skill standards, it:
1. Prevents hardcoded credentials by pulling from environment variables.
2. Uses the native python library xmlrpc.client (no external pip dependencies).
3. Selects fields explicitly to prevent heavy computed field overhead.
4. Leverages search_read in a single transaction trip to prevent network lag.

Author: CTiEG (hola@ctieg.com | www.ctieg.com)
Copyright: (c) 2026 CTiEG
License: MIT
\"\"\"

import os
import sys
import xmlrpc.client

def run_integration_test():
    print("================================================================")
    print("      CTIEG ODOO EXTERNAL API INTEGRATION TESTER                ")
    print("================================================================")

    # 1. Safely retrieve credentials from environment variables
    url = os.getenv("ODOO_URL")
    db = os.getenv("ODOO_DB")
    username = os.getenv("ODOO_USER")
    api_key = os.getenv("ODOO_API_KEY")

    if not all([url, db, username, api_key]):
        print("[✗] Error: Missing one or more required environment variables.")
        print("    Please set ODOO_URL, ODOO_DB, ODOO_USER, and ODOO_API_KEY in your system.")
        print("\\n    Example:")
        print("    export ODOO_URL=\\"https://mycompany.odoo.com\\"")
        print("    export ODOO_DB=\\"mycompany_db\\"")
        print("    export ODOO_USER=\\"integrator@mycompany.com\\"")
        print("    export ODOO_API_KEY=\\"your_generated_user_api_key\\"")
        print("================================================================")
        sys.exit(1)

    print(f"[*] Endpoint Target: {url}")
    print(f"[*] Target Database : {db}")
    print(f"[*] Connecting as   : {username}")

    try:
        # 2. Establish connection to the common endpoint (unauthenticated queries)
        print("[*] Contacting server version common service...")
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        version_info = common.version()
        print(f"[✓] Connection successful! Odoo Server Version: {version_info.get('server_version')}")

        # 3. Authenticate with Odoo to receive user ID (uid)
        print("[*] Authenticating with Odoo using API Key...")
        uid = common.authenticate(db, username, api_key, {})
        if not uid:
            print("[✗] Error: Authentication denied. Check your URL, DB, Username, and API Key.")
            sys.exit(1)
        print(f"[✓] Authenticated successfully. Received UID: {uid}")

        # 4. Establish connection to the object endpoint for transactional methods
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

        # 5. Execute search_read on res.partner (Customers) with explicit fields and limits
        print("[*] Performing optimized search_read on 'res.partner'...")
        model_name = "res.partner"
        domain = [("active", "=", True), ("is_company", "=", True)]
        
        # Explicit fields selection to protect server RAM and speed up query response
        kwargs = {
            "fields": ["id", "name", "email", "phone"],
            "limit": 5,
            "order": "name asc"
        }

        records = models.execute_kw(db, uid, api_key, model_name, "search_read", [domain], kwargs)
        
        print(f"[✓] Successfully retrieved {len(records)} active company records:\\n")
        for record in records:
            print(f"    - ID: {record.get('id')} | Name: {record.get('name')}")
            print(f"      Email: {record.get('email') or 'N/A'} | Phone: {record.get('phone') or 'N/A'}")
            print("    " + "-"*50)

        print("[✓] Odoo XML-RPC Integration Test successfully finished.")
        print("================================================================")

    except xmlrpc.client.Fault as fault:
        print(f"[✗] Odoo Server Exception Occurred!")
        print(f"    Fault Code  : {fault.faultCode}")
        print(f"    Fault String: {fault.faultString}")
        print("================================================================")
        sys.exit(1)
    except Exception as e:
        print(f"[✗] Network or Connection Error: {str(e)}")
        print("================================================================")
        sys.exit(1)

if __name__ == "__main__":
    run_integration_test()
"""

# ==============================================================================
# SKILL 1: querying_odoo_xmlrpc
# ==============================================================================

FILES_DATA[".cline/skills/querying_odoo_xmlrpc/SKILL.md"] = """---
name: querying-odoo-xmlrpc
description: |
  Masters remote database querying, record synchronization, and data integration on Odoo instances (v16.0 to v19.0).
  Use when the user requests connection code to an external Odoo API, executing CRUD actions over HTTP, handling Many2many relation Command tuples, managing API Keys, or implementing Odoo 19 JSON-2 HTTP queries.
  Do NOT use for internal addon development, custom model database definitions, or writing views XML (refer to developing-odoo-modules instead).
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG (hola@ctieg.com | www.ctieg.com)
  copyright: (c) 2026 CTiEG
---

# querying-odoo-xmlrpc

## When to use
* **External Integrations**: When writing scripts, API bridges, or external programs that communicate with Odoo.
* **Many2many / One2many Writes**: When generating external operations that alter relational fields using Odoo's Command tuples.
* **Modern JSON-2 Integrations**: When connecting external clients on Odoo 19.0+ using the standard HTTP endpoints.

## When NOT to use
* **Internal Code**: Writing Python logic inside a custom module.
* **Database definitions**: Declaring new persistent Odoo models.
* **UI Views**: Modifying XML forms or layout menus.

## Workflow

1. **Gobernanza de Credenciales y Seguridad**:
   * **Prohibit Hardcoded Secrets**: Ensure that credentials (User pass, URL, DB, API Keys) are extracted from system environment variables (`os.environ`).
   * **Enforce API Keys**: For Odoo v14.0+, enforce generating and utilizing API Keys in place of the account login password to secure the system against OAuth and 2FA logins.

2. **Garantía de Rendimiento en Consultas**:
   * **Mandatory Field Selection**: When executing `read` or `search_read`, Cline MUST explicitly define a list of fields in the arguments. Fetching unrestricted records loads expensive server-side computed fields and can crash Odoo's memory.
   * **Use search_read over separate search + read**: Combine search and read in a single call to save network round trips.
   * **Enforce Pagination**: Never retrieve open datasets; always apply safe limit and offset parameters.

3. **Relationship Tuple Command Protocol**:
   When writing to relational fields (Many2many or One2many), use Odoo's 3-element tuple Command protocol:
   `CommandValue` format: `(command_code, related_record_id, values_or_ids)`

   | Code | Constant | Operation | Description |
   | :--- | :--- | :--- | :--- |
   | `0` | `CREATE` | Create and Link | Creates a new record in the comodel and links it. |
   | `1` | `UPDATE` | Update Linked | Writes values on the related record with specified ID. |
   | `2` | `DELETE` | Delete and Unlink | Physically deletes the record from DB and removes relation. |
   | `3` | `UNLINK` | Unlink Only | Removes the relation without deleting the child record. |
   | `4` | `LINK` | Link Existing | Links an already existing record to the current record. |
   | `5` | `CLEAR` | Clear All Links | Removes all relations from the list without deleting records. |
   | `6` | `SET` | Replace Set | Replaces the list of relations with exactly the specified list of IDs. |

4. **Reference Implementation & Guides**:
   * Refer to `references/xmlrpc_api_guide.md` for XML-RPC and traditional endpoints.
   * Refer to `references/json2_api_guide.md` for Odoo 19 JSON-2 API specifications.
   * Use `assets/xmlrpc_client_template.py` and `assets/json2_client_template.py` as boilerplate templates.

## Examples
Input: "Write a script to remotely create an Odoo customer and link three tag IDs: [1, 2, 3]."
Output: Refer to `assets/xmlrpc_client_template.py` or use the command code `(6, 0, [1, 2, 3])` inside the dictionary values.

## Output format
* Keep the python files clean and self-documenting.
* Clearly specify environment variable extraction at the start of any Python file.

## Anti-patterns to avoid
* **No fields filter**: Omitting the `fields` filter in `read` or `search_read` is a critical performance error.
* **Password exposure**: Storing the user's local password directly inside code repositories.
* **No XML-RPC transaction pooling**: Making hundreds of separate individual RPC calls inside a Python loop instead of using single, consolidated batch calls.
"""

FILES_DATA[".cline/skills/querying_odoo_xmlrpc/references/xmlrpc_api_guide.md"] = """# Odoo XML-RPC & JSON-RPC Traditional API Guide

Odoo traditionally exposes its Models API over XML-RPC and JSON-RPC, enabling external clients to perform CRUD operations on database models.

## Endpoints

Odoo traditional RPC uses two main HTTP POST endpoints:
1. `/xmlrpc/2/common`: Handling non-authenticated requests (such as server version metadata and logins).
2. `/xmlrpc/2/object`: Handling model-level queries and executing transactional Python methods via `execute_kw`.

## Core Methods Mapped in execute_kw

1. **check_access_rights**: Validates if the user UID holds necessary access rights (`read`, `write`, `create`, `unlink`) for the given model.
2. **search**: Filters database identifiers (IDs) matching a domain logic.
3. **search_count**: Counts matching records without retrieving them.
4. **read**: Fetches field values for a specific list of record IDs.
5. **search_read**: Optimizes queries by performing a combined search and read in a single SQL execution transaction.
6. **create**: Persists a new record. Accepts a dictionary of values.
7. **write**: Modifies existing records in bulk. Accepts a list of IDs and a dictionary of updated values.
8. **unlink**: Deletes records by ID.

## Performance Optimization

* **Network Latency**: Never use separate `search` and `read` queries in succession; use `search_read` to save network round trips.
* **Memory Limits**: Never call `read` without a `fields` filter. Loading computed fields across hundreds of records in memory can trigger Odoo server out-of-memory crashes.
"""

FILES_DATA[".cline/skills/querying_odoo_xmlrpc/references/json2_api_guide.md"] = """# Odoo 19 External JSON-2 API Guide

Introduced in Odoo 19.0, the **JSON-2 HTTP API** replaces traditional XML-RPC/JSON-RPC protocols, which are officially scheduled for **complete removal in Odoo 22 (Fall 2028)**.

## Protocol Architecture

The JSON-2 API uses standard JSON over HTTP POST, targeted directly at the `/json/2/<model>/<method>` URL.

### HTTP Headers
* `Host`: The hostname of the Odoo server.
* `Authorization`: `bearer <API_KEY>` (Replaces password login completely).
* `Content-Type`: `application/json`
* `X-Odoo-Database`: The target database name (mandatory on multi-database servers).

### Request Payload Shape
The POST body must be a single JSON object containing:
* `ids`: An array of integer record IDs to execute the method on. Omit or pass empty for `@api.model` decorated methods.
* `context`: (Optional) An object representing dictionary overrides (e.g. `{"lang": "en_US"}`).
* Method parameters as named JSON keys (positional arguments are not supported in JSON-2).

## Programmatic API Key Management

For automated deployments, Odoo 19 allows programmatic generation and rotation of keys under the models:
* `res.users.apikeys.generate(key, scope, name, expiration_date)`
* `res.users.apikeys.revoke(key)`

## Key Rotation Best Practices
1. Generate the new key using the valid existing key.
2. Store the new key securely in the target environment.
3. Verify that the client can communicate with the new key.
4. Revoke the previous key immediately after validation.
"""

FILES_DATA[".cline/skills/querying_odoo_xmlrpc/assets/xmlrpc_client_template.py"] = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import xmlrpc.client

def get_odoo_connection():
    url = os.environ.get("ODOO_URL")
    db = os.environ.get("ODOO_DB")
    username = os.environ.get("ODOO_USER")
    api_key = os.environ.get("ODOO_API_KEY")

    if not all([url, db, username, api_key]):
        raise ValueError("Missing environment variables. Set ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY.")

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, api_key, {})
    if not uid:
        raise xmlrpc.client.Fault(401, "Authentication denied.")
    
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return db, api_key, uid, models

def fetch_partners_safely():
    db, api_key, uid, models = get_odoo_connection()
    
    # Combined search and read inside a single SQL query transaction
    domain = [("active", "=", True)]
    kwargs = {
        "fields": ["id", "name", "email"], # Strict fields filter to protect server RAM
        "limit": 10,
        "offset": 0,
        "order": "name asc"
    }
    
    return models.execute_kw(db, uid, api_key, "res.partner", "search_read", [domain], kwargs)
"""

FILES_DATA[".cline/skills/querying_odoo_xmlrpc/assets/json2_client_template.py"] = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

def odoo_json2_request(model, method, ids=None, context=None, **params):
    url = os.environ.get("ODOO_URL")
    db = os.environ.get("ODOO_DB")
    api_key = os.environ.get("ODOO_API_KEY")

    if not all([url, db, api_key]):
        raise ValueError("Missing environment variables.")

    endpoint = f"{url}/json/2/{model}/{method}"
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json",
        "X-Odoo-Database": db,
        "User-Agent": "CTiEG-Integrator/1.0"
    }

    payload = {
        "ids": ids or [],
        "context": context or {}
    }
    # Unpack extra kwargs as named parameters
    payload.update(params)

    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
"""

# ==============================================================================
# SKILL 2: architecting_odoo_orm
# ==============================================================================

FILES_DATA[".cline/skills/architecting_odoo_orm/SKILL.md"] = """---
name: architecting-odoo-orm
description: |
  Optimizes database queries, transaction boundaries, and computed fields in Odoo 19.0.
  Use when the user requests database query performance tuning, fixing N+1 database bottlenecks, writing computed fields with depends context, executing raw SQL securely, or invalidating the ORM cache.
  Do NOT use for creating remote connections over XML-RPC or JSON-2 (refer to querying-odoo-xmlrpc instead).
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG (hola@ctieg.com | www.ctieg.com)
  copyright: (c) 2026 CTiEG
---

# architecting-odoo-orm

## When to use
* **Database Performance Tuning**: Preventing massive relational loop queries by leveraging recordset bulk operations.
* **Secure SQL Composition**: Writing parameterized raw database statements using Odoo 19's SQL wrappers.
* **Transactional Caching**: Managing cache coherency when writing low-level database scripts.

## When NOT to use
* **External APIs**: Writing standalone HTTP client scripts.
* **Andamiaje de Módulos**: Setting up manifest files, directory rules, or views XML.

## Workflow

1. **Evitación de Consultas en Ciclos (Problema N+1)**:
   * **Enforce Prefetching**: Never search or browse individual record IDs inside Python `for` loops. Iterate over bulk recordsets so that Odoo's prefetching cache loads fields in a single PostgreSQL query trip.
   * **Avoid Loops on write()**: Write values in batch (`records.write({'state': 'confirmed'})`) instead of loop iterations.
   * **Database-level Aggregation**: Do NOT sum or average fields in Python loops. Always use `_read_group()` to push calculations directly to PostgreSQL.

2. **Gobernanza Transaccional y de Caché**:
   * **Strictly Prohibit Manual Commits**: Cline is forbidden from calling `cr.commit()` or `cr.rollback()` in custom backend logic, as this breaks test rollbacks and triggers severe data inconsistencies.
   * **Use Savepoints**: To isolate potential errors safely within loop structures, use transaction savepoints: `with self.env.cr.savepoint():`

3. **Secure SQL Composition (Odoo 19 Standards)**:
   * **Prohibit Direct `cr.execute()` Concatenations**: Prevent SQL injection by composing queries exclusively with the `odoo.tools.SQL` wrapper and executing them using `self.env.execute_query(sql)`.
   * **Manage Cache Flush and Invalidation**: Before running direct SQL, flush Odoo's model cache (`self.flush_model()`). After execution, invalidate the records cache (`self.invalidate_model()`) and alert Odoo of changed fields using `self.modified()`.

4. **Reference Implementation & Guides**:
   * Refer to `references/orm_performance.md` for prefetching mechanisms.
   * Refer to `references/sql_execution_cache.md` for Odoo 19 cache-aware query patterns.
   * Refer to `references/odoo19_deprecations.md` for deprecated API calls.
   * Use `assets/task_optimizer_model.py` as a complete, OCA-compliant model baseline.

## Examples
Input: "Write an aggregate query to get the sum of hours grouped by partner."
Output: Refer to `_read_group()` usage inside `references/orm_performance.md`.

## Output format
* All backend code must use proper Odoo 19 imports.
* Computed methods must be private, starting with a single underscore.

## Anti-patterns to avoid
* **`record._cr` usage**: Use `record.env.cr` instead.
* **`read_group` calls**: Deprecated in Odoo 18; use `_read_group()` instead.
* **No `ensure_one()`**: Forgetting to add `self.ensure_one()` at the start of instance methods.
"""

FILES_DATA[".cline/skills/architecting_odoo_orm/references/orm_performance.md"] = """# Odoo ORM Prefetching & Performance Guide

The Odoo ORM automatically pre-fetches records of the same prefetch-set (usually the recordset from which a record comes by iteration) to avoid the $N+1$ query problem.

## The N+1 Query Problem Explained

Executing one database query to fetch records, and then running another query *for each record* inside a loop.

### Naive Iteration (101 Queries for 100 records)
```python
# Anti-pattern: rompemos la precarga
for partner_id in partner_ids:
    partner = self.browse(partner_id)
    print(partner.name) # Una consulta SQL por cada registro
```

### Prefetched Iteration (1 Query)
```python
# Odoo loads the names of all partners in the prefetch set at once
partners = self.browse(partner_ids)
for partner in partners:
    print(partner.name) # Una sola consulta SQL para todo el lote
```

## Disabling Prefetching
If you must isolate a specific record and prevent it from fetching sibling values in bulk, use `with_prefetch()`:
```python
isolated_record = record.with_prefetch(False)
```

## read_group vs _read_group
* **`read_group()`**: Deprecated in Odoo 18.0.
* **`_read_group(domain, groupby, aggregates)`**: The official, high-performance Odoo 19 query aggregation method.
"""

FILES_DATA[".cline/skills/architecting_odoo_orm/references/sql_execution_cache.md"] = """# Odoo 19 SQL Execution & Cache Management

Odoo delays database persistence for performance reasons, meaning some computed fields or updates remain in the memory cache before being written to PostgreSQL.

## execute_query vs cr.execute
Odoo 19 introduces `self.env.execute_query()` as a safe, cache-aware SQL execution method.

```python
# Safe, composable query with automatic dependency metadata injection
from odoo.tools import SQL
query = SQL(
    "SELECT id, name FROM res_partner WHERE country_id = %s", 
    country_id
)
records = self.env.execute_query(query)
```

## Transaction Cache Governance

When executing custom SQL statements, you bypass the ORM layer entirely. You MUST manually handle Odoo's caches:

1. **Flush cache**: Force write Odoo memory modifications to PostgreSQL before executing the SQL statement:
   `self.flush_model(fnames)` or `self.flush_recordset(fnames)`
2. **Invalidate cache**: Clear outdated memory caches after execution:
   `self.invalidate_model(fnames)` or `self.invalidate_recordset(fnames)`
3. **Notify changes**: Inform Odoo's dependency engine that fields have been modified to trigger dependent calculations:
   `self.modified(fnames)`
"""

FILES_DATA[".cline/skills/architecting_odoo_orm/references/odoo19_deprecations.md"] = """# Odoo 19 Backend Deprecations & Replacements

Ensure Cline never utilizes deprecated methods or APIs. Use this list during code refactoring:

| Deprecated Call | Odoo 19 Replacement | Notes |
| :--- | :--- | :--- |
| `record._cr` | `record.env.cr` | Direct cursor access deprecated. |
| `record._context` | `record.env.context` | Use the environment context directly. |
| `record._uid` | `record.env.uid` | Extract UID from Environment. |
| `name_get()` | `_compute_display_name()` | Extinct in Odoo 18; must override display_name. |
| `read_group()` | `_read_group()` | Deprecated in Odoo 18.0; use native _read_group. |
| `odoo.osv` | *None* | Legacy osv namespace is fully deprecated. |
| `attrs="..."` | Atributes inline | XML `attrs` attribute deleted. Use inline `invisible`, `readonly`. |
| `<tree>` | `<list>` | Listview root tag renamed in v18. |
"""

FILES_DATA[".cline/skills/architecting_odoo_orm/assets/task_optimizer_model.py"] = """# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTaskOptimizer(models.Model):
    _name = "project.task.optimizer"
    _description = "Advanced Task Optimizer"
    _order = "sequence, id desc"
    _check_company_auto = True

    name = fields.Char(string="Title", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('done', 'Completed')
    ], string="State", default="draft", required=True)
    
    company_id = fields.Many2one(
        'res.company', string="Company", 
        default=lambda self: self.env.company, required=True
    )
    
    partner_id = fields.Many2one(
        'res.partner', string="Customer", 
        check_company=True, index="btree"
    )
    
    estimated_hours = fields.Float(string="Estimated Hours")
    discount_rate = fields.Float(string="Discount Rate", default=0.0)
    
    cost_total = fields.Monetary(
        compute="_compute_cost_total", 
        currency_field="currency_id", 
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency', related="company_id.currency_id", store=True
    )

    # Odoo 19 modern naming computed display_name
    @api.depends('name', 'state')
    def _compute_display_name(self):
        for record in self:
            state_label = dict(self._fields['state'].selection(self)).get(record.state, '')
            record.display_name = f"[{state_label.upper()}] {record.name}"

    # Stored computed field with precise dependencies
    @api.depends('estimated_hours', 'discount_rate')
    def _compute_cost_total(self):
        for record in self:
            base_rate = 50.0
            net_rate = base_rate * (1.0 - (record.discount_rate / 100.0))
            record.cost_total = record.estimated_hours * net_rate

    # Database-level constraint validation
    @api.constrains('estimated_hours', 'discount_rate')
    def _check_task_values(self):
        for record in self:
            if record.estimated_hours <= 0:
                raise ValidationError(_("Estimated hours must be strictly positive."))
            if not (0.0 <= record.discount_rate <= 100.0):
                raise ValidationError(_("Discount rate must be between 0% and 100%."))

    # Batch creation support
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = _("Untitled Task")
        return super(ProjectTaskOptimizer, self).create(vals_list)

    # Safe delete prevention
    @api.ondelete(at_uninstall=False)
    def _prevent_done_deletion(self):
        for record in self:
            if record.state == 'done':
                raise ValidationError(_("You cannot delete completed records."))
"""

# ==============================================================================
# SKILL 3: developing_odoo_modules
# ==============================================================================

FILES_DATA[".cline/skills/developing_odoo_modules/SKILL.md"] = """---
name: developing-odoo-modules
description: |
  Scaffolds, structures, and standardizes backend Odoo custom modules (v16.0 to v19.0) in accordance with the Odoo Community Association (OCA).
  Use when the user requests scaffolding a new Odoo addon, writing manifest files, organizing physical layers, creating form or list views XML, defining security matrices (CSV, rules), or establishing upgrade compatibility.
  Do NOT use for writing standalone remote query scripts (refer to querying-odoo-xmlrpc instead).
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
metadata:
  author: CTiEG (hola@ctieg.com | www.ctieg.com)
  copyright: (c) 2026 CTiEG
---

# developing-odoo-modules

## When to use
* **Scaffolding Addons**: Establishing physical directory layouts for modular Odoo extensions.
* **UI Views Definition**: Coding standard backoffice views (form, list, search) conforming to the target Odoo version.
* **Manifest Governance**: Writing `__manifest__.py` files with metadata and version keys.

## When NOT to use
* **Low-level Query Tuning**: Direct SQL composition or cache modification queries.
* **Remote Clients**: Setting up XML-RPC connection scripts.

## Workflow

1. **Estrategia de Desacoplamiento (Saneamiento de Migración)**:
   To ensure upgrade safety and zero downtime during Odoo major-version updates, Cline MUST promote the **Two-Layer Decoupling Strategy** for modular addons:
   * **Persistence Layer (`<addon_name>_data`)**: Exclusively containing Python models, database columns, SQL constraints, access groups, and ir.model.access.csv. This layer contains no views or UI references, meaning it migrates with zero SQL errors.
   * **App / Interface Layer (`<addon_name>_app`)**: Containing XML layout forms, window actions, menus, web controllers, and QWeb reports. This layer can be temporarily disabled during major DB schema migrations and safely refactored in isolation.

2. **OCA Directory Structure**:
   Ensure strict separation of directories: `models/`, `views/`, `security/`, `data/`, `demo/`, `tests/`, `static/`, and `wizard/`. Refer to `references/python_coding_standards.md` for import ordering and conventions.

3. **XML Formatting & IDs Naming Scheme**:
   * **Root tag renamed**: For Odoo 18.0+, all list view XML definitions must replace the deprecated `<tree>` root tag with `<list>`.
   * **Attributes inline**: Never use the dictionary `attrs` parameter for conditional visibility on Odoo 17+ (use inline boolean parameters).
   * **Aislación de Menús**: Extract top-level or structural menus into a dedicated `views/<module_name>_menus.xml` file to prevent install-time cyclical dependency errors.

4. **Reference Implementation & Guides**:
   * Refer to `references/layered_decoupling_strategy.md` for migration design.
   * Refer to `references/xml_views_menus_guide.md` for Odoo 18/19 XML syntax.
   * Refer to `references/python_coding_standards.md` for styling guidelines.
   * Use `assets/manifest_template.py`, `assets/security_groups.xml`, `assets/ir.model.access.csv`, and `assets/views_menus_template.xml` as boilerplate scaffolds.

## Examples
Input: "Scaffold an Odoo 19 Sales Performance module under OCA rules."
Output: Build the physical layers and write files using the template assets located in the assets/ folder.

## Output format
* Use `LGPL-3` or `AGPL-3` license keys in manifest configurations.
* Enforce semantic versioning according to OCA rules (`{Odoo Major}.{x}.{y}.{z}`).

## Anti-patterns to avoid
* **Tree tag on v18**: Declaring list views using the `<tree>` tag on Odoo 18/19.
* **Nested menus in views**: Bloating form view XMLs by inserting `<menuitem>` tags directly next to layout definitions.
* **No `ir.model.access.csv`**: Every custom model must have an explicit security access permission, otherwise users will hit Access Denied errors.
"""

FILES_DATA[".cline/skills/developing_odoo_modules/references/layered_decoupling_strategy.md"] = """# Layered Decoupling Strategy for Odoo Custom Addons

Major version upgrades are high-risk operations in ERP life cycles, usually causing data loss or severe downtime because layout views break under updated database schemas.

## The Decoupling Pattern

To isolate physical data from volatile visual layouts, we split a feature into two distinct addons:

### 1. Persistence Layer (`my_module_data`)
* **Contains**: Models, fields, PostgreSQL indexes, security groups, model access CSV, data files (`noupdate="1"`).
* **Restrictions**: Absolutely NO XML views, menus, window actions, or QWeb reports.
* **Migration Advantage**: It can be migrated first and safely. It carries zero UI dependencies, preventing OpenUpgrade schema migration crashes.

### 2. Application Layer (`my_module_app`)
* **Contains**: Views, actions, menus, reports, SCSS assets, web controllers.
* **Restrictions**: Declares no new database fields (only inherits view behaviors).
* **Migration Advantage**: Can be safely uninstalled or disabled before schema updates, preventing UI breakage from locking the main database migration process.
"""

FILES_DATA[".cline/skills/developing_odoo_modules/references/xml_views_menus_guide.md"] = """# Odoo 18 & 19 XML View and Menu Standards

Ensure all XML declarations meet modern Odoo 19.0 specifications.

## 1. tree vs list root tags (v18+)

The classic `<tree>` root tag is completely obsolete and removed in Odoo 18. Any list view must use `<list>`:

```xml
<!-- GOOD -->
<record id="my_model_view_list" model="ir.ui.view">
    <field name="name">my.model.view.list</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <list string="My Records">
            <field name="name"/>
        </list>
    </field>
</record>
```

## 2. Dynamic visibility inline (v17+)

Dictionary-styled `attrs` are obsolete. Define attributes inline:

```xml
<!-- GOOD -->
<field name="partner_id" invisible="state == 'draft'" readonly="state == 'done'" required="state == 'progress'"/>
```

## 3. Menu Separation

To prevent cyclical install errors, isolate all parent/child `<menuitem>` tags inside `views/<module_name>_menus.xml`.
"""

FILES_DATA[".cline/skills/developing_odoo_modules/references/python_coding_standards.md"] = """# OCA Python Coding Standards

All custom code must follow PEP8 guidelines and the Odoo Community Association guidelines.

## 1. Import Ordering

Import statements must be ordered alphabetically within three strict groups:
1. Standard / External libraries (one per line, e.g. `import os`, `import logging`).
2. Odoo core submodules (e.g. `from odoo import models, fields, api, _`).
3. Odoo third-party addons (rare, only if absolutely necessary).

```python
# GOOD
import logging
import os

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
```

## 2. Odoo Idiomatic Code

* **Recordsets operations**: Always favor recordset helpers (`filtered()`, `mapped()`, `sorted()`) over writing Python loops wherever possible.
* **Context propagation**: Never overwrite `self.env.context` as a standard dictionary. Use `with_context()` to pass dynamic overrides safely without side effects:
  `records.with_context(mail_notrack=True).write({'state': 'done'})`
"""

FILES_DATA[".cline/skills/developing_odoo_modules/assets/manifest_template.py"] = """# -*- coding: utf-8 -*-
{
    "name": "Sales Performance Optimizer (OCA Standard)",
    "summary": "Advanced metrics and analytics for sales team targets",
    "version": "18.0.1.0.0", # Strict OCA SemVer format
    "category": "Sales",
    "author": "CTiEG",
    "license": "LGPL-3",
    "website": "https://www.ctieg.com",
    "depends": [
        "sale_management",
        "mail"
    ],
    # Dynamic conditional dependencies
    "depends_if_installed": {
        "board": ["views/sales_performance_dashboard.xml"]
    },
    "data": [
        "security/sales_performance_groups.xml",
        "security/ir.model.access.csv",
        "views/sales_performance_optimizer_views.xml",
        "views/sales_performance_menus.xml"
    ],
    "demo": [
        "demo/sales_performance_demo.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
"""

FILES_DATA[".cline/skills/developing_odoo_modules/assets/security_groups.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="module_category_sales_performance" model="ir.module.category">
            <field name="name">Sales Performance</field>
            <field name="sequence">20</field>
        </record>

        <record id="group_sales_performance_user" model="res.groups">
            <field name="name">Analyst User</field>
            <field name="category_id" ref="module_category_sales_performance"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>

        <record id="group_sales_performance_manager" model="res.groups">
            <field name="name">Analyst Manager</field>
            <field name="category_id" ref="module_category_sales_performance"/>
            <field name="implied_ids" eval="[(4, ref('group_sales_performance_user'))]"/>
            <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
        </record>
    </data>
</odoo>
"""

FILES_DATA[".cline/skills/developing_odoo_modules/assets/ir.model.access.csv"] = """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sales_performance_user,sales.performance.user,model_project_task_optimizer,group_sales_performance_user,1,1,1,0
access_sales_performance_manager,sales.performance.manager,model_project_task_optimizer,group_sales_performance_manager,1,1,1,1
"""

FILES_DATA[".cline/skills/developing_odoo_modules/assets/views_menus_template.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Forms view with inline conditional parameters -->
    <record id="project_task_optimizer_view_form" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.form</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <form string="Task Optimizer Form">
                <header>
                    <button name="action_confirm" string="Confirm" type="object" class="oe_highlight" invisible="state != 'draft'"/>
                    <field name="state" widget="statusbar" statusbar_visible="draft,progress,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="E.g. Task name..."/>
                        </h1>
                    </div>
                    <group>
                        <group name="left_details">
                            <field name="partner_id" readonly="state == 'done'"/>
                            <field name="company_id" readonly="state == 'done'"/>
                        </group>
                        <group name="right_metrics">
                            <field name="estimated_hours" readonly="state == 'done'"/>
                            <field name="discount_rate" readonly="state == 'done'"/>
                            <field name="cost_total"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Modern v18/19 List view replacing legacy tree tag -->
    <record id="project_task_optimizer_view_list" model="ir.ui.view">
        <field name="name">project.task.optimizer.view.list</field>
        <field name="model">project.task.optimizer</field>
        <field name="arch" type="xml">
            <list string="Tasks" decoration-info="state == 'draft'" decoration-success="state == 'done'">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="estimated_hours" sum="Total hours"/>
                <field name="cost_total" sum="Total cost"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="project_task_optimizer_action" model="ir.actions.act_window">
        <field name="name">Performance Analysis</field>
        <field name="res_model">project.task.optimizer</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first commercial task optimization record.
            </p>
        </field>
    </record>
</odoo>
"""

# 6. .cline/skills/developing_odoo_modules/assets/views_menus_template.xml menu list
FILES_DATA[".cline/skills/developing_odoo_modules/assets/views_menus_list.xml"] = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="menu_sales_performance_root" 
              name="Performance Analysis" 
              parent="sale.menu_sale_config" 
              sequence="50"/>

    <menuitem id="menu_sales_performance_optimizer" 
              name="Analysis Tasks" 
              parent="menu_sales_performance_root" 
              action="project_task_optimizer_action" 
              sequence="10"/>
</odoo>
"""

# ==============================================================================
# INSTALLER LOGIC
# ==============================================================================

def main():
    print_banner()
    print_info("Starting the Odoo Cline Skills Repository Scaffolder...")

    # Establish target working directory (the current directory where the script is run)
    target_dir = os.getcwd()
    print_info(f"Target Project Directory: {target_dir}")

    # Counter for successfully written files
    success_count = 0

    for file_path, content in FILES_DATA.items():
        # Build the absolute path for target files
        abs_path = os.path.join(target_dir, file_path)
        
        # Ensure parent directories exist
        parent_dir = os.path.dirname(abs_path)
        if not os.path.exists(parent_dir):
            try:
                os.makedirs(parent_dir, exist_ok=True)
            except Exception as e:
                print_error(f"Failed to create directory {parent_dir}: {str(e)}")
                sys.exit(1)

        # Write content inline to file
        try:
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\\n")
            print_success(f"Generated: {file_path}")
            success_count += 1
        except Exception as e:
            print_error(f"Failed to write file {file_path}: {str(e)}")
            sys.exit(1)

    # Specific file post-processing (e.g. setting permissions on test_odoo_xmlrpc.py)
    test_script_path = os.path.join(target_dir, "test_odoo_xmlrpc.py")
    if os.path.exists(test_script_path):
        try:
            os.chmod(test_script_path, 0o755)
            print_success("Set execute permissions (0755) on test_odoo_xmlrpc.py")
        except Exception as e:
            print_info(f"Could not apply chmod 0755: {str(e)} (Might be on a Windows filesystem)")

    print("\\n======================================================================")
    print_success(f"Successfully generated {success_count} files in the project workspace.")
    print_info(" Cline Skills structure perfectly matches the 'Agent Skills Day 3' runbook.")
    print_info("Developed by: CTiEG (hola@ctieg.com | www.ctieg.com)")
    print("======================================================================\\n")

if __name__ == "__main__":
    main()
