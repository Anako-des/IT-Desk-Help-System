import reflex as rx
from typing import Optional
from app.states.user_state import User
from sqlalchemy import text


class AuthState(rx.State):
    error_message: str = ""
    user: Optional[User] = None
    is_admin: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return self.user is not None

    @rx.event
    async def login(self, form_data: dict):
        """
        Handles user login by checking credentials against the database.
        - Admin: jhernandez / 123456789 (hardcoded)
        - DB User: email from 'user' table and 'contrasenna' field
        """
        self.error_message = ""
        email = form_data.get("username", "").strip()
        password = form_data.get("password", "")
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        if email == "jhernandez" and password == "123456789":
            self.user = User(
                ID=0, name="Admin User", email="jhernandez@example.com", area="IT"
            )
            self.is_admin = True
            return rx.redirect("/")
        async with rx.asession() as session:
            query = text(
                "SELECT ID, name, email, contrasenna, area FROM user WHERE email = :email"
            )
            result = await session.execute(query, {"email": email})
            db_user = result.first()
            if db_user and db_user.contrasenna == password:
                self.user = User(
                    ID=db_user.ID,
                    name=db_user.name,
                    email=db_user.email,
                    area=db_user.area,
                )
                self.is_admin = False
                return rx.redirect("/")
            else:
                self.error_message = "Invalid email or password."

    @rx.event
    def logout(self):
        self.user = None
        self.is_admin = False
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")