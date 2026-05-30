alias wg1="echo 'deb http://deb.debian.org/debian buster-backports main' >> /etc/apt/sources.list"
alias wg2="sudo apt install linux-image-amd64 && sudo apt update"
alias wg3="sudo apt install wireguard-dkms wireguard-tools"
 
alias wg4="sudo modprobe wireguard && lsmod | grep wireguard"
alias wg5="sudo apt install resolvconf"
alias wg6="/sbin/modinfo wireguard"

alias wg7="mkdir /etc/wireguard/ && chmod 700 /etc/wireguard/ && cd /etc/wireguard/ && wg genkey | tee vpn-server-private.key | wg pubkey > vpn-server-public.key &&\
wg genkey | tee vpn-client-private.key | wg pubkey > vpn-client-public.key"

alias wg8="cat > /etc/wireguard/server.conf << EOF
# define the  !WireGuard service
[Interface]
# contents of file vpn-server-private.key
PrivateKey = sAOAM1JZtpDx2CdiVvvGZ33XOLwqTlaEo7flozdy71k=
# UDP service port
ListenPort = 55820
EOF"

alias wg9="ip route ls default"

alias wg10="cat > /etc/network/interfaces.d/wg0 << EOF
# activate on boot
auto wg0
# interface configuration
iface wg0 inet static
    address 10.0.2.1/24
    pre-up ip link add wg0 type wireguard
    pre-up wg setconf wg0 /etc/wireguard/server.conf
    # route packages when the VPN interface is up
    post-up sysctl --write net.ipv4.ip_forward=1

    # and stop routing when stopping the VPN interface
    post-down sysctl --write net.ipv4.ip_forward=0
    post-down ip link del wg0

iface wg0 inet6 static
    address fc00:23:5::1/64
    # route packages when the VPN interface is up
    post-up sysctl --write net.ipv6.conf.all.forwarding=1
    # and stop routing when stopping the VPN interface
    post-down sysctl --write net.ipv6.conf.all.forwarding=0
EOF"

alias wg11="cat > /etc/wireguard/wg0.conf << EOF
[Interface]
# Put here the content of vpn-client-private.key
PrivateKey = +L4WsHUTCbQHnxv2yUf+tU5Mbe0Iv/7+63q+uddLklQ=
Address = 10.0.2.5/32, fc00:23:5::2/64
DNS = 8.8.8.8

[Peer]
# Put here the content of vpn-server-public.key created on the server
PublicKey = 8Kt8x8+PfNbhyAk7CdUEFdM8YLld2jRDL9T1kjl5+EM=
Endpoint = 185.216.176.104:55820
EOF"

alias wg12="cat >> /etc/wireguard/server.conf << EOF
[Peer]
# Put here the content of vpn-client-public.key
PublicKey = JnaOoE6E8LhbJ2hsBSDMYrmbiCH1MpESwjGo/2kEOHc=
AllowedIPs = 10.0.2.5/32
EOF"

alias wg13="wg-quick up wg0"

alias wg14="cat >> /etc/nftables.conf << EOF

add table wireguard-nat

table ip wireguard-nat {
        chain prerouting {
                type nat hook prerouting priority -100; policy accept;
        }

        chain postrouting {
                type nat hook postrouting priority 100; policy accept;
                oifname 'ens33' masquerade
        }
}
EOF"

alias wg15="sudo systemctl enable --now nftables"

alias wg16="cat >> /etc/wireguard/wg0.conf << EOF
AllowedIPs = 0.0.0.0/0, ::/0
EOF"

wg-quick down wg0
wg-quick up wg0
systemctl status wg-quick@server.service
curl ipinfo.io


tcpdump
dig
bind9
dnsmasq
socat TCP4-LISTEN:8080 STDOUT