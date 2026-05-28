# NetWatcher für LXD + WireGuard

Dieses Tool ist für eine eigene Admin-Umgebung gedacht, z. B. drei LXD-Server, die über WireGuard verbunden sind.

Es macht drei Dinge:

1. Es ermittelt Ziel-IP-Adressen möglichst automatisch aus LXD, WireGuard, Linux-Routen und ARP/Nachbarschaftstabelle.
2. Es scannt nur die konfigurierten TCP-Ports und zeigt in der WebGUI nur aktive Hosts mit offenen Ports.
3. Es verwaltet WireGuard-Peers in der Server-Config: `AllowedIPs` ändern, Peer hinzufügen/löschen, neue Schlüssel generieren.

## Installation

```bash
apt update
apt install -y python3 python3-venv python3-pip wireguard-tools iproute2 lxd-client

unzip netwatcher.zip
cd netwatcher
./install.sh
./run.sh
```

Dann öffnen:

```text
http://SERVER-IP:8080
```

## Wichtige Dateien

```text
config.yml                  Hauptkonfiguration
app.py                      Flask-App, Scanner, WireGuard-Verwaltung
netwatcher.sqlite3          SQLite-Datenbank, wird automatisch erstellt
netwatcher.service          systemd-Service Beispiel
```

## Automatische IP-Ermittlung

Das Tool versucht Quellen zu kombinieren:

- `lxc list` für laufende Container/VMs und deren IPv4-Adressen
- `lxc network list` für LXD-Bridge-Netze wie `lxdbr0`
- WireGuard `Address` und Peer-`AllowedIPs`
- Linux-Routen aus `ip -4 route`
- ARP/Nachbarn aus `ip -4 neigh`
- manuelle Ziele aus `config.yml`

Große Netze werden aus Sicherheitsgründen nicht automatisch vollständig gescannt. Standardlimit im Code: 4096 Adressen pro Netz.

## WireGuard-Verwaltung

Standardpfad:

```text
/etc/wireguard/wg0.conf
```

Vor jeder Änderung legt das Tool ein Backup an:

```text
/etc/wireguard/netwatcher-backups/
```

Standardmäßig wird die Datei nur gespeichert. WireGuard wird **nicht automatisch neu gestartet**.

Wenn du willst, dass Änderungen sofort aktiv werden:

```yaml
wireguard:
  auto_apply: true
  apply_command: "wg-quick down wg0 && wg-quick up wg0"
```

Oder in der UI unter **Einstellungen** aktivieren.

## Beispiel AllowedIPs

Für einzelne VPN-Clients:

```text
10.0.0.2/32
10.0.0.3/32
```

Für einen Peer, der zusätzlich ein LXD-Netz hinter sich erreichbar macht:

```text
10.0.0.4/32, 10.251.167.0/24
```

## systemd Installation

Beispiel nach `/opt/netwatcher` kopieren:

```bash
sudo mkdir -p /opt/netwatcher
sudo cp -a . /opt/netwatcher/
sudo cp /opt/netwatcher/netwatcher.service /etc/systemd/system/netwatcher.service
sudo systemctl daemon-reload
sudo systemctl enable --now netwatcher
```

## Sicherheit

Nicht öffentlich ins Internet stellen. Am besten nur über WireGuard erreichbar machen.

Beispiel mit UFW:

```bash
ufw allow in on wg0 to any port 8080 proto tcp
ufw deny 8080/tcp
```

Oder mit nftables nur `wg0` erlauben.
