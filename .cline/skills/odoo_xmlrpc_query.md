---
name: querying-odoo-xmlrpc
description: |
  Establishes remote integrations, queries databases, and processes external transactions with Odoo instances (v14.0 to v19.0) using XML-RPC and the new JSON-2 API. Use this skill when the user asks to connect to an external Odoo instance, execute RPC method calls, authenticate with API keys, or perform CRUD operations remotely.
  Do NOT use for writing local Odoo module models, optimizing backend database transactions, or designing web controllers.
version: 4.0.0
license: MIT
allowed-tools:
  - Read
  - Write
  - Bash
metadata:
  author: CTiEG
  email: hola@ctieg.com
  website: www.ctieg.com
---

# Querying Odoo XML-RPC & JSON-2

## When to use
* **External Integrations**: Connecting external applications (e.g., e-commerce platforms like Shopify, CRMs like Salesforce, custom mobile apps, or BI scripts) to an Odoo database.
* **Remote CRUD Operations**: Performing create, read, update, or delete operations on Odoo records remotely over HTTP/HTTPS.
* **Remote Method Invocation**: Triggering specific backend model actions (such as confirming a sales order via `action_confirm`) from external systems.
* **API Key Management**: Integrating systems securely using granular, rotatable Odoo API keys instead of master passwords.

## When NOT to use
* **Local Backend Development**: Writing backend Python classes, view XML files, or overriding default ORM methods inside an Odoo addon.
* **Controller Routing**: Building local HTTP endpoints (`@http.route`) inside a custom Odoo module.
* **Database Direct Access**: Running raw SQL queries directly against PostgreSQL on the Odoo server.

## Workflow
1. **Secure Configuration Setup**: 
   Ensure connection parameters are loaded from safe environment variables (`ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_API_KEY`). Reject hardcoded credentials immediately.
2. **Endpoint Connection & Version Check**:
   Initialize connection to the `/xmlrpc/2/common` endpoint. Check connection validity by querying the server version.
3. **Authentication Handshake**:
   Call the `authenticate` method to log in and obtain the unique User ID (`uid`).
4. **Targeted Data Retrieval (search_read)**:
   When reading records, always use the unified `search_read` method over separate `search` and `read` calls. This optimizes latency by consolidating transactions into a single round-trip.
5. **Enforce Strict Field Filtering**:
   Always pass an explicit `'fields'` parameter within the keyword arguments to prevent memory leaks and performance degradation on the server caused by fetching unneeded computed/relational fields.
6. **Apply Relational Commands (x2many fields)**:
   Use the 3-element tuple structure to modify relational fields (`One2many` and `Many2many`) in a single payload. Refer to the command mapping below:

| Command Tuple | Action | Technical Behavior |
| :--- | :--- | :--- |
| `(0, 0, {values})` | **Create & Link** | Creates a new record in the co-model and links it to the parent. |
| `(1, id, {values})` | **Update Linked** | Updates the linked record matching `id` with the new values. |
| `(2, id, 0)` | **Delete & Unlink** | Deletes the linked record physically from the database and removes the link. |
| `(3, id, 0)` | **Unlink Only** | Removes the relation/link but keeps the linked record in the database. |
| `(4, id, 0)` | **Link Existing** | Links an existing record matching `id` to the parent. |
| `(5, 0, 0)` | **Clear All Links** | Unlinks all records without deleting them. |
| `(6, 0, [ids])` | **Replace Set** | Replaces the entire relation set with the provided list of IDs. |

7. **Handle JSON-2 (Odoo 19+) Transitions**:
   Be aware that traditional XML-RPC/JSON-RPC endpoints are scheduled for deprecation in Odoo 21.1 and complete removal in Odoo 22. For Odoo 19+, prioritize the new **External JSON-2 API (`/json/2/<model>/<method>`)** using bearer token headers.

## Examples

### Example 1: Robust XML-RPC search_read in Python
```python
import os
import xmlrpc.client

def fetch_ready_sales_orders(limit=50):
    url = os.environ.get("ODOO_URL")
    db = os.environ.get("ODOO_DB")
    username = os.environ.get("ODOO_USER")
    api_key = os.environ.get("ODOO_API_KEY")

    if not all([url, db, username, api_key]):
        raise ValueError("Missing environment variables for Odoo connection.")

    try:
        # Step 1: Authenticate on the common endpoint
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, api_key, {})
        if not uid:
            raise xmlrpc.client.Fault(401, "Access Denied: Invalid credentials.")

        # Step 2: Establish connection to object endpoint
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        
        # Step 3: Define safe query domain and field filters
        domain = [('state', '=', 'sale')]
        kwargs = {
            'fields': ['id', 'name', 'partner_id', 'amount_total', 'date_order'],
            'limit': limit,
            'order': 'date_order desc'
        }

        # Step 4: Execute search_read in a single transaction
        orders = models.execute_kw(
            db, uid, api_key, 'sale.order', 'search_read', [domain], kwargs
        )
        return orders

    except xmlrpc.client.Fault as e:
        print(f"Odoo API Error [{e.faultCode}]: {e.faultString}")
        raise
```

### Example 2: Modern JSON-2 API Request (Odoo 19+)
```bash
curl -X POST https://mycompany.odoo.com/json/2/sale.order/search_read \
  -H "Authorization: Bearer my_secure_api_key_string" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": [["state", "=", "sale"]],
    "fields": ["name", "partner_id", "amount_total"],
    "limit": 10
  }'
```

## Output format
Integrations built using this skill must:
* Be structured as isolated, highly reusable Python scripts or modules using exclusively the `xmlrpc.client` standard library or standard HTTP requests for JSON-2.
* Read configurations dynamically using environment variables or configuration files.
* Yield JSON-serializable structures with explicitly declared fields.
* Follow defensive programming styles, including try-except blocks capturing `xmlrpc.client.Fault` or checking HTTP response statuses.

## Anti-patterns to avoid
* **DO NOT** hardcode secrets or master credentials in the script.
* **DO NOT** omit the `'fields'` parameter when requesting data. This forces Odoo to evaluate all fields (including heavy computed metrics), causing performance drops and server-side timeouts.
* **DO NOT** chain `search` followed by `read` sequentially. This doubles the network round-trip overhead. Use `search_read` instead.
* **DO NOT** pass simple Python lists to One2many/Many2many fields. Use the tuple syntax specified in the workflow.
* **DO NOT** assume external RPC calls are safe against network hiccups; always implement timeouts, connection retries, and error parsing.
