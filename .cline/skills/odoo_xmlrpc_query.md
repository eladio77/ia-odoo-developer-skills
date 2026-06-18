# Skill: Odoo XML-RPC Remote Query and Integration Engine

This Skill empowers the Cline agent with architectural guidelines, development patterns, and essential security measures for establishing connections, executing queries, and performing transactions on Odoo instances (v14.0 to v19.0) using the standard XML-RPC protocol.

## Architecture and Security Guidelines

0. **Clean and Concise Code**:
   - Do not generate unnecessary comments in the generated code. Code should be self-explanatory.
   - Prioritize clarity through descriptive variable and function names, not through comments.
   - Be concise: generate only the essential code needed to solve the task, without redundant explanations.
   - Comments are only allowed to document complex, non-obvious business logic that cannot be expressed with descriptive names.

1. **Credential Governance and Security**:
   - **Hard-code Prohibition**: Never embed API keys, passwords, or user data directly in scripts.
   - **Environment Variables**: Require and read access data from the environment using `os.environ` (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_API_KEY`).
   - **API Keys Usage (Odoo v14.0+)**: Fully replace the traditional user password with API keys generated from the Odoo user profile for automated transactions, ensuring they inherit only the strict permissions of the user.

2. **Query Performance Guarantee**:
   - **Restricted Read (Anti-mass-loading pattern)**: When calling `read` or `search_read`, it is **mandatory** to specify a `fields` parameter in the keyword arguments. Omitting this parameter forces Odoo to instantiate all model fields, including expensive computed fields, causing server memory saturation.
   - **search_read over search + read**: Always prefer using the consolidated `search_read` function to obtain filtered records with their values in a single network round trip. Using `search` followed by `read` separately doubles network requests and degrades latency.
   - **Mandatory Pagination**: Do not perform open-ended queries. Segment data loads using explicit pagination parameters (`limit`, `offset`, `order`).

---

## Relational Commands Protocol (x2many Fields)

To modify `One2many` and `Many2many` relation fields through the external API, Odoo requires a structured list of tuples. Each internal command consists of 3 elements: `(code, id/0, values/ids)`.

| Tuple Structure | Operation | Behavior Description |
| :--- | :--- | :--- |
| `(0, 0, {values})` | **Create & Link** | Creates a new secondary record with the values dictionary and links it to the parent. |
| `(1, id, {values})` | **Update Linked** | Updates the specified secondary record by its `id` with the new values. |
| `(2, id, 0)` | **Delete & Unlink** | Physically deletes the record from the database and removes its association. |
| `(3, id, 0)` | **Unlink Only** | Removes the relationship/link without destroying the secondary record from the database. |
| `(4, id, 0)` | **Link Existing** | Links an already existing record in the database (by its `id`) to the parent. |
| `(5, 0, 0)` | **Clear All Links** | Unlinks all existing relationships without deleting the secondary records. |
| `(6, 0, [ids])` | **Replace Set** | Replaces the entire set of existing relationships with the specified list of IDs. |

---

## Code Scaffolding (Standard Python)

Always use Python's native `xmlrpc.client` library, which requires no third-party dependencies.

### 1. Authentication and Connection (UID Retrieval)
```python
import os
import xmlrpc.client

def get_odoo_connection():
    url = os.environ.get("ODOO_URL")
    db = os.environ.get("ODOO_DB")
    username = os.environ.get("ODOO_USER")
    api_key = os.environ.get("ODOO_API_KEY")

    if not all([url, db, username, api_key]):
        raise ValueError("Missing environment variables for Odoo connection.")

    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, api_key, {})
    if not uid:
        raise xmlrpc.client.Fault(401, "Authentication denied: Invalid credentials.")

    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    return db, api_key, uid, models
```

### 2. Efficient Query with Pagination and Field Filters (search_read)
```python
def fetch_salesperson_customers(salesperson_id, limit=50, offset=0):
    db, api_key, uid, models = get_odoo_connection()

    model_name = "res.partner"
    domain = [
        ("user_id", "=", salesperson_id),
        ("active", "=", True),
        ("is_company", "=", True)
    ]

    kwargs = {
        "fields": ["id", "name", "email", "phone", "company_id"],
        "limit": limit,
        "offset": offset,
        "order": "name asc"
    }

    customers = models.execute_kw(
        db, uid, api_key, model_name, "search_read", [domain], kwargs
    )
    return customers
```

### 3. Advanced Record Creation with x2many Commands
```python
def create_sale_order_with_lines(partner_id, product_id, quantity, price_unit):
    db, api_key, uid, models = get_odoo_connection()

    model_name = "sale.order"

    order_vals = {
        "partner_id": partner_id,
        "date_order": xmlrpc.client.DateTime().value,
        "order_line": [
            (0, 0, {
                "product_id": product_id,
                "product_uom_qty": quantity,
                "price_unit": price_unit,
                "name": "Automated sale line"
            })
        ]
    }

    order_id = models.execute_kw(
        db, uid, api_key, model_name, "create", [order_vals]
    )
    return order_id
```

---

## Error Handling and Diagnostics Protocol

- **xmlrpc.client.Fault**: Catch this exception type as a priority. In case of business logic failures or access permission errors in Odoo, the external API will return a structured error containing the Odoo Python traceback.
- **Endpoint Validation**: For generalized network errors (e.g., socket timeouts), ensure the URL does not end with redundant slashes and that the port is correct.
- **Transaction Limitations**: Remember that through XML-RPC, each call via `execute_kw` executes within its own implicit transaction. If you need to execute multiple complex insertions that must fail or apply atomically in bulk, you must structure an intermediate controller on the Odoo server side (customized HTTP Controller or Web Service) to avoid overloading the client channel with sequential calls.