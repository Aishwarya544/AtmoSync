 
import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

conn = None
cursor = None

try:
    print("Opening Snowflake browser authentication...")

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        authenticator="externalbrowser",
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    print("\nSuccessfully connected to Snowflake!")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            CURRENT_ACCOUNT(),
            CURRENT_USER(),
            CURRENT_ROLE(),
            CURRENT_DATABASE(),
            CURRENT_SCHEMA(),
            CURRENT_WAREHOUSE()
    """)

    print("\nConnection details:")
    print(cursor.fetchone())

    cursor.execute("""
        SELECT *
        FROM ATMOSYNC_DB.RAW.SENSOR_READINGS
        ORDER BY RECORDED_AT DESC
        LIMIT 5
    """)

    print("\nLatest sensor readings:")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    if not rows:
        print("No sensor readings found.")

except Exception as error:
    print("\nConnection failed:")
    print(error)

finally:
    if cursor:
        cursor.close()

    if conn:
        conn.close()
        print("\nSnowflake connection closed.")
