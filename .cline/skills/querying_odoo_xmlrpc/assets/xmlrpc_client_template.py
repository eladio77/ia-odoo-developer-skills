#!/usr/bin/env python3
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
    
    return models.execute_kw(db, uid, api_key, "res.partner", "search_read", [domain], kwargs)\n