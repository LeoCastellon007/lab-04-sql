#!/usr/bin/env python3

"""Query the `mock` table in your COMPUTING_ID_mock database."""

import logging
import os

import mysql.connector
import pandas as pd

# In your terminal, define the following environment variables:
# export DBHOST='ds2022.cgls84scuy1e.us-east-1.rds.amazonaws.com'
# export DBUSER='COMPUTING_ID'
# export DBPASS='COMPUTING_ID'
# export DBNAME='COMPUTING_ID_mock'
DBHOST = os.environ.get("DBHOST")
DBUSER = os.environ.get("DBUSER")
DBPASS = os.environ.get("DBPASS")
DBNAME = os.environ.get("DBNAME")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TABLE = "mock"


def get_connection():
    """Open and return a connection to the mock database."""
    logger.info("Connecting to %s on %s", DBNAME, DBHOST)
    return mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)


def get_data_by_group(value):
    """Return all `mock` rows whose `group` column equals ``value`` (list of tuples)."""
    # `group` is a reserved word, so it must be quoted with backticks
    query = f"SELECT * FROM `{TABLE}` WHERE `group` = %s ORDER BY id;"
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        cursor.execute(query, (value,))  # parameterized: no SQL injection
        results = cursor.fetchall()
        cursor.close()
        logger.info("Found %d rows where group = %r", len(results), value)
        return results
    except mysql.connector.Error as e:
        logger.error("MySQL error: %s", e)
        return None
    finally:
        if db is not None and db.is_connected():
            db.close()


def plot_counts(groupby):
    """Count `mock` rows per distinct value of column ``groupby`` and return a DataFrame."""
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()

        # Column names cannot be %s parameters, so check against the real columns first
        cursor.execute(f"SHOW COLUMNS FROM `{TABLE}`;")
        columns = [row[0] for row in cursor.fetchall()]
        if groupby not in columns:
            raise ValueError(f"Unknown column {groupby!r}; expected one of {columns}")

        query = (
            f"SELECT `{groupby}`, COUNT(*) AS n FROM `{TABLE}` "
            f"GROUP BY `{groupby}` ORDER BY n DESC;"
        )
        cursor.execute(query)
        df = pd.DataFrame(cursor.fetchall(), columns=[groupby, "count"])
        cursor.close()
        logger.info("Counted %d distinct values of %s", len(df), groupby)
        return df
    except mysql.connector.Error as e:
        logger.error("MySQL error: %s", e)
        return None
    finally:
        if db is not None and db.is_connected():
            db.close()


def main():
    """Demonstrate the query functions."""
    print("=== rows in group 'red' ===")
    rows = get_data_by_group("red")
    if rows is not None:
        for row in rows[:10]:
            print(row)
        print(f"... {len(rows)} rows total")

    print("=== counts per group ===")
    print(plot_counts("group"))

    print("=== counts per age (top 5) ===")
    counts = plot_counts("age")
    if counts is not None:
        print(counts.head())


if __name__ == "__main__":
    main()
