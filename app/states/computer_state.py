import reflex as rx
from typing import TypedDict, Optional
import datetime


class Computer(TypedDict):
    id: int
    nserie: str
    name: str
    marca: str
    fechaS: str
    tipo: str


class ComputerState(rx.State):
    computers: list[Computer] = [
        {
            "id": 1,
            "nserie": "DELL-LAT-7420-01",
            "name": "Latitude 7420",
            "marca": "Dell",
            "fechaS": "2023-01-15",
            "tipo": "Laptop",
        },
        {
            "id": 2,
            "nserie": "HP-ED-800-02",
            "name": "EliteDesk 800 G6",
            "marca": "HP",
            "fechaS": "2023-02-20",
            "tipo": "PC",
        },
        {
            "id": 3,
            "nserie": "LEN-TP-X1C-03",
            "name": "ThinkPad X1 Carbon",
            "marca": "Lenovo",
            "fechaS": "2023-03-10",
            "tipo": "Laptop",
        },
        {
            "id": 4,
            "nserie": "AAPL-IP14-04",
            "name": "iPhone 14 Pro",
            "marca": "Apple",
            "fechaS": "2023-04-05",
            "tipo": "Celular",
        },
        {
            "id": 5,
            "nserie": "SAMS-ODY-G5-05",
            "name": "Monitor Odyssey G5",
            "marca": "Samsung",
            "fechaS": "2023-05-12",
            "tipo": "Monitor",
        },
        {
            "id": 6,
            "nserie": "BRO-HL-L2380-06",
            "name": "HL-L2380DW",
            "marca": "Brother",
            "fechaS": "2023-06-18",
            "tipo": "Impresora",
        },
        {
            "id": 7,
            "nserie": "DELL-XPS-15-07",
            "name": "XPS 15 9520",
            "marca": "Dell",
            "fechaS": "2023-07-22",
            "tipo": "Laptop",
        },
        {
            "id": 8,
            "nserie": "HP-SP-X360-08",
            "name": "Spectre x360",
            "marca": "HP",
            "fechaS": "2023-08-30",
            "tipo": "Laptop",
        },
        {
            "id": 9,
            "nserie": "LOGI-MXM3-09",
            "name": "MX Master 3",
            "marca": "Logitech",
            "fechaS": "2023-09-01",
            "tipo": "Mouse",
        },
        {
            "id": 10,
            "nserie": "LOGI-MXK-10",
            "name": "MX Keys",
            "marca": "Logitech",
            "fechaS": "2023-09-01",
            "tipo": "Teclado",
        },
    ]
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_computer: Optional[Computer] = None
    computer_to_delete: Optional[Computer] = None
    search_query: str = ""
    next_id: int = 11

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
            tipo=form_data["tipo"],
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
                self.computers[i]["tipo"] = form_data["tipo"]
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