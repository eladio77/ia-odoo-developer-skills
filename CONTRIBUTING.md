# Contribution Guide for Odoo Cline Skills

Thank you for your interest in contributing to the Odoo Skills library for Cline! This project is led and maintained by **CTiEG** (hola@ctieg.com | [www.ctieg.com](https://www.ctieg.com)). We deeply value community contributions to make this the most robust artificial intelligence resource for Odoo developers.

By contributing, you help the AI write cleaner, safer, more efficient Odoo code aligned with the core Odoo and **OCA (Odoo Community Association)** standards.

---

## 📜 Golden Rules for Skills

Any new skill or modification to existing ones must comply with the following requirements:

1. **Grounding Guarantee**: Every instruction or code pattern must be rigorously backed by official Odoo documentation or widely recognized community best practices.
2. **Modularity**: Design the guidelines so that the AI acts on demand. Do not saturate skill files with generic Python explanations. Focus on Odoo logic.
3. **Multi-Version**: Make sure to clearly indicate whether a code pattern applies or changes between versions (e.g., specify what works in v16, what changed in v17, and what is mandatory for v18 and v19+).
4. **Security and Performance First**: Every Skill must actively educate the agent to write code that avoids security flaws (e.g., SQL injections, unwanted privilege escalation with `sudo()`) and database bottlenecks (e.g., loops with single write operations, missing prefetching, or N+1 problems).

---

## 📥 Contribution Process

1. **Fork the Repository**: Create a copy of this repository in your GitHub account.
2. **Create a Branch**: Name your branch descriptively:
   * For new skills: `feature/skill-name`
   * For fixes or improvements: `fix/improvement-name`
3. **Write and Validate**:
   * Make sure Skills are saved in Markdown format (`.md`) inside `.cline/skills/`.
   * If you add Python examples, ensure they are syntactically correct under Python 3.10+ and compatible with the Odoo ORM.
4. **Submit a Pull Request (PR)**:
   * Describe the motivation for the change in detail.
   * Provide a use case or example of how Cline successfully uses the new skill.
   * The technical team at **CTiEG** will review the proposal as soon as possible.

---

## 📐 Suggested Structure for New Skills

Each Skill `.md` file should be structured using the following template:
```markdown
# Skill: [Short and Descriptive Competency Name]

[Brief description of what technical ability this file grants to the Cline agent]

## Architectural Guidelines
*   **[Key Design Rule]**: [Design or security instruction]
*   **[Performance Rule]**: [Optimization instruction]

## Reference Code / Syntax
... Clean, commented code examples ready to be imitated by the AI ...

## Version Constraints
*   **Odoo [Version]**: [Details of critical version-specific changes]
```

---

We look forward to your Pull Request! If you have any questions, you can write to us directly at [hola@ctieg.com](mailto:hola@ctieg.com).