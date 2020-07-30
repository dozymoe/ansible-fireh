import os
import psycopg2

conn_args = 'postgresql://%s:%s@%s:%s/%s' % (
    os.environ['DATABASE_USER'],
    os.environ['DATABASE_PASSWORD'],
    os.environ.get('DATABASE_HOST', '127.0.0.1'),
    os.environ.get('DATABASE_PORT', '5432'),
    os.environ['DATABASE_NAME'],
)
conn = psycopg2.connect(conn_args)
cur = conn.cursor()
cur.execute("""
        CREATE TABLE IF NOT EXISTS virtual_domains (
          id serial NOT NULL,
          name varchar(50) NOT NULL,

          PRIMARY KEY (id)
        )
        """)
cur.execute("""
        CREATE TABLE IF NOT EXISTS virtual_users (
          id serial NOT NULL,
          domain_id integer NOT NULL,
          password varchar(255) NOT NULL,
          email varchar(100) NOT NULL,

          PRIMARY KEY (id),
          UNIQUE (email),
          FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
        )
        """)
cur.execute("""
        CREATE TABLE IF NOT EXISTS virtual_aliases (
          id serial NOT NULL,
          domain_id integer NOT NULL,
          source varchar(100) NOT NULL,
          destination varchar(100) NOT NULL,

          PRIMARY KEY (id),
          FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
        )
        """)
conn.commit()
