import reflex as rx
from typing import TypedDict, Optional
import datetime
from app.states.user_state import User
from app.states.computer_state import Computer


class RA(TypedDict):
    id: int
    user_rfc: str
    dispositivo_nserie: str
    fechaA: str
    comentarios: str


class RAState(rx.State):
    ras: list[RA] = [
        {
            "id": 1,
            "user_rfc": "ABCD123456XYZ",
            "dispositivo_nserie": "SN12345",
            "fechaA": "2023-02-01",
            "comentarios": "Initial assignment",
        },
        {
            "id": 2,
            "user_rfc": "EFGH789012ABC",
            "dispositivo_nserie": "SN67890",
            "fechaA": "2023-03-15",
            "comentarios": "Loaner device",
        },
    ]
    users: list[User] = [
        {
            "id": 1,
            "rfc": "ABCD123456XYZ",
            "name": "John Doe",
            "email": "john.doe@example.com",
            "puesto": "Developer",
        },
        {
            "id": 2,
            "rfc": "EFGH789012ABC",
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "puesto": "Designer",
        },
        {
            "id": 3,
            "rfc": "IJKL345678DEF",
            "name": "Peter Jones",
            "email": "peter.jones@example.com",
            "puesto": "Project Manager",
        },
    ]
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
    ]
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ra: Optional[RA] = None
    ra_to_delete: Optional[RA] = None
    search_query: str = ""
    next_id: int = 3

    @rx.var
    def filtered_ras(self) -> list[RA]:
        """This computed var filters the RA list based on the search query.
        In a database-backed app, this filtering would happen in the SQL query.
        SQL Query (example): SELECT * FROM RA WHERE user_rfc LIKE '%query%' OR dispositivo_nserie LIKE '%query%'
        """
        if not self.search_query:
            return self.ras
        return [
            r
            for r in self.ras
            if self.search_query.lower() in r["user_rfc"].lower()
            or self.search_query.lower() in r["dispositivo_nserie"].lower()
            or self.search_query.lower() in r["comentarios"].lower()
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
    def add_ra(self, form_data: dict):
        """Adds a new RA record.
        SQL Query: INSERT INTO RA (user_rfc, dispositivo_nserie, fechaA, comentarios) VALUES (...);
        """
        new_ra = RA(
            id=self.next_id,
            user_rfc=form_data["user_rfc"],
            dispositivo_nserie=form_data["dispositivo_nserie"],
            comentarios=form_data["comentarios"],
            fechaA=datetime.date.today().isoformat(),
        )
        self.ras.append(new_ra)
        self.next_id += 1
        return RAState.close_add_modal

    @rx.event
    def show_edit_modal(self, ra: RA):
        self.editing_ra = ra
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_ra = None

    @rx.event
    def update_ra(self, form_data: dict):
        """Updates an existing RA record.
        SQL Query: UPDATE RA SET user_rfc = ..., dispositivo_nserie = ..., comentarios = ... WHERE ID = ...;
        """
        if self.editing_ra is None:
            return
        ra_id = self.editing_ra["id"]
        for i, ra in enumerate(self.ras):
            if ra["id"] == ra_id:
                self.ras[i]["user_rfc"] = form_data["user_rfc"]
                self.ras[i]["dispositivo_nserie"] = form_data["dispositivo_nserie"]
                self.ras[i]["comentarios"] = form_data["comentarios"]
                break
        return RAState.close_edit_modal

    @rx.event
    def show_delete_confirmation(self, ra: RA):
        self.ra_to_delete = ra
        self.show_delete_alert = True

    @rx.event
    def delete_ra(self):
        """Deletes an RA record.
        SQL Query: DELETE FROM RA WHERE ID = ...;
        """
        if self.ra_to_delete:
            self.ras = [r for r in self.ras if r["id"] != self.ra_to_delete["id"]]
        return RAState.cancel_delete

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.ra_to_delete = None