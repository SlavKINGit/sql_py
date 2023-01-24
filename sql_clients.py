# createdb -U postgres netology_db

import psycopg2


def createdb(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS clients(
                    id serial PRIMARY KEY,
                    first_name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email text NOT NULL UNIQUE
                );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS phones(
                    client_id int NOT NULL REFERENCES clients(id),
                    phone bigint NOT NULL UNIQUE
                );''')


def add_client(cur, first_name, last_name, email):
    cur.execute('''INSERT INTO clients(first_name, last_name, email)
                VALUES
                (%s, %s, %s);''', (first_name, last_name, email))


def add_phone(cur, client_id, phone):
    cur.execute('''INSERT INTO phones
                VALUES
                (%s, %s);''', (client_id, phone))


def change_client_data(cur, id, first_name=None, last_name=None, email=None):
    if first_name is not None:
        cur.execute('''UPDATE clients
                    SET first_name = %s
                    WHERE id = %s;''', (first_name, id))
    if last_name is not None:
        cur.execute('''UPDATE clients
                    SET last_name = %s
                    WHERE id = %s;''', (last_name, id))
    if email is not None:
        cur.execute('''UPDATE clients
                    SET email = %s
                    WHERE id = %s;''', (email, id))


def delete_phone(cur, phone):
    cur.execute('''DELETE FROM phones
                WHERE phone = %s;''', (phone, ))


def delete_client(cur, id):
    cur.execute('''DELETE FROM phones
                WHERE client_id = %s;''', (id, ))
    cur.execute('''DELETE FROM clients
                WHERE id = %s;''', (id, ))


def find_client_by_info(cur, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cur.execute('''SELECT *
                    FROM clients
                    WHERE first_name = %s;''', (first_name, ))
        print('Matched first_names:')
        print(cur.fetchone())
    if last_name is not None:
        cur.execute('''SELECT *
                    FROM clients
                    WHERE last_name = %s;''', (last_name, ))
        print('Matched last_names:')
        print(cur.fetchone())
    if email is not None:
        cur.execute('''SELECT *
                    FROM clients
                    WHERE email = %s;''', (email, ))
        print('Matched emails:')
        print(cur.fetchone())
    if phone is not None:
        cur.execute('''SELECT *
                    FROM clients
                    WHERE id = (SELECT DISTINCT(client_id)
                                        FROM phones
                                        WHERE phone = %s);''', (phone, ))
        print('Matched phones:')
        print(cur.fetchone())


def main():
    with psycopg2.connect(database='netology_db', user='postgres', password='7355608') as conn:
        with conn.cursor() as cursor:
            # createdb(cursor)
            # add_client(cursor, 'Bruce', 'Mathers', 'BruceMM@gmail.com')
            # add_client(cursor, 'Mickey', 'Mouse', 'MickeyMouse@gmail.com')
            # add_phone(cursor, 1, 88005553535)
            # add_phone(cursor, 2, 89262474989)
            # change_client_data(cursor, 1, 'Valera', 'Shamanin', 'ShamaninVV@mail.ru')
            # delete_phone(cursor, '89771112323')
            # find_client_by_info(cursor, first_name=None, last_name=None, email=None, phone=88005553535)
            delete_client(cursor, 1)


if __name__ == '__main__':
    main()
