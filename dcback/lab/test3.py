import base64
import secrets
import sys, os, subprocess
from pathlib import Path
sys.path.insert(0, '/home/dcback')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from dataclasses import dataclass
# os.system('export PYTHONPATH=/home/ws/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.11/bin/python:$PWD')
# os.environ['PYTHONPATH'] = '/home/ws/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.11/bin/python:/home/dcback'
from pprint import pprint
# print(os.environ)
from django.db.models import Count, Sum, Max, Min, Avg, Q
# os.environ['PYTHONPATH'] = '/home/user/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.10/bin/python:'+os.environ['PWD']

# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# django.setup()
# from eshop.payment.paymentwall.base import PW
from eshop.models import Basket, Brand
from pprint import pprint
import getpass, imaplib
import requests
from decimal import Decimal
from datetime import datetime, timedelta
# from eshop.hc_vault.vault_client import vault_Client
from difflib import SequenceMatcher


def string_similarity(str1, str2):
    """
    Berechnet die Ähnlichkeit zwischen zwei Strings (0.0 bis 1.0).
    Gibt einen Wert zwischen 0 (keine Ähnlichkeit) und 1 (identisch) zurück.
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def are_strings_similar(str1, str2, threshold=0.9):
    """
    Prüft, ob zwei Strings ähnlich sind (Standard: 90% Ähnlichkeit).
    
    Args:
        str1: Erster String
        str2: Zweiter String
        threshold: Schwellenwert für Ähnlichkeit (0.0 bis 1.0), Standard: 0.9 (90%)
    
    Returns:
        bool: True wenn ähnlich, False wenn nicht
    """
    similarity = string_similarity(str1, str2)
    return similarity >= threshold


def get_all_files_recursive(directory_path):
    """Gibt alle Dateien rekursiv zurück"""
    directory = Path(directory_path)
    files = list(directory.rglob('*'))
    files = [f for f in files if f.is_file()]
    return files

# ============================================
# Django QuerySet filter() Beispiele:
# ============================================
def filter_examples():
    # 1. Einfacher Filter (exakte Übereinstimmung)
    bqs = Brand.objects.filter(wsaler='Prepaidforge')
    bqs = Brand.objects.filter(active=True)
    bqs = Brand.objects.filter(in_stock=True, active=True)  # UND-Verknüpfung

    # 2. Filter mit Lookups (Field Lookups)
    bqs = Brand.objects.filter(title__icontains='Nintendo')  # Case-insensitive Contains
    bqs = Brand.objects.filter(title__startswith='Nintendo')  # Beginnt mit
    bqs = Brand.objects.filter(title__endswith='EU')  # Endet mit
    bqs = Brand.objects.filter(title__iexact='nintendo switch')  # Case-insensitive exakt
    bqs = Brand.objects.filter(created_at__year=2024)  # Jahr
    bqs = Brand.objects.filter(created_at__gte=datetime(2024, 1, 1))  # Größer oder gleich

    # 3. Filter mit Q-Objekten (komplexe Bedingungen)
    # OR-Verknüpfung
    bqs = Brand.objects.filter(Q(wsaler='Prepaidforge') | Q(wsaler='Other'))
    # AND-Verknüpfung
    bqs = Brand.objects.filter(Q(active=True) & Q(in_stock=True))
    # NOT-Verknüpfung
    bqs = Brand.objects.filter(~Q(deleted=True))  # Nicht gelöscht
    # Kombination
    bqs = Brand.objects.filter(
        Q(active=True) & Q(in_stock=True) | Q(wsaler='Prepaidforge')
    )

    # 4. Filter mit exclude() (ausschließen)
    bqs = Brand.objects.exclude(deleted=True)
    bqs = Brand.objects.exclude(active=False)

    # 5. Filter mit chaining (mehrere Filter hintereinander)
    bqs = Brand.objects.filter(wsaler='Prepaidforge').filter(active=True)
    # oder
    bqs = Brand.objects.filter(wsaler='Prepaidforge', active=True)  # Gleiche Wirkung

    # 6. Filter mit Aggregation
    brand_count = Brand.objects.filter(wsaler='Prepaidforge').aggregate(Count('id'))

    # 7. Filter mit distinct() (eindeutige Werte)
    bqs = Brand.objects.filter(wsaler='Prepaidforge').distinct()

    # 8. Filter mit order_by() (Sortierung)
    bqs = Brand.objects.filter(wsaler='Prepaidforge').order_by('title')
    bqs = Brand.objects.filter(wsaler='Prepaidforge').order_by('-created_at')  # Absteigend

    # 9. Filter mit values() oder values_list() (nur bestimmte Felder)
    bqs = Brand.objects.filter(wsaler='Prepaidforge').values('title', 'slug')
    bqs = Brand.objects.filter(wsaler='Prepaidforge').values_list('title', flat=True)

    # 10. Filter mit exists() (prüft ob Einträge existieren)
    exists = Brand.objects.filter(wsaler='Prepaidforge', active=True).exists()

    # ============================================
    # Verwendung mit Dateien und String-Ähnlichkeit
    # ============================================

    directory = Path('cdnx/media/brands')
    files = get_all_files_recursive(directory)

    # Brands filtern
    bqs = Brand.objects.filter(wsaler='Prepaidforge', active=True, deleted=False)
    bqs = Basket.objects.filter(in_order=False)
    print(bqs)
    print(bqs.count())
    bqs.delete()

bqs = Brand.objects.filter(active=True).values_list('title', flat=True)
print(bqs)
