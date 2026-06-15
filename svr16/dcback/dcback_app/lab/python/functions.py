
import json



def jaccard_similarity(str1, str2):
    set1, set2 = set(str1.replace(' ','').replace('-','').lower()), set(str2.replace(' ','').replace('-','').lower())
    similarity = len(set1 & set2) / len(set1 | set2)
    return similarity


"list methods list methode"

regs2 = [
    region
    for product in pqs
    for region in json.loads(product.regions)
]

# Ergebnis:

['no', 'se', 'fr', 'be', 'nl', 'it', 'es', 'de', 'fi', 'uk', 'dk']

# Wenn du zusätzlich Duplikate entfernen willst:

regs2 = list({
    region
    for product in pqs
    for region in json.loads(product.regions)
})

# Wenn Reihenfolge erhalten bleiben soll:

regs2 = list(dict.fromkeys(
    region
    for product in pqs
    for region in json.loads(product.regions)
))