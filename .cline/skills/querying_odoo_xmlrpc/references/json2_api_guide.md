# Odoo 19 External JSON-2 API Guide

Introduced in Odoo 19.0, the **JSON-2 HTTP API** replaces traditional XML-RPC/JSON-RPC protocols, which are officially scheduled for **complete removal in Odoo 22 (Fall 2028)**.

## Protocol Architecture

The JSON-2 API uses standard JSON over HTTP POST, targeted directly at the `/json/2/<model>/<method>` URL.

### HTTP Headers
* `Host`: The hostname of the Odoo server.
* `Authorization`: `bearer <API_KEY>` (Replaces password login completely).
* `Content-Type`: `application/json`
* `X-Odoo-Database`: The target database name (mandatory on multi-database servers).

### Request Payload Shape
The POST body must be a single JSON object containing:
* `ids`: An array of integer record IDs to execute the method on. Omit or pass empty for `@api.model` decorated methods.
* `context`: (Optional) An object representing dictionary overrides (e.g. `{"lang": "en_US"}`).
* Method parameters as named JSON keys (positional arguments are not supported in JSON-2).

## Programmatic API Key Management

For automated deployments, Odoo 19 allows programmatic generation and rotation of keys under the models:
* `res.users.apikeys.generate(key, scope, name, expiration_date)`
* `res.users.apikeys.revoke(key)`

## Key Rotation Best Practices
1. Generate the new key using the valid existing key.
2. Store the new key securely in the target environment.
3. Verify that the client can communicate with the new key.
4. Revoke the previous key immediately after validation.\n