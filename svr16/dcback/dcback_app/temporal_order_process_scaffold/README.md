# Django + Temporal Order/Fulfillment Scaffold

Robuster Bestellprozess für digitale Produkte:

- Supplier-Katalog-Sync
- Warenkorbprüfung gegen lokale Supplier-Daten
- Order-Snapshot
- Temporal Fulfillment Workflow
- idempotente SupplierPurchase Records
- verschlüsselte Code-Speicherung
- retrybarer E-Mail-Versand
- Admin-Review Status für unsichere Supplier-Käufe

Zahlung ist absichtlich nicht implementiert.

## Install

```bash
pip install -r requirements.txt
```

Settings:

```python
INSTALLED_APPS += ["rest_framework", "orders"]

TEMPORAL_ADDRESS = "temporal.loc:7233"
TEMPORAL_TASK_QUEUE_ORDER = "order-fulfillment"

PREPAIDFORGE_BASE_URL = "https://api.prepaidforge.example"  # TODO
PREPAIDFORGE_API_KEY = "..."                               # TODO
PREPAIDFORGE_SANDBOX = True

CODE_ENCRYPTION_KEY = "..."  # Fernet key
DEFAULT_FROM_EMAIL = "shop@example.com"
```

Fernet-Key:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Worker starten

```bash
python manage.py start_order_worker
```

## Hinweis

Die PrepaidForge-Endpunkte im Client sind Platzhalter. Trage dort die echten Pfade und JSON-Felder aus deiner PrepaidForge-Dokumentation ein.
