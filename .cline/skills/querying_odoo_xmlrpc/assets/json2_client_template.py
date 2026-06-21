#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests

def odoo_json2_request(model, method, ids=None, context=None, **params):
    url = os.environ.get("ODOO_URL")
    db = os.environ.get("ODOO_DB")
    api_key = os.environ.get("ODOO_API_KEY")

    if not all([url, db, api_key]):
        raise ValueError("Missing environment variables.")

    endpoint = f"{url}/json/2/{model}/{method}"
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json",
        "X-Odoo-Database": db,
        "User-Agent": "CTiEG-Integrator/1.0"
    }

    payload = {
        "ids": ids or [],
        "context": context or {}
    }
    # Unpack extra kwargs as named parameters
    payload.update(params)

    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()\n