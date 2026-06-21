# OCA Python Coding Standards

All custom code must follow PEP8 guidelines and the Odoo Community Association guidelines.

## 1. Import Ordering

Import statements must be ordered alphabetically within three strict groups:
1. Standard / External libraries (one per line, e.g. `import os`, `import logging`).
2. Odoo core submodules (e.g. `from odoo import models, fields, api, _`).
3. Odoo third-party addons (rare, only if absolutely necessary).

```python
# GOOD
import logging
import os

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
```

## 2. Odoo Idiomatic Code

* **Recordsets operations**: Always favor recordset helpers (`filtered()`, `mapped()`, `sorted()`) over writing Python loops wherever possible.
* **Context propagation**: Never overwrite `self.env.context` as a standard dictionary. Use `with_context()` to pass dynamic overrides safely without side effects:
  `records.with_context(mail_notrack=True).write({'state': 'done'})`\n