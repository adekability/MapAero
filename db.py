import sqlite3
from services import resource_path


def create_record(filename, lat, lon, file, color, current_datetime, load_name):
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    """
    Create a new record in the main table.

    Parameters:
    - filename: str, the filename for the record
    - lat: float, latitude value
    - lon: float, longitude value
    """
    try:
        cursor.execute('''INSERT INTO main (filename, lat, lon, image, color, datetime, name) VALUES (?, ?, ?, ?, ?, ?, ?)''', (filename, lat, lon, file, color, current_datetime, load_name))
        conn.commit()
        print("Record created successfully!")
        cursor.close()
        conn.close()
    except sqlite3.IntegrityError:
        print(f"Record with filename '{filename}' already exists.")
        cursor.close()
        conn.close()

def delete_record(filename):
    """
    Delete a record from the main table by filename.

    Parameters:
    - filename: str, the filename of the record to delete
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM main WHERE filename = ?''', (filename,))
    if cursor.rowcount > 0:
        conn.commit()
        print(f"Record with filename '{filename}' deleted successfully!")
    else:
        print(f"No record found with filename '{filename}'.")
    cursor.close()
    conn.close()

def get_record(lat, lon):
    """
    Get a record from the main table by filename.

    Parameters:
    - filename: str, the filename of the record to retrieve

    Returns:
    - tuple or None: the record if found, None if not found
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM main WHERE lat = ? AND lon = ?''', (lat, lon))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return record
    else:
        print(f"No record found")
        return None

def get_image(filename: str):
    """
    Get a record from the main table by filename.

    Parameters:
    - filename: str, the filename of the record to retrieve

    Returns:
    - tuple or None: the record if found, None if not found
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT image FROM main WHERE filename = ? ''', (filename,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if record:
        return record[0]
    else:
        print(f"No record found")
        return None

def fetch_all_records(image=False):
    """
    Fetch all records from the main table.

    Returns:
    - list of tuples: all records from the main table
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    if not image:
        cursor.execute('''SELECT filename, lat, lon, color, datetime, id, name FROM main''')
    else:
        cursor.execute('''SELECT * FROM main''')
    records = cursor.fetchall()
    if records:
        cursor.close()
        conn.close()
        return records
    else:
        print("No records found in the main table.")
        cursor.close()
        conn.close()
        return []

def fetch_records_by_datetime(datetimes, image=False):
    """
    Fetch all records from the main table.

    Returns:
    - list of tuples: all records from the main table
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    if not image:
        cursor.execute('SELECT filename, lat, lon, color, datetime, id FROM main WHERE datetime (%s)' % ','.join('?' * len(datetimes)), datetimes)
    else:
        cursor.execute('SELECT * FROM main WHERE datetime (%s)' % ','.join('?' * len(datetimes)), datetimes)
    records = cursor.fetchall()
    if records:
        cursor.close()
        conn.close()
        return records
    else:
        print("No records found in the main table.")
        cursor.close()
        conn.close()
        return []

def fetch_distinct_colors():
    """
    Fetch all distinct colors from the main table.

    Returns:
    - list of tuples: all distinct colors from the main table
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT DISTINCT color FROM main''')
    records = cursor.fetchall()
    if records:
        cursor.close()
        conn.close()
        return records
    else:
        print("No records found in the main table.")
        cursor.close()
        conn.close()
        return []
def fetch_distinct_names():
    """
    Fetch all distinct colors from the main table.

    Returns:
    - list of tuples: all distinct colors from the main table
    """
    main_db = resource_path('main.db')
    conn = sqlite3.connect(main_db)
    cursor = conn.cursor()
    cursor.execute('''SELECT name, color from main group by name;''')
    records = cursor.fetchall()
    if records:
        cursor.close()
        conn.close()
        return records
    else:
        print("No records found in the main table.")
        cursor.close()
        conn.close()
        return []
