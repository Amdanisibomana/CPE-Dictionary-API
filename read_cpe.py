import xml.etree.ElementTree as ET
import sqlite3
import json

# Connect to SQLite (creates cpe_data.db if it doesn't exist)
conn = sqlite3.connect("cpe_data.db")
cursor = conn.cursor()

# Create table and indexes if they don't already exist
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS cpes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpe_title TEXT,
        cpe_22_uri TEXT,
        cpe_23_uri TEXT,
        reference_links TEXT,
        cpe_22_deprecation_date TEXT,
        cpe_23_deprecation_date TEXT
    );

    CREATE INDEX IF NOT EXISTS idx_title ON cpes (cpe_title);
    CREATE INDEX IF NOT EXISTS idx_uri22 ON cpes (cpe_22_uri);
    CREATE INDEX IF NOT EXISTS idx_uri23 ON cpes (cpe_23_uri);
    CREATE INDEX IF NOT EXISTS idx_deprecation_22 ON cpes (cpe_22_deprecation_date);
    CREATE INDEX IF NOT EXISTS idx_deprecation_23 ON cpes (cpe_23_deprecation_date);
''')

# Load the XML file
tree = ET.parse("official-cpe-dictionary_v2.3.xml")
root = tree.getroot()

# Namespace 
ns = {'cpe': 'http://cpe.mitre.org/dictionary/2.0'}

count = 0

# Loop through each cpe-item
for item in root.findall('cpe:cpe-item', ns):
    cpe_23_uri = item.get('name')
    cpe_title = None
    cpe_22_uri = None
    refs = []
    date_22 = None
    date_23 = None

    title = item.find('cpe:title', ns)
    if title is not None:
        cpe_title = title.text

    ref_tags = item.findall('cpe:references/cpe:reference', ns)
    for ref in ref_tags:
        refs.append(ref.text)

    item_22 = item.find('cpe:cpe-22-item', ns)
    if item_22 is not None:
        cpe_22_uri = item_22.get('name')
        dep_22 = item_22.find('cpe:deprecated', ns)
        if dep_22 is not None:
            date_22 = dep_22.get('date')

    dep_23 = item.find('cpe:deprecated', ns)
    if dep_23 is not None:
        date_23 = dep_23.get('date')

    # Insert into database
    cursor.execute('''
        INSERT INTO cpes (
            cpe_title,
            cpe_22_uri,
            cpe_23_uri,
            reference_links,
            cpe_22_deprecation_date,
            cpe_23_deprecation_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        cpe_title,
        cpe_22_uri,
        cpe_23_uri,
        json.dumps(refs),
        date_22,
        date_23
    ))

    count += 1

    # Commit every 1000 records to avoid memory issues
    # and to keep the database responsive
    if count % 1000 == 0:
        conn.commit()
        print("Inserted", count)

# Final commit and wrap up
conn.commit()
print("Finished. Total:", count)
conn.close()
