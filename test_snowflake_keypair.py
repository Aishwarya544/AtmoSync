 
import os
import snowflake.connector
from dotenv import load_dotenv

# Load Snowflake settings from the .env file
load_dotenv()

conn = None
cursor = None

try:
    print("Connecting to Snowflake using key-pair authentication...")

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user="bokkiaishwarya",

        # Location of your private key
        private_key_file=r"C:\Users\bokki\snowflake_private_key.pem",

        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

    print("\nSuccessfully connected to Snowflake!")

    cursor = conn.cursor()

    # Verify the Snowflake connection
    cursor.execute("""
        SELECT
            CURRENT_USER(),
            CURRENT_ROLE(),
            CURRENT_DATABASE(),
            CURRENT_SCHEMA(),
            CURRENT_WAREHOUSE()
    """)

    print("\nConnection details:")
    print(cursor.fetchone())

    # Check the sensor readings table
    cursor.execute("""
        SELECT COUNT(*)
        FROM ATMOSYNC_DB.RAW.SENSOR_READINGS
    """)

    print("\nSensor readings in Snowflake:")
    print(cursor.fetchone()[0])

except Exception as error:
    print("\nConnection failed:")
    print(error)

finally:
    if cursor:
        cursor.close()

    if conn:
        conn.close()
        print("\nSnowflake connection closed.")
