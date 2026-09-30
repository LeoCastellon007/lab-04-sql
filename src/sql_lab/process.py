#!/usr/bin/env python3

"""Read MOCK_DATA.csv, clean it, and upload it to the `mock` table in MySQL."""

import logging
import os
import re

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

# Map pandas dtypes (from df.dtypes) to MySQL column types.
TYPE_MAPPING = {
    "int64": "BIGINT",
    "int32": "INT",
    "float64": "DOUBLE",
    "bool": "TINYINT(1)",
    "datetime64[ns]": "DATETIME",
    "datetime64[us]": "DATETIME",
    "object": "VARCHAR(255)",  # safe default varchar length
    "string": "VARCHAR(255)",
    "str": "VARCHAR(255)",  # pandas 3 default string dtype
}


def read_data(filename):
    """Load a CSV file into a pandas DataFrame and return it."""
    logger.info("Reading %s", filename)
    df = pd.read_csv(filename)
    logger.info("Read %d rows and %d columns", len(df), len(df.columns))
    return df


def clean_data(data):
    """Drop rows with missing values and cast columns to upload-ready types.

    `signup_date` arrives as text like 9/22/2026 and is converted to a datetime
    so it maps to a SQL DATETIME column.
    """
    logger.info("Cleaning %d rows", len(data))
    df = data.copy()

    # Normalize column names: lowercase, no surrounding spaces
    df.columns = [c.strip().lower() for c in df.columns]

    # Treat empty or whitespace-only strings as missing, then drop incomplete rows
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    before = len(df)
    df = df.dropna()
    logger.info("Dropped %d rows with missing values", before - len(df))

    # Cast types so the dtype -> SQL mapping produces sensible columns
    df["id"] = df["id"].astype("int64")
    df["age"] = df["age"].astype("int64")
    df["signup_date"] = pd.to_datetime(df["signup_date"], format="%m/%d/%Y")

    logger.info("Cleaned data has %d rows", len(df))
    return df


def load_data(data, table):
    """Create `table` if needed and insert every DataFrame row into it.

    Uses parameterized INSERTs (approach A). Existing rows are cleared first, so
    rerunning the script reloads the table instead of failing on duplicate ids.
    """
    # Table and column names cannot be %s parameters, so only allow plain identifiers
    for name in [table, *data.columns]:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            raise ValueError(f"Unsafe SQL identifier: {name!r}")

    # Build the column definitions from the DataFrame dtypes; id is the primary key
    col_defs = []
    for col, dtype in data.dtypes.items():
        sql_type = TYPE_MAPPING.get(str(dtype), "VARCHAR(255)")
        pk = " PRIMARY KEY" if col == "id" else ""
        col_defs.append(f"`{col}` {sql_type} NOT NULL{pk}")
    create_stmt = f"CREATE TABLE IF NOT EXISTS `{table}` ({', '.join(col_defs)})"

    # Backticks are needed because `group` is a reserved word in MySQL
    columns = ", ".join(f"`{c}`" for c in data.columns)
    placeholders = ", ".join(["%s"] * len(data.columns))
    insert_stmt = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"

    db = None
    try:
        logger.info("Connecting to %s on %s", DBNAME, DBHOST)
        db = mysql.connector.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
        cursor = db.cursor()

        logger.info("Creating table `%s` if it does not exist", table)
        cursor.execute(create_stmt)
        cursor.execute(f"DELETE FROM `{table}`")

        # astype(object) turns numpy ints/timestamps into plain Python values
        for row in data.astype(object).itertuples(index=False):
            cursor.execute(insert_stmt, tuple(row))

        db.commit()
        logger.info("Inserted %d rows into `%s`", len(data), table)
        cursor.close()
    except mysql.connector.Error as e:
        logger.error("MySQL error: %s", e)
        if db is not None:
            db.rollback()
        raise
    finally:
        if db is not None and db.is_connected():
            db.close()
            logger.info("Connection closed")


def main():
    """Run the read -> clean -> load pipeline for MOCK_DATA.csv."""
    logger.info("Starting upload")
    df = read_data("MOCK_DATA.csv")
    df = clean_data(df)
    load_data(df, "mock")
    logger.info("Done")


if __name__ == "__main__":
    main()
