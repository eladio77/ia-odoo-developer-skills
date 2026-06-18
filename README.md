# Odoo Cline Agentic Skills Library

A set of **Skills for Cline and VS Code** designed by **CTiEG** to train Artificial Intelligence agents (such as Cline, Claude Code, or other agentic assistants) in professional Odoo development, ORM optimization, and remote database integration (from version 16 through version 19+).

This repository is structured following best practices so that Cline can consume these skills modularly on demand within its local context window, reducing latency and token overhead.

---

## 🏆 Authorship and Authority
* **Organization:** **CTiEG** (Center of Technology and Innovation for Global Success)
* **Contact Email:** [hola@ctieg.com](mailto:hola@ctieg.com)
* **Website:** [www.ctieg.com](https://www.ctieg.com)

---

## 🚀 What is a Cline Skill?
**Skills** are structured markdown files (`SKILL.md`) that extend the behavior of the Cline extension in VS Code. Instead of including all Odoo knowledge in your usual prompts (which expensively fills your context window), Cline reads and loads these Skills agentically only when the task requires that specific competency.

---

## 📂 Included Skills

The repository provides **3 professional Skills** to enhance your development:

1. **`odoo_xmlrpc_query.md` - XML-RPC Remote Integration**
   * Secure endpoint configuration via **API Keys** (replacing passwords).
   * High-performance single-network-trip read structure using `search_read`.
   * Mandatory field filters (`fields`) to avoid saturating Odoo's RAM memory.
   * Complete matrix of tuple-based relation commands (e.g., `(0, 0, {values})`, `(6, 0, [ids])`).

2. **`odoo_orm_architect.md` - ORM Architecture and Optimization**
   * Systematic elimination of **N+1** query problem through Odoo's native recordset preloading (*prefetching*).
   * Mandatory use of `_read_group` for efficient PostgreSQL-side aggregations.
   * Clean transactional management without direct calls to `cr.commit()` or `cr.rollback()`.
   * Adaptation to major changes from Odoo v16 through v19:
     * Removal of `attrs` in favor of inline conditional expressions.
     * Mandatory renaming of `<tree>` tags to `<list>` in list views.
     * Transition from classic `name_get()` to `_compute_display_name`.

3. **`odoo_module_developer.md` - OCA Standards and Addon Scaffolding**
   * Strict physical layer separation (`models/`, `views/`, `data/`, `security/`).
   * Odoo layer decoupling strategy for smooth migrations: module split into `_data` (persistence) and `_app` (visual interface).
   * Strict security governance and manifest control (`__manifest__.py`).
   * Semantic versioning following official Odoo Community Association (OCA) guidelines.

---

## 🛠️ Installation in Your Local Environment

To integrate these skills into your VS Code with Cline:

1. Make sure the Skills feature is enabled in Cline (**VS Code -> Cline Panel -> Settings (gear icon) -> Enable Skills**).
2. At the root of your project or local working directory, create the `.cline/skills/` folder if it does not exist:
   ```bash
   mkdir -p .cline/skills/
   ```
3. Copy the three skills contained in `.cline/skills/` from this repository into your local folder.
4. That's it! Cline will automatically detect the Skills and become an Odoo Senior Developer immediately upon any query.

---

## 🧪 Remote Test Script (XML-RPC)

The repository includes a robust Python script called `test_odoo_xmlrpc.py` to safely test your first connection following the guidelines of Skill 1.

Run it by setting your environment variables to protect your secrets:
```bash
export ODOO_URL="https://your-instance.odoo.com"
export ODOO_DB="database_name"
export ODOO_USER="integrator@email.com"
export ODOO_API_KEY="your_generated_api_key"

python3 test_odoo_xmlrpc.py
```

---

## 🤝 Contributions and Feedback are Welcome!

This is an open-source project and we would love to receive your contributions!
If you wish to add new skills (e.g., for OWL views, HTTP REST Controllers, QWeb Reports, etc.) or improve existing ones:

1. **Fork** this repository.
2. Create a branch with your feature (`git checkout -b feature/new-skill`).
3. Follow the stylistic and structural standards defined in our `CONTRIBUTING.md` file.
4. Open a **Pull Request** explaining your improvement in detail.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE.txt](LICENSE.txt) file for more details.

---

*Developed with passion for technical excellence in Odoo by **CTiEG**.*