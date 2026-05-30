
import re

def add_prefix_to_tailwind_classes(html, prefix='tw-'):
    # Regex, um alle Klassen zu finden
    class_pattern = re.compile(r'className="([^"]*)"')

    # Funktion, um die Klassen mit dem Präfix zu versehen
    def add_prefix(match):
        classes = match.group(1)
        prefixed_classes = ' '.join(f'{prefix}{cls}' if not cls.startswith(prefix) else cls for cls in classes.split())
        return f'className="{prefixed_classes}"'

    # Ersetzen der Klassen im HTML-Code
    return class_pattern.sub(add_prefix, html)

# Beispiel-HTML-Code
html_code = '''
<div className="grid grid-cols-12 gap-4">
    <div className="col-span-12 md:col-span-6 lg:col-span-3">Content</div>
    <div className="col-span-12 md:col-span-6 lg:col-span-3"></div>
    <div className="col-span-12 md:col-span-6 lg:col-span-3"></div>
    <div className="col-span-12 md:col-span-6 lg:col-span-3"></div>
</div>
'''


# with open('/home/dcui/src/pages/Homepage/GridList.jsx', 'r') as fr:
#     d = fr.read()

# # Anwendung der Funktion
# prefixed_html = add_prefix_to_tailwind_classes(d)
# with open('/home/dcui/src/pages/Homepage/GridList.jsx', 'w') as fw:
#     d = fw.write(prefixed_html)
# print(prefixed_html)