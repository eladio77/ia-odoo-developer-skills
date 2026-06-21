# Odoo XML-RPC & JSON-RPC Traditional API Guide

Odoo traditionally exposes its Models API over XML-RPC and JSON-RPC, enabling external clients to perform CRUD operations on database models.

## Endpoints

Odoo traditional RPC uses two main HTTP POST endpoints:
1. `/xmlrpc/2/common`: Handling non-authenticated requests (such as server version metadata and logins).
2. `/xmlrpc/2/object`: Handling model-level queries and executing transactional Python methods via `execute_kw`.

## Core Methods Mapped in execute_kw

1. **check_access_rights**: Validates if the user UID holds necessary access rights (`read`, `write`, `create`, `unlink`) for the given model.
2. **search**: Filters database identifiers (IDs) matching a domain logic.
3. **search_count**: Counts matching records without retrieving them.
4. **read**: Fetches field values for a specific list of record IDs.
5. **search_read**: Optimizes queries by performing a combined search and read in a single SQL execution transaction.
6. **create**: Persists a new record. Accepts a dictionary of values.
7. **write**: Modifies existing records in bulk. Accepts a list of IDs and a dictionary of updated values.
8. **unlink**: Deletes records by ID.

## Performance Optimization

* **Network Latency**: Never use separate `search` and `read` queries in succession; use `search_read` to save network round trips.
* **Memory Limits**: Never call `read` without a `fields` filter. Loading computed fields across hundreds of records in memory can trigger Odoo server out-of-memory crashes.\n