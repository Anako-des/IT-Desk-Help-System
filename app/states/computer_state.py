import reflex as rx
from typing import TypedDict, Optional
import datetime


class Computer(TypedDict):
    id: int
    nserie: str
    name: str
    marca: str
    fechaS: str


class ComputerState(rx.State):
    computers: list[Computer] = [
        {
            "id": 1,
            "nserie": "SN12345",
            "name": "Laptop Pro",
            "marca": "BrandA",
            "fechaS": "2023-01-15",
        },
        {
            "id": 2,
            "nserie": "SN67890",
            "name": "Desktop 5000",
            "marca": "BrandB",
            "fechaS": "2022-11-20",
        },
        {
            "id": 3,
            "nserie": "SN54321",
            "name": "Ultrabook Flex",
            "marca": "BrandA",
            "fechaS": "2023-05-10",
        },
    ]
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_computer: Optional[Computer] = None
    computer_to_delete: Optional[Computer] = None
    search_query: str = ""
    next_id: int = 4

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
    def add_computer(self, form_data: dict):
        new_computer = Computer(
            id=self.next_id,
            nserie=form_data["nserie"],
            name=form_data["name"],
            marca=form_data["marca"],
            fechaS=datetime.date.today().isoformat(),
        )
        self.computers.append(new_computer)
        self.next_id += 1
        return ComputerState.close_add_modal

    @rx.event
    def show_edit_modal(self, computer: Computer):
        self.editing_computer = computer
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_computer = None

    @rx.event
    def update_computer(self, form_data: dict):
        if self.editing_computer is None:
            return
        computer_id = self.editing_computer["id"]
        for i, computer in enumerate(self.computers):
            if computer["id"] == computer_id:
                self.computers[i]["nserie"] = form_data["nserie"]
                self.computers[i]["name"] = form_data["name"]
                self.computers[i]["marca"] = form_data["marca"]
                break
        return ComputerState.close_edit_modal

    @rx.event
    def show_delete_confirmation(self, computer: Computer):
        self.computer_to_delete = computer
        self.show_delete_alert = True

    @rx.event
    def delete_computer(self):
        if self.computer_to_delete:
            self.computers = [
                c for c in self.computers if c["id"] != self.computer_to_delete["id"]
            ]
        return ComputerState.cancel_delete

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.computer_to_delete = None

    @rx.event
    def set_show_delete_alert(self, value: bool):
        self.show_delete_alert = value
        if not value:
            self.computer_to_delete = None