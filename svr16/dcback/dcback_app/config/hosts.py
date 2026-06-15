from django.conf import settings
from django_hosts import host, patterns


host_patterns = patterns(
    '',
    # host(r'', settings.ROOT_URLCONF, name='rest'),
    host(r'shop', 'apps.shop.urls', name='shop'),
    host(r'orders', 'apps.orders.urls', name='orders'),
    host(r'accounts', 'apps.account.urls', name='accounts'),
    host(r'api', 'api.urls', name='api'),
    host(r'local', 'config.local_urls', name='local'),
)
