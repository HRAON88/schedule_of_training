from app.database.connection import Connection
from app.database.models.user import UserModel
from app.database.repository.roles import RolesRepository
from app.database.repository.users import UsersRepository


class Core:
    def is_admin_mode(self):
        with Connection() as c:
            r = UsersRepository(c)
            return len(r.get_all()) == 0

    def get_user(self, user_id) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            return r.get_by_id(user_id)

    def get_roles(self):
        with Connection() as c:
            r = RolesRepository(c)
            return r.get_all()

    def add_admin_user(self, user_id, first_name, last_name, username) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            role_r = RolesRepository(c)
            admin_role = role_r.get_by_role("admin")
            if not admin_role:
                raise ValueError("Admin role not found")
            m = UserModel(
                id=user_id,
                firstname=first_name,
                lastname=last_name,
                username=username,
                role_id=admin_role.id,
            )
            return r.add(m)

    def add_basic_user(self, user_id, first_name, last_name, username) -> UserModel:
        with Connection() as c:
            r = UsersRepository(c)
            role_r = RolesRepository(c)
            admin_role = role_r.get_by_role("sportsman")
            if not admin_role:
                raise ValueError("Admin role not found")
            m = UserModel(
                id=user_id,
                firstname=first_name,
                lastname=last_name,
                username=username,
                role_id=admin_role.id,
            )
            return r.add(m)
