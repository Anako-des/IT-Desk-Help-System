import reflex as rx
from typing import Optional, TypedDict
from app.states.user_state import User


class AuthState(rx.State):
    error_message: str = ""
    user: Optional[User] = None
    is_admin: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user is not None

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "")
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        if username == "jhernandez" and password == "123456789":
            self.user = User(
                id=0,
                rfc="ADMIN",
                name="Admin User",
                email="jhernandez@example.com",
                puesto="Administrator",
            )
            self.is_admin = True
            return rx.redirect("/")
        elif password == "123456789":
            from app.states.user_state import UserState

            all_users = UserState.users
            found_user = next((u for u in all_users if u["email"] == username), None)
            if found_user:
                self.user = found_user
                self.is_admin = False
                return rx.redirect("/")
            else:
                self.error_message = "Invalid credentials."
        else:
            self.error_message = "Invalid credentials."

    @rx.event
    def logout(self):
        self.user = None
        self.is_admin = False
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")