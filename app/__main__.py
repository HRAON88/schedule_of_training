from database.connection import Connection
from database.models.sport import SportsModel
from database.repository.sports import SportsRepository

def launch_db():
    with open("init_db.txt", mode="r") as file:
        init_db = file.read()
    with Connection() as con:
        cur = con.cursor()
        cur.executescript(init_db)
        con.commit()

if __name__ == '__main__':
    launch_db()

