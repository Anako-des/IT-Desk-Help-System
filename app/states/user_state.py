import reflex as rx
from typing import TypedDict, Optional


class User(TypedDict):
    userName: str
    name: str
    email: str
    contrasenna: str
    area: str


class UserState(rx.State):
    users: list[User] = [
        {
            "userName": "johndoe",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "contrasenna": "pass123",
            "area": "Development",
        },
        {
            "userName": "janesmith",
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "contrasenna": "pass456",
            "area": "Design",
        },
        {
            "userName": "peterjones",
            "name": "Peter Jones",
            "email": "peter.jones@example.com",
            "contrasenna": "pass789",
            "area": "Management",
        },
    ]
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
        return [
            u
            for u in self.users
            if self.search_query.lower() in u["name"].lower()
            or self.search_query.lower() in u["email"].lower()
            or self.search_query.lower() in u["userName"].lower()
        ]

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def show_add_modal(self):
        self.show_add_dialog = True

    @rx.event
    def close_add_modal(self):
        self.show_add_dialog = False

    @rx.event
    def add_user(self, form_data: dict):
        new_user = User(
            userName=form_data["userName"],
            name=form_data["name"],
            email=form_data["email"],
            contrasenna=form_data["contrasenna"],
            area=form_data["area"],
        )
        self.users.append(new_user)
        return UserState.close_add_modal

    @rx.event
    def show_edit_modal(self, user: User):
        self.editing_user = user
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_user = None

    @rx.event
    def update_user(self, form_data: dict):
        if self.editing_user is None:
            return
        username = self.editing_user["userName"]
        for i, user in enumerate(self.users):
            if user["userName"] == username:
                self.users[i]["userName"] = form_data["userName"]
                self.users[i]["name"] = form_data["name"]
                self.users[i]["email"] = form_data["email"]
                self.users[i]["area"] = form_data["area"]
                if form_data.get("contrasenna"):
                    self.users[i]["contrasenna"] = form_data["contrasenna"]
                break
        return UserState.close_edit_modal

    @rx.event
    def show_delete_confirmation(self, user: User):
        self.user_to_delete = user
        self.show_delete_alert = True

    @rx.event
    def delete_user(self):
        if self.user_to_delete:
            self.users = [
                u
                for u in self.users
                if u["userName"] != self.user_to_delete["userName"]
            ]
        return UserState.cancel_delete

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.user_to_delete = None

    @rx.event
    def set_show_delete_alert(self, value: bool):
        self.show_delete_alert = value
        if not value:
            self.user_to_delete = None