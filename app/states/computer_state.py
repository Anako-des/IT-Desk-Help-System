import reflex as rx
from typing import TypedDict, Optional
from sqlalchemy import text
import datetime


class Computer(TypedDict):
    nserie: str
    name: str
    marca: str
    fechaS: str
    tipo: str


class ComputerState(rx.State):
    computers: list[Computer] = []
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_computer: Optional[Computer] = None
    computer_to_delete: Optional[Computer] = None
    search_query: str = ""

    @rx.var
    def filtered_computers(self) -> list[Computer]:
        if not self.search_query:
            return self.computers
        return [
            c
            for c in self.computers
            if self.search_query.lower() in c["name"].lower()
            or self.search_query.lower() in c["marca"].lower()
            or self.search_query.lower() in c["nserie"].lower()
        ]

    @rx.event(background=True)
    async def load_computers(self):
        async with self:
            self.computers = []
        async with rx.asession() as session:
            query = text(
                "SELECT nserie, name, marca, DATE_FORMAT(fechaS, '%Y-%m-%d') as fechaS, tipo FROM Dispositivos ORDER BY name"
            )
            result = await session.execute(query)
            computers_data = [dict(row) for row in result.mappings()]
            async with self:
                self.computers = computers_data

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
    async def add_computer(self, form_data: dict):
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "INSERT INTO Dispositivos (nserie, name, marca, fechaS, tipo) VALUES (:nserie, :name, :marca, CURDATE(), :tipo)"
                )
                await session.execute(
                    query,
                    {
                        "nserie": form_data["nserie"],
                        "name": form_data["name"],
                        "marca": form_data["marca"],
                        "tipo": form_data["tipo"],
                    },
                )
        async with self:
            yield ComputerState.close_add_modal
            yield ComputerState.load_computers

    @rx.event
    def show_edit_modal(self, computer: Computer):
        self.editing_computer = computer
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_computer = None

    @rx.event(background=True)
    async def update_computer(self, form_data: dict):
        if self.editing_computer is None:
            return
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "UPDATE Dispositivos SET name = :name, marca = :marca, tipo = :tipo WHERE nserie = :nserie"
                )
                await session.execute(
                    query,
                    {
                        "name": form_data["name"],
                        "marca": form_data["marca"],
                        "tipo": form_data["tipo"],
                        "nserie": self.editing_computer["nserie"],
                    },
                )
        async with self:
            yield ComputerState.close_edit_modal
            yield ComputerState.load_computers

    @rx.event
    def show_delete_confirmation(self, computer: Computer):
        self.computer_to_delete = computer
        self.show_delete_alert = True

    @rx.event(background=True)
    async def delete_computer(self):
        if self.computer_to_delete:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM Dispositivos WHERE nserie = :nserie")
                    await session.execute(
                        query, {"nserie": self.computer_to_delete["nserie"]}
                    )
        async with self:
            yield ComputerState.cancel_delete
            yield ComputerState.load_computers

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.computer_to_delete = None