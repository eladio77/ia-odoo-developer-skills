# Odoo ORM Prefetching & Performance Guide

The Odoo ORM automatically pre-fetches records of the same prefetch-set (usually the recordset from which a record comes by iteration) to avoid the $N+1$ query problem.

## The N+1 Query Problem Explained

Executing one database query to fetch records, and then running another query *for each record* inside a loop.

### Naive Iteration (101 Queries for 100 records)
```python
# Anti-pattern: rompemos la precarga
for partner_id in partner_ids:
    partner = self.browse(partner_id)
    print(partner.name) # Una consulta SQL por cada registro
```

### Prefetched Iteration (1 Query)
```python
# Odoo loads the names of all partners in the prefetch set at once
partners = self.browse(partner_ids)
for partner in partners:
    print(partner.name) # Una sola consulta SQL para todo el lote
```

## Disabling Prefetching
If you must isolate a specific record and prevent it from fetching sibling values in bulk, use `with_prefetch()`:
```python
isolated_record = record.with_prefetch(False)
```

## read_group vs _read_group
* **`read_group()`**: Deprecated in Odoo 18.0.
* **`_read_group(domain, groupby, aggregates)`**: The official, high-performance Odoo 19 query aggregation method.\n