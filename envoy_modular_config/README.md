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
│   ├── domains/api_digicod_eu.yaml
│   ├── domains/rest_digicod_eu.yaml
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
- `domains/api_digicod_eu.yaml`: `api.digicod.eu` -> `gunicorn_cluster`, mit `prefix_rewrite: /api/`
- `domains/rest_digicod_eu.yaml`: `rest.digicod.eu` -> `gunicorn_cluster`, mit `prefix_rewrite: /rest/`

Wenn der Backend-Service die Pfade ohne `/api/` oder `/rest/` erwartet, entferne in der jeweiligen Domain-Datei nur `prefix_rewrite`.

## Bauen

```bash
python3 scripts/build_envoy.py
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
3. `front.digicod.eu` und die alten Pfad-Routen wurden durch `digicod.eu`, `api.digicod.eu` und `rest.digicod.eu` ersetzt.
4. Listener, Domains und Cluster sind getrennt, werden aber final unter `static_resources` zusammengefuehrt.
