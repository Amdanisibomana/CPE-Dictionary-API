-- This creates the table to store the CPE data pulled from the XML file.
-- I'm using TEXT for most of these since SQLite handles strings well,
-- and I'm storing reference_links as a JSON string.

CREATE TABLE IF NOT EXISTS cpes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpe_title TEXT,
    cpe_22_uri TEXT,
    cpe_23_uri TEXT,
    reference_links TEXT, -- just saving the list of links as a JSON string
    cpe_22_deprecation_date TEXT, -- using text here, will store dates as strings like "2024-01-01"
    cpe_23_deprecation_date TEXT
);

-- These indexes are here just to make searching faster later on.
-- I added them for the fields I thought someone might filter by.

CREATE INDEX IF NOT EXISTS idx_title ON cpes (cpe_title);
CREATE INDEX IF NOT EXISTS idx_uri22 ON cpes (cpe_22_uri);
CREATE INDEX IF NOT EXISTS idx_uri23 ON cpes (cpe_23_uri);
CREATE INDEX IF NOT EXISTS idx_deprecation_22 ON cpes (cpe_22_deprecation_date);
CREATE INDEX IF NOT EXISTS idx_deprecation_23 ON cpes (cpe_23_deprecation_date);
