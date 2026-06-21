# Contributing to Odoo Cline Skills

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

Thank you for helping us shape the future of agentic Odoo development!\n