# Odoo Cline Skills Suite

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

*Copyright (c) 2026 CTiEG. Licensed under the MIT License.*\n