import mysql.connector
from mysql.connector import Error

db_config = {
    'host': 'my-db-server1.mysql.database.azure.com',
    'user': 'admin_user',
    'password': 'Project@db',
    'database': 'companydb',
    'ssl_ca': 'BaltimoreCyberTrustRoot.crt.pem'
}

def execute_sql_script(script_path):
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        with open(script_path, 'r') as file:
            sql_script = file.read()

        # Split SQL commands by semicolons
        commands = sql_script.split(';')

        for command in commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    connection.commit()
                    print(f"Executed: {command[:50]}...")
                except Error as e:
                    if e.errno == 1060:  # Duplicate column error
                        print(f"⚠️ Column already exists: Skipping...")
                    else:
                        raise e  # Re-raise other errors

        print("\n✅ All SQL commands executed successfully!")

    except Error as e:
        print(f"❌ Error: {e}")
        if connection and connection.is_connected():
            connection.rollback()

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Connection closed.")

if __name__ == "__main__":
    execute_sql_script('schema_changes.sql')