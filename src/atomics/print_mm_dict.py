import re

MASS_RE = re.compile(
    r'<a href="[^"]*">'             # opening anchor tag
    r'\s*([A-Za-z]{1,2})-\s*(\d+)\s*'  # group 1: symbol, group 2: mass number (allows spaces before/after)
    r'</a>'                         # closing anchor tag
    r'\s+([\d.]+)'                  # group 3: mass in u
    r'\s+\+-'                       # the " +-" before uncertainty
)

def parse_element_page(text, store):
    """Adds nuclide molar masses (kg/mol) found in `text` into `store` with uppercase symbols."""
    for m in MASS_RE.finditer(text):
        symbol, A, mass_u = m.group(1).upper(), m.group(2), float(m.group(3))
        key = f"{symbol}{A}"
        if key not in store:
            store[key] = mass_u * 1e-3
    return store

complete_mm = {}
for i in range(0, 119):
    path = format("data/nuC_pages/Element" + i.__str__() + ".html")
    with open(path, mode="r") as f:
        text = f.read()
        # print(text)
        parse_element_page(text, complete_mm)

print(complete_mm)
