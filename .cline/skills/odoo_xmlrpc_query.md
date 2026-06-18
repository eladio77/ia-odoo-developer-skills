# Skill: Odoo Remote API Integration Engine (XML-RPC & JSON-2)

This Skill equips the Cline agent with advanced engineering patterns, secure transaction strategies, and code templates to connect, query, and modify Odoo instances remotely (v14.0 to v19.0+) using XML-RPC and the new Odoo 19 External JSON-2 API.

---

## ⚠️ Critical Deprecation Warning (Odoo 19 to Odoo 22)
* **API Deprecation:** Traditional XML-RPC and JSON-RPC endpoints (`/xmlrpc`, `/xmlrpc/2`, `/jsonrpc`) are officially **scheduled for complete removal in Odoo 22 (Fall 2028)** [335, 356].
* **The Standard Successor:** The **External JSON-2 API** (accessed via the `/json/2/<model>/<method>` endpoint) is the modern replacement [319, 320]. 
* **Guidelines:** For all new remote integrations in Odoo 19+, prioritize the JSON-2 API. Use XML-RPC only for legacy compatibility.

---

## 🔒 Security & Authentication Architecture
* **Forbidden Pattern:** Never hardcode passwords or store usernames directly in source code.
* **API Keys:** Odoo supports 160-bit random API keys [323, 324]. Use these in place of passwords [258, 360]. API keys cannot be used to log in via the UI but grant identical permissions to the user account [258, 360].
* **Least Privilege:** Always create a dedicated integration user (e.g., "API Bot") with narrow, specific access rights and an empty login password (to block UI logins) instead of using the main Administrator account [330].
* **Programmatic Key Rotation:** Use Odoo 19's programmatic key management methods:
  * `res.users.apikeys.generate(key, scope, name, expiration_date)`: Generates a scoped key programmatically [325, 327].
  * `res.users.apikeys.revoke(key)`: Revokes the specified key immediately [327, 328].
  * **Best Practice:** Authenticate with a newly generated key first, then revoke the previous key to complete a zero-downtime rotation [328, 329].

---

## ⚡ Performance Optimization & Memory Care
* **Avoid N+1 Queries Remotely:** Never call `search()` to get a list of IDs and then run `read()` on them in a loop [728, 838]. This generates multiple network round trips and hits database query limits.
* **The search_read Shortcut:** Use `search_read()` to perform search and retrieval in a single database transaction and network round-trip [333, 911, 920].
* **Mandatory Field Filtering:** Never call `read()` or `search_read()` without passing an explicit `fields` list of strings [265, 296, 728]. Omitting `fields` forces the Odoo server to calculate and return *every* field on the model, including heavy non-stored computed fields, causing high server CPU load and latency [491, 529, 728, 837].

---

## 📦 Transaction Isolation & State Safety
* **Isolated Transactions:** Each remote request to the JSON-2 or XML-RPC endpoints runs in its own SQL transaction [332]. It is impossible to chain multiple independent RPC calls inside a single transaction [332].
* **Race Conditions:** Making sequential queries can cause race conditions (e.g., checking inventory and then reserving it) since concurrent database transactions can alter data in between [332].
* **The Fix:** If a workflow requires multi-step consistency, call a single server-side method decorated with `@api.model` or `@api.private` that executes all sub-steps atomically inside Odoo, rather than executing them step-by-step from the external script [332, 333].

---

## 🧱 The x2many Command Tuple Protocol
Relational fields (`One2many` and `Many2many`) cannot be written to with a simple list of IDs [695, 724]. They require a strict list of 3-element command tuples `(code, record_id, values)` [522, 695]:

| Code | Python Function | Tuple Format | Description |
| :--- | :--- | :--- | :--- |
| **0** | `Command.create(values)` | `(0, 0, {values})` | Creates a new record in the comodel and links it [524, 724]. |
| **1** | `Command.update(id, values)`| `(1, id, {values})` | Writes values directly onto an already linked comodel record [525, 724]. |
| **2** | `Command.delete(id)` | `(2, id, 0)` | Deletes the comodel record entirely and removes the link [525, 724]. |
| **3** | `Command.unlink(id)` | `(3, id, 0)` | Removes the link but does not delete the comodel record [525, 526, 724]. |
| **4** | `Command.link(id)` | `(4, id, 0)` | Links an existing comodel record to the parent [526, 724]. |
| **5** | `Command.clear()` | `(5, 0, 0)` | Removes all links from the relation (deletes nothing) [526, 527, 724]. |
| **6** | `Command.set(ids)` | `(6, 0, [ids])` | Replaces the entire relation set with the provided list of IDs [527, 724]. |

---

## 💻 Standard Integration Blueprints

### 1. Modern JSON-2 REST Client (Odoo 19 Standard)
```python
import os
import requests
import json

def odoo_json2_call(model, method, params=None, ids=None, context=None):
    """
    Executes a high-performance HTTP POST request using Odoo 19 JSON-2 API.
    """
    url = os.getenv("ODOO_URL").rstrip('/')
    db = os.getenv("ODOO_DB")
    api_key = os.getenv("ODOO_API_KEY")

    endpoint = f"{url}/json/2/{model}/{method}"
    
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json",
        "X-Odoo-Database": db,
        "User-Agent": "CTiEG-IntegrationClient/1.0"
    }

    # Construct the JSON-2 request body
    body = {}
    if ids is not None:
        body["ids"] = ids
    if context is not None:
        body["context"] = context
    if params is not None:
        body.update(params)

    try:
        response = requests.post(endpoint, headers=headers, json=body, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"[Error] HTTP Status: {response.status_code}")
        print(f"[Error] Response Body: {response.text}")
        raise err

# Example usage for search_read
partner_data = odoo_json2_call(
    model="res.partner",
    method="search_read",
    params={
        "domain": [["is_company", "=", True], ["customer_rank", ">", 0]],
        "fields": ["name", "email", "phone"],
        "limit": 10,
        "order": "name asc"
    }
)
```

### 2. Legacy XML-RPC Client (v14.0 to v19.0)
```python
import os
import xmlrpc.client

def run_legacy_xmlrpc():
    url = os.getenv("ODOO_URL").rstrip('/')
    db = os.getenv("ODOO_DB")
    user = os.getenv("ODOO_USER")
    api_key = os.getenv("ODOO_API_KEY")

    # Connect to the unauthenticated meta-service endpoint
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, user, api_key, {})
    
    if not uid:
        raise PermissionError("Authentication failed.")

    # Connect to the transactional object service endpoint
    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
    
    # search_read combines queries and avoids keeping IDs in memory
    results = models.execute_kw(
        db, uid, api_key,
        "sale.order",
        "search_read",
        [[("state", "=", "sale")]],
        {
            "fields": ["name", "date_order", "amount_total", "partner_id"],
            "limit": 5,
            "order": "date_order desc"
        }
    )
    return results
```
