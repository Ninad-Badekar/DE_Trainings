import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()
SOURCE_DB = os.getenv("DATABASE_URL")   
DEST_DB = os.getenv("DEST_DB")          

source_engine = create_engine(SOURCE_DB)
dest_engine = create_engine(DEST_DB)

SourceSession = sessionmaker(bind=source_engine)
DestSession = sessionmaker(bind=dest_engine)

TABLE_NAME = "users"
TRACK_COLUMN = "user_id"  

def get_existing_user_ids(session):
    result = session.execute(text(f"SELECT {TRACK_COLUMN} FROM {TABLE_NAME}"))
    return {row[0] for row in result.fetchall()}

def incremental_upsert():
    source_session = SourceSession()
    dest_session = DestSession()

    try:
        print("Fetching existing user_ids from destination...")
        existing_ids = get_existing_user_ids(dest_session)
        print(f"Found {len(existing_ids)} existing user_ids in destination.")

        
        if not existing_ids:
            query = text(f"SELECT * FROM {TABLE_NAME}")
        else:
            id_list = ", ".join(map(str, existing_ids))
            query = text(f"""
                SELECT * FROM {TABLE_NAME}
                WHERE {TRACK_COLUMN} NOT IN ({id_list})
                OR {TRACK_COLUMN} IN ({id_list})
            """)

        rows = source_session.execute(query).fetchall()

        if not rows:
            print("No records to insert or update.")
            return

        
        columns = list(rows[0]._mapping.keys())
        placeholders = ", ".join([f":{col}" for col in columns])
        update_clause = ", ".join([
            f"{col} = VALUES({col})" for col in columns if col != TRACK_COLUMN
        ])

        insert_sql = text(f"""
            INSERT INTO {TABLE_NAME} ({', '.join(columns)})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE {update_clause}
        """)

        for row in rows:
            dest_session.execute(insert_sql, dict(row._mapping))

        dest_session.commit()
        print(f"Upserted {len(rows)} records.")

    except Exception as e:
        dest_session.rollback()
        print(f"Error during sync: {e}")
    finally:
        source_session.close()
        dest_session.close()

if __name__ == "__main__":
    incremental_upsert()
