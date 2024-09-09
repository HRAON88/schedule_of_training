from database.connection import Connection

from app.database.models.roles import RolesModel
from app.database.models.sport import SportsModel
from app.database.repository.roles import RolesRepository
from app.database.repository.sports import SportsRepository
from telegram.tg_functional import bot


def upload_roles(con):
    role_rep = RolesRepository(con)
    for role in [
        RolesModel(id=1, role="admin"),
        RolesModel(id=2, role="coach"),
        RolesModel(id=3, role="sportsman"),
    ]:
        m = role_rep.get_by_id(role.id)
        if not m:
            role_rep.add(role)


def upload_sports(con):
    rep = SportsRepository(con)
    for model in [
        SportsModel(id=1, sport="Самбо"),
        SportsModel(id=2, sport="Бокс"),
        SportsModel(id=3, sport="Спортзал"),
    ]:
        m = rep.get_by_id(model.id)
        if not m:
            rep.add(model)


def create_tables(con):
    with open("init_db.txt", mode="r") as file:
        init_db = file.read()
    cur = con.cursor()
    cur.executescript(init_db)
    con.commit()


def launch_db():
    with Connection() as con:
        create_tables(con)
        upload_roles(con)
        upload_sports(con)


if __name__ == "__main__":
    print("start app")
    launch_db()
    bot.polling()