from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Just a test route to make sure the server is running
@app.route('/')
def home():
    return "CPE API is up and running."

# Route to get CPEs with page and limit
@app.route('/api/cpes')
def get_cpes():
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 10)

    page = int(page)
    limit = int(limit)
    offset = (page - 1) * limit

    # Connect to database
    conn = sqlite3.connect('cpe_data.db')
    cursor = conn.cursor()

    # Get total count
    cursor.execute('SELECT COUNT(*) FROM cpes')
    total = cursor.fetchone()[0]

    # Get some rows based on page and limit
    cursor.execute('SELECT * FROM cpes ORDER BY id LIMIT ? OFFSET ?', (limit, offset))
    rows = cursor.fetchall()

    # Get column names
    col_names = [desc[0] for desc in cursor.description]

    data = []
    for row in rows:
        entry = dict(zip(col_names, row))
        # Convert reference_links back to list
        if entry['reference_links']:
            entry['reference_links'] = json.loads(entry['reference_links'])
        else:
            entry['reference_links'] = []
        data.append(entry)

    conn.close()

    # Return everything in a JSON response
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "data": data
    })

# Route to search CPEs
@app.route('/api/cpes/search')
def search_cpes():
    title = request.args.get('cpe_title')
    uri_22 = request.args.get('cpe_22_uri')
    uri_23 = request.args.get('cpe_23_uri')
    date = request.args.get('deprecation_date')

    filters = []
    values = []

    if title:
        filters.append("cpe_title LIKE ?")
        values.append(f"%{title}%")
    if uri_22:
        filters.append("cpe_22_uri LIKE ?")
        values.append(f"%{uri_22}%")
    if uri_23:
        filters.append("cpe_23_uri LIKE ?")
        values.append(f"%{uri_23}%")
    if date:
        filters.append("(cpe_22_deprecation_date < ? OR cpe_23_deprecation_date < ?)")
        values.append(date)
        values.append(date)

    query = "SELECT * FROM cpes"
    if filters:
        query += " WHERE " + " AND ".join(filters)

    conn = sqlite3.connect('cpe_data.db')
    cursor = conn.cursor()
    cursor.execute(query, values)
    rows = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]

    data = []
    for row in rows:
        entry = dict(zip(col_names, row))
        if entry['reference_links']:
            entry['reference_links'] = json.loads(entry['reference_links'])
        else:
            entry['reference_links'] = []
        data.append(entry)

    conn.close()

    return jsonify({
        "data": data
    })

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
