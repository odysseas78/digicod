# config/middleware/local_paths_only.py
from ipaddress import ip_address, ip_network
from django.http import HttpResponseForbidden


class LocalOnlyDomainMiddleware:
    """
    Erlaubt local.digicod.eu nur aus bestimmten IP-Netzen.

    Beispiel:
      local.digicod.eu nur aus 10.0.0.0/24

    Wichtig:
      Hinter Envoy muss die echte Client-IP korrekt an Django weitergegeben werden.
    """

    LOCAL_HOSTS = {
        "local.digicod.eu",
    }

    ALLOWED_NETWORKS = [
        ip_network("10.0.0.0/24"),
        ip_network("127.0.0.0/8"),
        ip_network("::1/128"),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        """
        Erst X-Forwarded-For lesen, sonst REMOTE_ADDR.

        Wichtig:
        X-Forwarded-For nur verwenden, wenn dein Envoy der einzige direkte
        Proxy vor Django ist und Clients den Header nicht selbst durchreichen dürfen.
        """
        xff = request.META.get("HTTP_X_FORWARDED_FOR")

        if xff:
            # erste IP = ursprünglicher Client
            return xff.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR", "")

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()

        if host in self.LOCAL_HOSTS:
            raw_ip = self.get_client_ip(request)

            try:
                client_ip = ip_address(raw_ip)
            except ValueError:
                return HttpResponseForbidden("Forbidden: invalid client IP")

            allowed = any(client_ip in network for network in self.ALLOWED_NETWORKS)

            if not allowed:
                return HttpResponseForbidden("Forbidden: local domain only")

        return self.get_response(request)
     
     
     

class LocalOnlyPathsMiddleware:
    PROTECTED_PREFIXES = (
        "/local/",
        "/internal/",
        "/debug/",
    )

    ALLOWED_NETWORKS = [
        ip_network("10.0.0.0/24"),
        ip_network("127.0.0.0/8"),
        ip_network("::1/128"),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def get_client_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            return xff.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")

    def __call__(self, request):
        if request.path.startswith(self.PROTECTED_PREFIXES):
            raw_ip = self.get_client_ip(request)

            try:
                client_ip = ip_address(raw_ip)
            except ValueError:
                return HttpResponseForbidden("Forbidden")

            if not any(client_ip in network for network in self.ALLOWED_NETWORKS):
                return HttpResponseForbidden("Forbidden")

        return self.get_response(request)