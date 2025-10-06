import reflex as rx
from typing import TypedDict, Optional
from sqlalchemy import text
from app.states.user_state import User
from app.states.computer_state import Computer


class RA(TypedDict):
    ID: int
    user_id: int
    dispositivo_nserie: str
    fechaA: str
    comentarios: str
    user_name: str
    dispositivo_name: str


class RAState(rx.State):
    ras: list[RA] = []
    users: list[User] = []
    computers: list[Computer] = []
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ra: Optional[RA] = None
    ra_to_delete: Optional[RA] = None
    search_query: str = ""

    @rx.var
    def filtered_ras(self) -> list[RA]:
        if not self.search_query:
            return self.ras
        query = self.search_query.lower()
        return [
            r
            for r in self.ras
            if query in r["user_name"].lower()
            or query in r["dispositivo_nserie"].lower()
            or query in r["dispositivo_name"].lower()
            or (query in r["comentarios"].lower())
        ]

    @rx.event(background=True)
    async def load_all_data(self):
        async with self:
            self.ras = []
            self.users = []
            self.computers = []
        async with rx.asession() as session:
            ra_query = text("""
                SELECT RA.ID, RA.user_id, RA.dispositivo_nserie, DATE_FORMAT(RA.fechaA, '%Y-%m-%d') as fechaA, 
                RA.comentarios, user.name as user_name, Dispositivos.name as dispositivo_name 
                FROM RA 
                JOIN user ON RA.user_id = user.ID 
                JOIN Dispositivos ON RA.dispositivo_nserie = Dispositivos.nserie 
                ORDER BY RA.fechaA DESC
                """)
            ra_result = await session.execute(ra_query)
            ra_data = [dict(row) for row in ra_result.mappings()]
            user_query = text("SELECT ID, name, email, area FROM user ORDER BY name")
            user_result = await session.execute(user_query)
            user_data = [dict(row) for row in user_result.mappings()]
            computer_query = text("SELECT nserie, name FROM Dispositivos ORDER BY name")
            computer_result = await session.execute(computer_query)
            computer_data = [dict(row) for row in computer_result.mappings()]
            async with self:
                self.ras = ra_data
                self.users = user_data
                self.computers = computer_data

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
    async def add_ra(self, form_data: dict):
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "INSERT INTO RA (user_id, dispositivo_nserie, fechaA, comentarios) VALUES (:user_id, :dispositivo_nserie, CURDATE(), :comentarios)"
                )
                await session.execute(query, form_data)
        async with self:
            yield RAState.close_add_modal
            yield RAState.load_all_data

    @rx.event
    def show_edit_modal(self, ra: RA):
        self.editing_ra = ra
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_ra = None

    @rx.event(background=True)
    async def update_ra(self, form_data: dict):
        if self.editing_ra is None:
            return
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "UPDATE RA SET user_id = :user_id, dispositivo_nserie = :dispositivo_nserie, comentarios = :comentarios WHERE ID = :ra_id"
                )
                await session.execute(
                    query,
                    {
                        "user_id": form_data["user_id"],
                        "dispositivo_nserie": form_data["dispositivo_nserie"],
                        "comentarios": form_data["comentarios"],
                        "ra_id": self.editing_ra["ID"],
                    },
                )
        async with self:
            yield RAState.close_edit_modal
            yield RAState.load_all_data

    @rx.event
    def show_delete_confirmation(self, ra: RA):
        self.ra_to_delete = ra
        self.show_delete_alert = True

    @rx.event(background=True)
    async def delete_ra(self):
        if self.ra_to_delete:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM RA WHERE ID = :ra_id")
                    await session.execute(query, {"ra_id": self.ra_to_delete["ID"]})
        async with self:
            yield RAState.cancel_delete
            yield RAState.load_all_data

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.ra_to_delete = None