import reflex as rx
from typing import TypedDict, Optional
from sqlalchemy import text


class User(TypedDict):
    ID: int
    name: str
    email: str
    area: str | None


class UserState(rx.State):
    users: list[User] = []
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_user: Optional[User] = None
    user_to_delete: Optional[User] = None
    search_query: str = ""

    @rx.var
    def filtered_users(self) -> list[User]:
        if not self.search_query:
            return self.users
        query = self.search_query.lower()
        return [
            u
            for u in self.users
            if query in u["name"].lower()
            or query in u["email"].lower()
            or (u["area"] and query in u["area"].lower())
        ]

    @rx.event(background=True)
    async def load_users(self):
        async with self:
            self.users = []
        async with rx.asession() as session:
            query = text("SELECT ID, name, email, area FROM user ORDER BY name")
            result = await session.execute(query)
            users_data = [dict(row) for row in result.mappings()]
            async with self:
                self.users = users_data

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def show_add_modal(self):
        self.show_add_dialog = True

    @rx.event
    def close_add_modal(self):
        self.show_add_dialog = False

    @rx.event(background=True)
    async def add_user(self, form_data: dict):
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "INSERT INTO user (name, email, contrasenna, area) VALUES (:name, :email, :contrasenna, :area)"
                )
                await session.execute(
                    query,
                    {
                        "name": form_data["name"],
                        "email": form_data["email"],
                        "contrasenna": form_data["contrasenna"],
                        "area": form_data["area"],
                    },
                )
        async with self:
            yield UserState.close_add_modal
            yield UserState.load_users

    @rx.event
    def show_edit_modal(self, user: User):
        self.editing_user = user
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_user = None

    @rx.event(background=True)
    async def update_user(self, form_data: dict):
        if self.editing_user is None:
            return
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "UPDATE user SET name = :name, email = :email, area = :area WHERE ID = :user_id"
                )
                await session.execute(
                    query,
                    {
                        "name": form_data["name"],
                        "email": form_data["email"],
                        "area": form_data["area"],
                        "user_id": self.editing_user["ID"],
                    },
                )
        async with self:
            yield UserState.close_edit_modal
            yield UserState.load_users

    @rx.event
    def show_delete_confirmation(self, user: User):
        self.user_to_delete = user
        self.show_delete_alert = True

    @rx.event(background=True)
    async def delete_user(self):
        if self.user_to_delete:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM user WHERE ID = :user_id")
                    await session.execute(query, {"user_id": self.user_to_delete["ID"]})
        async with self:
            yield UserState.cancel_delete
            yield UserState.load_users

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.user_to_delete = None