# CPE Data Collection and API Development

This project was built for a cybersecurity internship assessment. The goal was to take a large XML dataset from NIST's official CPE dictionary, extract the relevant details, and make them accessible in a more usable form. I wrote a Python script to parse the XML, created a schema in SQLite to store the data efficiently, and then built a REST API using Flask to interact with the dataset. The result is a simple local API that makes it easy to search and page through over 1.4 million CPE entries based on things like title, URIs, and deprecation status.
---

## Files Included

| File                                | Purpose                                                   |
|-------------------------------------|-----------------------------------------------------------|
| `read_cpe.py`                       | Parses the XML and populates the database                 |
| `setup.sql`                         | SQL file that defines the schema and indexes              |
| `cpe_data.db`                       | The SQLite database (generated after running the script)  |
| `app.py`                            | Main Flask API backend                                    |
| `official-cpe-dictionary_v2.3.xml`  | Source XML file from NIST                                 |

---

## Large Files (External Links)

- 📂 [Download cpe_data.db](https://1drv.ms/u/c/e3db8d91938a2eeb/EV8OC0MRAdxOsGRhlpWMEqUBbIg7-SZ_gJVeR4FycesEHg?e=2IONKS)
- 📂 [Download official-cpe-dictionary_v2.3.xml](https://1drv.ms/u/c/e3db8d91938a2eeb/Eb4LWr1-sNlPuxAVotV-5-cBtRexXswLTMSRU7NjuxKH4A?e=fMFgF1)


## What I Did
- Wrote a Python script using `ElementTree` to parse over 1.4 million XML records.
- Created a SQLite schema and used batch inserts for performance.
- Designed and built REST API routes with Flask to support both pagination and search.
- Tested everything locally with different parameters to make sure it responds fast and accurately.

---

## How to Run It (Step-by-Step)

### 1. Prerequisites
- Make sure Python 3.13+ is installed.
- This is a local project. No deployment or external database required.

### 2. Install Dependencies
Open your terminal and install Flask:

```bash
pip install flask
```

### 3. Set Up the Database and Import the Data
This step parses the XML file and loads the data into a local SQLite database:

```bash
python read_cpe.py
```

This will:
- Create the `cpe_data.db` file
- Create the schema and indexes (if not already there)
- Insert all 1.4 million+ CPE entries from `official-cpe-dictionary_v2.3.xml`

### 4. Run the API Server
Start the Flask server:

```bash
python app.py
```

Once the server is running, visit this URL in your browser:

```
http://127.0.0.1:5000/
```

You should see:
```
"CPE API is up and running."
```

---

## API Endpoints

### `GET /api/cpes`
Returns all CPEs with pagination support.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)

**Example:**
```
http://127.0.0.1:5000/api/cpes?page=2&limit=15
```

### `GET /api/cpes/search`
Filters the CPEs based on query parameters.

**Query Parameters:**
- `cpe_title`: partial or full match on the title
- `cpe_22_uri`: partial match on CPE 2.2 URI
- `cpe_23_uri`: partial match on CPE 2.3 URI
- `deprecation_date`: filters all entries deprecated **before** this date. Applies to both v2.2 and v2.3 deprecation fields.

**Example:**
```
http://127.0.0.1:5000/api/cpes/search?cpe_title=windows&deprecation_date=2024-01-01
```

---

## Data Source
- [Official CPE Dictionary v2.3 (NVD/NIST)](https://nvd.nist.gov/products/cpe)

This XML file is huge and publicly available, commonly used in vulnerability analysis and asset inventories.

---

## Output Example

Visiting this:
```
http://127.0.0.1:5000/api/cpes?page=1&limit=5
```
returns JSON like:
```json
{
  "page": 1,
  "limit": 5,
  "total": 1413024,
  "data": [
    {
      "id": 1,
      "cpe_title": "Example CPE Title",
      "cpe_22_uri": "cpe:/a:example:22",
      "cpe_23_uri": "cpe:/a:example:23",
      "reference_links": ["link1", "link2"],
      "cpe_22_deprecation_date": null,
      "cpe_23_deprecation_date": null
    },
    ...
  ]
}
```

---

This project demonstrates working with real-world datasets, backend API development, and designing for performance and usability all in one place.
