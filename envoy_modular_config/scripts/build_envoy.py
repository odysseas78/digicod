#!/usr/bin/env python3
from __future__ import annotations
import copy
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ModuleNotFoundError as exc:
    if exc.name != "yaml":
        raise
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
ADMIN_FILE = ROOT / "envoy-parts/admin/admin.yaml"
HTTP_LISTENER_FILE = ROOT / "envoy-parts/listeners/http_redirect_listener.yaml"
HTTPS_LISTENER_FILE = ROOT / "envoy-parts/listeners/https_listener.yaml"
HTTP_ROUTE_CONFIG_FILE = ROOT / "envoy-parts/routes/http_redirects.yaml"
HTTPS_ROUTE_CONFIG_FILE = ROOT / "envoy-parts/routes/https_routes.yaml"
DOMAINS_DIR = ROOT / "envoy-parts/domains"
CLUSTERS_FILE = ROOT / "envoy-parts/clusters/upstreams.yaml"
OUTPUT_FILES = (
    ROOT / "digicod_eu.yaml",
    ROOT / "generated/envoy.yaml",
)

ROUTE_INCLUDE_KEY = "__include_route_config__"


def require_pyyaml() -> None:
    if yaml is not None:
        return

    print(
        "\n".join(
            [
                "Missing dependency: PyYAML is not installed for this Python interpreter.",
                f"Interpreter: {sys.executable}",
                "",
                "On this Windows setup, `python3` can point to a different Python than `python`.",
                "Try one of these commands from envoy_modular_config:",
                "  python scripts/build_envoy.py",
                "  py -3 scripts/build_envoy.py",
                "",
                "If you really want to use this interpreter, install PyYAML into it:",
                f"  {sys.executable} -m pip install PyYAML",
            ]
        ),
        file=sys.stderr,
    )
    raise SystemExit(1)


def load_yaml(path: Path) -> dict[str, Any]:
    require_pyyaml()
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(f"YAML root must be mapping in {path}")
    return data


def require_list(value: Any, path: Path, key: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{key} must be a list in {path}")
    return value


def optional_mapping(value: Any, path: Path, key: str) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{key} must be a mapping in {path}")
    return value


def load_route_config(path: Path, virtual_hosts: list[dict[str, Any]]) -> dict[str, Any]:
    data = load_yaml(path)
    route_config = optional_mapping(data.get("route_config"), path, "route_config")
    if route_config is None:
        raise ValueError(f"route_config is required in {path}")

    route_config = copy.deepcopy(route_config)
    route_config["virtual_hosts"] = virtual_hosts
    return route_config


def load_hostnames(data: dict[str, Any], path: Path) -> list[str]:
    hostnames: list[str] = []

    explicit_domains = data.get("domains")
    if explicit_domains is not None:
        domains = require_list(explicit_domains, path, "domains")
        hostnames.extend(domains)

    subdomains = data.get("subdomains")
    if subdomains is not None:
        subdomain_list = require_list(subdomains, path, "subdomains")
        base_domain = data.get("base_domain")
        if not isinstance(base_domain, str) or not base_domain:
            raise TypeError(f"base_domain must be a non-empty string when subdomains is set in {path}")

        for subdomain in subdomain_list:
            if not isinstance(subdomain, str) or not subdomain:
                raise TypeError(f"subdomains must contain non-empty strings in {path}")
            hostnames.append(f"{subdomain}.{base_domain}")

    if not hostnames or not all(isinstance(hostname, str) and hostname for hostname in hostnames):
        raise TypeError(f"domains or subdomains must contain non-empty strings in {path}")

    return hostnames


def load_domains() -> list[dict[str, Any]]:
    domain_files = sorted(DOMAINS_DIR.glob("*.yaml"))
    if not domain_files:
        raise FileNotFoundError(f"No domain config files found in {DOMAINS_DIR}")

    domains: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    seen_domains: dict[str, Path] = {}

    for path in domain_files:
        data = load_yaml(path)

        name = data.get("name")
        if not isinstance(name, str) or not name:
            raise TypeError(f"name must be a non-empty string in {path}")
        if name in seen_names:
            raise ValueError(f"Duplicate domain config name {name!r} in {path}")
        seen_names.add(name)

        hostnames = load_hostnames(data, path)
        for hostname in hostnames:
            if hostname in seen_domains:
                raise ValueError(f"Domain {hostname!r} is configured in both {seen_domains[hostname]} and {path}")
            seen_domains[hostname] = path

        https_routes = require_list(data.get("https_routes"), path, "https_routes")
        if not https_routes:
            raise ValueError(f"At least one HTTPS route is required in {path}")

        http_routes = require_list(data.get("http_routes"), path, "http_routes")
        if not http_routes:
            raise ValueError(f"At least one HTTP route is required in {path}")

        typed_per_filter_config = optional_mapping(data.get("typed_per_filter_config"), path, "typed_per_filter_config")
        http_typed_per_filter_config = optional_mapping(
            data.get("http_typed_per_filter_config", typed_per_filter_config),
            path,
            "http_typed_per_filter_config",
        )
        https_typed_per_filter_config = optional_mapping(
            data.get("https_typed_per_filter_config", typed_per_filter_config),
            path,
            "https_typed_per_filter_config",
        )

        domains.append(
            {
                "name": name,
                "order": data.get("order", 100),
                "domains": hostnames,
                "https_routes": https_routes,
                "http_routes": http_routes,
                "http_typed_per_filter_config": http_typed_per_filter_config,
                "https_typed_per_filter_config": https_typed_per_filter_config,
                "path": path,
            }
        )

    return sorted(domains, key=lambda item: (item["order"], item["path"].name))


def build_virtual_hosts(domains: list[dict[str, Any]], route_key: str) -> list[dict[str, Any]]:
    virtual_hosts: list[dict[str, Any]] = []

    for domain in domains:
        if route_key == "http_routes":
            routes = domain["http_routes"]
            name = f"{domain['name']}_http_redirect"
        else:
            routes = domain["https_routes"]
            name = domain["name"]

        virtual_host = {
            "name": name,
            "domains": copy.deepcopy(domain["domains"]),
            "routes": copy.deepcopy(routes),
        }

        typed_per_filter_config_key = (
            "http_typed_per_filter_config"
            if route_key == "http_routes"
            else "https_typed_per_filter_config"
        )
        typed_per_filter_config = domain.get(typed_per_filter_config_key)
        if typed_per_filter_config is not None:
            virtual_host["typed_per_filter_config"] = copy.deepcopy(typed_per_filter_config)

        virtual_hosts.append(virtual_host)

    return virtual_hosts


def validate_cluster_references(domains: list[dict[str, Any]], clusters: list[dict[str, Any]]) -> None:
    cluster_names = {cluster.get("name") for cluster in clusters if isinstance(cluster, dict)}
    missing: list[str] = []

    for domain in domains:
        for route in domain["https_routes"]:
            if not isinstance(route, dict):
                continue
            route_action = route.get("route")
            if not isinstance(route_action, dict):
                continue
            cluster_name = route_action.get("cluster")
            if isinstance(cluster_name, str) and cluster_name not in cluster_names:
                missing.append(f"{domain['path']}: {cluster_name}")

    if missing:
        raise ValueError("Unknown cluster references:\n" + "\n".join(missing))


def replace_route_includes(
    listener: dict[str, Any],
    route_configs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    include_count = 0

    for chain in listener.get("filter_chains", []):
        for item_filter in chain.get("filters", []):
            typed_config = item_filter.get("typed_config", {})
            if not isinstance(typed_config, dict):
                continue
            current_route_config = typed_config.get("route_config")
            if not isinstance(current_route_config, dict):
                continue
            include_name = current_route_config.get(ROUTE_INCLUDE_KEY)
            if include_name is None:
                continue
            if include_name not in route_configs:
                raise KeyError(f"Unknown route config include {include_name!r}")
            typed_config["route_config"] = copy.deepcopy(route_configs[include_name])
            include_count += 1

    if include_count == 0:
        raise ValueError(f"No route config include found in listener {listener.get('name')!r}")

    return listener


def main() -> None:
    require_pyyaml()

    admin = load_yaml(ADMIN_FILE)
    http_listener = load_yaml(HTTP_LISTENER_FILE)["listener"]
    https_listener = load_yaml(HTTPS_LISTENER_FILE)["listener"]
    clusters = load_yaml(CLUSTERS_FILE)
    cluster_list = require_list(clusters.get("clusters"), CLUSTERS_FILE, "clusters")
    domains = load_domains()

    validate_cluster_references(domains, cluster_list)

    route_configs = {
        HTTP_ROUTE_CONFIG_FILE.stem: load_route_config(
            HTTP_ROUTE_CONFIG_FILE,
            build_virtual_hosts(domains, "http_routes"),
        ),
        HTTPS_ROUTE_CONFIG_FILE.stem: load_route_config(
            HTTPS_ROUTE_CONFIG_FILE,
            build_virtual_hosts(domains, "https_routes"),
        ),
    }

    http_listener = replace_route_includes(http_listener, route_configs)
    https_listener = replace_route_includes(https_listener, route_configs)

    final_config = {
        "admin": admin["admin"],
        "static_resources": {
            "listeners": [http_listener, https_listener],
            "clusters": cluster_list,
        },
    }

    for output_file in OUTPUT_FILES:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open("w", encoding="utf-8") as f:
            yaml.safe_dump(final_config, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
        print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
