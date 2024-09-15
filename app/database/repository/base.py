from app.database.models.base import BaseModel


class BaseFunction:
    table = None
    model = None

    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()

    def get_by_id(self, item_id):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE id = {item_id}")
        result = self.cur.fetchone()
        if result:
            names = [description[0] for description in self.cur.description]
            return self.model(**{col: val for val, col in zip(result, names)})

    def get_all_users(self):
        self.cur.execute(f"SELECT * FROM {self.table}")
        result = self.cur.fetchall()
        if result:
            return self.model(*result)

    def add(self, model: BaseModel):
        columns, values = [], []
        for key, value in model.to_dict().items():
            if key == "id" and value is None:
                continue
            columns.append(key)
            if value is None:
                value = "null"
            values.append(value)
        self.cur.execute(f"INSERT INTO {self.table} {tuple(columns)} VALUES {tuple(values)}")
        model.id = self.cur.lastrowid
        self.connection.commit()
        return self.get_by_id(model.id)

    def delete(self, model: BaseModel):
        self.cur.execute(f"delete from {self.table} WHERE {self.table}.id = {model.id}")
        self.connection.commit()

    def update(self, model: BaseModel, item_id):
        spis = []
        for key, value in model.to_dict().items():
            if type(value) == int:
                spis.append(f"{key}={value}")
            elif type(value) == str:
                spis.append(f"{key}='{value}'")
        self.cur.execute(f"UPDATE {self.table} SET {', '.join(spis)} WHERE id = {item_id}")
        self.connection.commit()

    def get_all(self):
        self.cur.execute(f'select * from {self.table}')
        names = [description[0] for description in self.cur.description]
        result = [str(self.model(**{col: val for val, col in zip(item, names)})) for item in self.cur.fetchall()]
        return '\n'.join(result)

    def get_all_sportsman(self):
        self.cur.execute(f'select * from {self.table}')
        names = [description[0] for description in self.cur.description]
        return [self.model(**{col: val for val, col in zip(item, names)}) for item in self.cur.fetchall()]

