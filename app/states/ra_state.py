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
            "user_rfc": "rhernandez",
            "dispositivo_nserie": "DELL-LAT-7420-01",
            "fechaA": "2023-01-20",
            "comentarios": "Equipo para líder de IT.",
        },
        {
            "id": 2,
            "user_rfc": "rperez",
            "dispositivo_nserie": "LEN-TP-X1C-03",
            "fechaA": "2023-03-15",
            "comentarios": "Asignado a Ana Perez en IT.",
        },
        {
            "id": 3,
            "user_rfc": "gbaez",
            "dispositivo_nserie": "HP-ED-800-02",
            "fechaA": "2023-02-25",
            "comentarios": "Estación de trabajo para Gerardo Baez.",
        },
        {
            "id": 4,
            "user_rfc": "mlopez",
            "dispositivo_nserie": "AAPL-IP14-04",
            "fechaA": "2023-04-10",
            "comentarios": "Celular corporativo para el área de Ventas.",
        },
        {
            "id": 5,
            "user_rfc": "jtorres",
            "dispositivo_nserie": "SAMS-ODY-G5-05",
            "fechaA": "2023-05-15",
            "comentarios": "Monitor adicional para estación de Finanzas.",
        },
        {
            "id": 6,
            "user_rfc": "lramirez",
            "dispositivo_nserie": "BRO-HL-L2380-06",
            "fechaA": "2023-06-20",
            "comentarios": "Impresora asignada al departamento de RH.",
        },
        {
            "id": 7,
            "user_rfc": "dcastro",
            "dispositivo_nserie": "DELL-XPS-15-07",
            "fechaA": "2023-07-25",
            "comentarios": "Equipo de alto rendimiento para Marketing.",
        },
        {
            "id": 8,
            "user_rfc": "vromero",
            "dispositivo_nserie": "HP-SP-X360-08",
            "fechaA": "2023-08-31",
            "comentarios": "Laptop para Valeria Romero en Producción.",
        },
        {
            "id": 9,
            "user_rfc": "fnavarro",
            "dispositivo_nserie": "LOGI-MXM3-09",
            "fechaA": "2023-09-02",
            "comentarios": "Periféricos para Fernando Navarro.",
        },
        {
            "id": 10,
            "user_rfc": "svega",
            "dispositivo_nserie": "LOGI-MXK-10",
            "fechaA": "2023-09-02",
            "comentarios": "Teclado asignado a Sandra Vega.",
        },
    ]
    users: list[User] = []
    computers: list[Computer] = []
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ra: Optional[RA] = None
    ra_to_delete: Optional[RA] = None
    search_query: str = ""
    next_id: int = 11

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