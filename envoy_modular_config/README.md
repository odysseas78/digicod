# Modular Envoy Configuration

Diese Vorlage teilt die Envoy-Konfiguration in gemeinsame Listener/Cluster und je eine Domain-Datei auf. Der Builder erzeugt daraus `digicod_eu.yaml` und zusaetzlich `generated/envoy.yaml`.

## Struktur

```text
envoy_modular_config/
├── envoy-parts/
│   ├── admin/admin.yaml
│   ├── listeners/http_redirect_listener.yaml
│   ├── listeners/https_listener.yaml
│   ├── domains/digicod_eu.yaml
│   ├── domains/gunicorn_subdomains_digicod_eu.yaml
│   ├── domains/local_digicod_eu.yaml
│   └── clusters/upstreams.yaml
├── generated/
│   └── envoy.yaml
├── digicod_eu.yaml
└── scripts/
    ├── build_envoy.py
    └── validate_envoy.sh
```

## Domains

Die Domain-Dateien sind die normalen Bearbeitungspunkte:

- `domains/digicod_eu.yaml`: `digicod.eu` -> `service_cluster`
- `domains/gunicorn_subdomains_digicod_eu.yaml`: `api.digicod.eu`, `shop.digicod.eu` -> `gunicorn_cluster`
- `domains/local_digicod_eu.yaml`: `local.digicod.eu` -> `gunicorn_cluster`, nur fuer `10.0.0.0/24` und `127.0.0.1`

Der Backend-Service sieht damit die Subdomain-Pfade direkt ab `/`. Beispiel: `https://api.digicod.eu/products` kommt in Django als `/products` an.

Mehrere Subdomains mit gleicher Route koennen in einer Datei stehen:

```yaml
name: gunicorn_subdomains_digicod_eu
order: 20
base_domain: digicod.eu
subdomains:
  - api
  - shop
https_routes:
  - match:
      prefix: /
    route:
      cluster: gunicorn_cluster
```

## Bauen

PowerShell/Windows:

```powershell
python .\scripts\build_envoy.py
```

Alternative:

```powershell
py -3 .\scripts\build_envoy.py
```

Unter Windows kann `python3` auf eine andere Python-Installation zeigen als `python`; wenn PyYAML dort fehlt, bitte `python` oder `py -3` verwenden.

Linux/macOS:

```bash
python scripts/build_envoy.py
```

Der Build schreibt beide Ziel-Dateien:

- `digicod_eu.yaml`
- `generated/envoy.yaml`

## Validieren

```bash
bash scripts/validate_envoy.sh
```

Oder direkt:

```bash
envoy --mode validate -c generated/envoy.yaml
```

## Starten

```bash
envoy -c generated/envoy.yaml
```

## Korrekturen gegenüber der ursprünglichen Datei

1. `request_headers_to_add` mit `%RESPONSE_CODE%` wurde zu `response_headers_to_add` geaendert.
2. Feste IP-Upstreams nutzen jetzt `STATIC` statt `logical_dns`.
3. `front.digicod.eu` und die alten Pfad-Routen wurden durch `digicod.eu` und die Subdomain-Dateien ersetzt.
4. Listener, Domains und Cluster sind getrennt, werden aber final unter `static_resources` zusammengefuehrt.
