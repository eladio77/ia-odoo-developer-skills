#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
"""

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
        print("\n    Example:")
        print("    export ODOO_URL=\"https://mycompany.odoo.com\"")
        print("    export ODOO_DB=\"mycompany_db\"")
        print("    export ODOO_USER=\"integrator@mycompany.com\"")
        print("    export ODOO_API_KEY=\"your_generated_user_api_key\"")
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
        
        print(f"[✓] Successfully retrieved {len(records)} active company records:\n")
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
    run_integration_test()\n