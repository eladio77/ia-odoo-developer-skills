---
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
* **No XML-RPC transaction pooling**: Making hundreds of separate individual RPC calls inside a Python loop instead of using single, consolidated batch calls.\n