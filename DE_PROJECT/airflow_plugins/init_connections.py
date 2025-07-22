# airflow_plugins/init_connections.py

from airflow.models.connection import Connection
from airflow import settings
from sqlalchemy.orm import Session

def create_connection_if_not_exists(conn: Connection):
    session: Session = settings.Session()
    existing = session.query(Connection).filter(Connection.conn_id == conn.conn_id).first()
    if existing:
        print(f"🔄 Connection '{conn.conn_id}' already exists.")
        return
    session.add(conn)
    session.commit()
    print(f"✅ Connection '{conn.conn_id}' created.")

def init_connections():
    connections = [
        Connection(
            conn_id="postgres_dw",
            conn_type="postgres",
            host="postgres_dw",
            schema="ipl_warehouse",
            login="ipl_data",
            password="ipl_data",
            port=5432
        ),
        Connection(
            conn_id="mysql_source",
            conn_type="mysql",
            host="mysql_source",
            schema="ipl_daily_db",
            login="ipl_user",
            password="ipl_password",
            port=3306
        ),
        Connection(
            conn_id="spark_ssh",
            conn_type="ssh",
            host="spark-master",
            login="bitnami",  # change if needed
            port=22
        ),
        Connection(
            conn_id="kafka_default",
            conn_type="generic",  # use 'http' if you want
            host="kafka",
            port=9092,
            extra='{"bootstrap_servers": "kafka:9092"}'
        ),
        Connection(
            conn_id="redis_default",
            conn_type="redis",
            host="redis",
            port=6379
        )
    ]

    for conn in connections:
        create_connection_if_not_exists(conn)

if __name__ == "__main__":
    init_connections()
