import sqlite3 as sq



class Executions:
    def __init__(self, path) -> None:
        self.bdname = path


    def insert_data(self, value1, value2, remind_constantly: int = 0) -> None:
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            cur.execute(f'''INSERT INTO notes (date, text, remind_constantly) VALUES ('{value1}', '{value2}', '{remind_constantly}');''')
    

    def give_all_data(self) -> tuple:
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            arr = cur.execute('''SELECT * FROM notes ORDER BY date;''').fetchall()
        return arr
    

    def del_all_notes(self) -> None:
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM notes''')


    def give_nearest_note(self) -> list:
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            cur.execute(f'''SELECT * FROM notes ORDER BY date LIMIT 1;''')
            note = cur.fetchall()
        return note


    def del_note(self, key: int) -> None:
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            cur.execute(f'''DELETE FROM notes WHERE number = {key}''')
    

    def check_bd_existing(self):
        with sq.connect(self.bdname) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS notes(
                    number INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATETIME,
                    text TEXT,
                    remind_constantly BIT 
                    )""")
