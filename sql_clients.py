# createdb -U postgres netology_db

import psycopg2

conn = psycopg2.connect(database='netology_db', user='postgres', password='7355608')
cur = conn.cursor()


def createdb():
    cur.execute('''CREATE TABLE IF NOT EXISTS clients(
                    id serial PRIMARY KEY,
                    first_name VARCHAR(60) NOT NULL,
                    last_name VARCHAR(60) NOT NULL,
                    email text NOT NULL UNIQUE,
                    phone text[]
                );''')
    conn.commit()


def add_client(first_name, last_name, email, phone='{""}'):
    cur.execute('INSERT INTO clients(first_name, last_name, email, phone) VALUES(%s, %s, %s, %s);', (first_name, last_name, email, phone))
    conn.commit()


def add_phone(phone, id):
    cur.execute('SELECT array_length(phone, 1) FROM clients WHERE id = %s;', (id, ))
    num = cur.fetchone()[0] + 1
    cur.execute('UPDATE clients SET phone[%s] = %s WHERE id = %s;', (num, phone, id))
    conn.commit()


def change_client_data(id, first_name=None, last_name=None, email=None):
    if first_name is not None:
        cur.execute('UPDATE clients SET first_name = %s WHERE id = %s;', (first_name, id))
        conn.commit()
    if last_name is not None:
        cur.execute('UPDATE clients SET last_name = %s WHERE id = %s;', (last_name, id))
        conn.commit()
    if email is not None:
        cur.execute('UPDATE clients SET email = %s WHERE id = %s;', (email, id))
        conn.commit()


def delete_phone(phone, id):
    cur.execute('SELECT phone FROM clients WHERE id = %s;', (id, ))
    set_ = set()
    for i in cur.fetchone()[0]:
        if i != phone and i is not None:
            set_.add(i)
    good_phones = f'{set_}'
    cur.execute('UPDATE clients SET phone = %s WHERE id = %s;', (good_phones, id))
    conn.commit()


def delete_client(id):
    cur.execute('DELETE FROM clients WHERE id = %s;', (id, ))
    conn.commit()


def find_client_by_info(first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cur.execute('SELECT * FROM clients WHERE first_name = %s;', (first_name, ))
        print('Matched first_names:')
        print(cur.fetchone())
    if last_name is not None:
        cur.execute('SELECT * FROM clients WHERE last_name = %s;', (last_name, ))
        print('Matched last_names:')
        print(cur.fetchone())
    if email is not None:
        cur.execute('SELECT * FROM clients WHERE email = %s;', (email, ))
        print('Matched emails:')
        print(cur.fetchone())
    if phone is not None:
        cur.execute('SELECT * FROM clients WHERE phone && ARRAY[%s];', (phone, ))
        print('Matched phones:')
        print(cur.fetchone())


def main():
    createdb()
    add_client('Bruce', 'Mathers', 'BruceMM@gmail.com', '{"88005553535"}')
    add_phone('89771112323', 1)
    change_client_data(1, 'Valera', 'Shamanin', 'ShamaninVV@mail.ru')
    delete_phone('89771112323', 1)
    find_client_by_info(first_name=None, last_name=None, email=None, phone='88005553535')
    delete_client(1)
    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
