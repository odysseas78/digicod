import pycountry
from pprint import pprint

gg = ['dk', 'SG', 'ww', 'uk', 'tw', 'jp', 'lv', 'United Kingdom', 'MY', 'EUW', 'cn', 'no', 'North America', 'AR', 'gr', 'PH', 'it', 'ca', 'emea', 'NZ', 'ie', 'ID', 'ru', 'Other', 'fr', 'in', 'fi', 'sa', 'es', 'de', 'au', 'United States', 'PE', 'VD', 'TH', 'mx', 'ae', 'tr', 'ro', 'pl', 'sk', 'lt', 'Rest of the world', 'hk', 'se', 'cz', 'HU', 'eu', 'ch', 'ZA', 'at', 'pt', 'nl', 'us', 'be', 'br', 'HR', 'CL', 'NA']

# Definieren von Regionen und Sonderfällen
regions = {
    'emea': 'EMEA',
    'eu': 'EU',
    'euw': 'EUW',
    'na': 'NA',
    'north america': 'NA',
    'rest of the world': 'WW',
    'other': 'WW',
    'ww': 'WW',
    'VD':'VN',
}

def standardize_entry(entry):
    entry.replace('[','').replace(']','')
    entry_lower = entry.lower()
    
    # Überprüfen, ob der Eintrag eine definierte Region/Sonderfall ist
    if entry_lower in regions:
        return regions[entry_lower]
    
    # Versuchen, den Eintrag als ISO Alpha-2 Code zu interpretieren
    try:
        country = pycountry.countries.get(alpha_2=entry.upper())
        if country:
            return country.alpha_2
    except:
        pass
    
    # Versuchen, den Eintrag als vollständigen Ländernamen zu interpretieren
    try:
        country = pycountry.countries.lookup(entry)
        return country.alpha_2
    except LookupError:
        pass
    
    # Wenn alles fehlschlägt, den Eintrag als UNKNOWN markieren
    return 'WW'

# Erstellen eines leeren Sets für die standardisierten Einträge

def regionsfn(data):
    
    standardized_set = set()

    for item in data:
        standardized = standardize_entry(item)
        standardized_set.add(standardized)
    return standardized_set

# print("Standardisierte Einträge ohne Duplikate:")
# res = list(regionsfn(data=gg))
# pprint(res)
# pprint(type(res))
# pprint(len(res))
