from app.database.models.roles import RolesModel
from app.database.repository.roles import RolesRepository

from app.telegram_bot.aio_bot import main
from database.connection import Connection


def launch_db():
    with open("init_db.txt", mode="r") as file:
        init_db = file.read()
    with Connection() as con:
        cur = con.cursor()
        cur.executescript(init_db)
        con.commit()

        role_rep = RolesRepository(con)
        for role in [
            RolesModel(id=1, role="admin"),
            RolesModel(id=2, role="coach"),
            RolesModel(id=3, role="sportsman"),
        ]:
            m = role_rep.get_by_id(role.id)
            if not m:
                role_rep.add(role)


if __name__ == '__main__':
    print("start app")
    launch_db()
    main()
