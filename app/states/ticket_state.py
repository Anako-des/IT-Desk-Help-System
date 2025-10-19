import reflex as rx
from typing import TypedDict, Optional


class Ticket(TypedDict):
    id: int
    folio: str
    ra_id: int
    servicio_id: int
    descripcion: str
    comentarios: str
    fechaI: str
    estado: str
    fechaF: Optional[str]


class TicketState(rx.State):
    tickets: list[Ticket] = [
        {
            "id": 1,
            "folio": "IT-RH-001",
            "ra_id": 1,
            "servicio_id": 1,
            "descripcion": "Necesito instalar la suite de Adobe.",
            "comentarios": "Urgente para proyecto de diseño.",
            "fechaI": "2024-10-01 09:30:00",
            "estado": "Working",
            "fechaF": None,
        },
        {
            "id": 2,
            "folio": "FIN-JT-002",
            "ra_id": 5,
            "servicio_id": 3,
            "descripcion": "No tengo acceso a la carpeta de Finanzas.",
            "comentarios": "Acceso concedido.",
            "fechaI": "2024-10-05 11:00:00",
            "estado": "Finish",
            "fechaF": "2024-10-05 12:00:00",
        },
        {
            "id": 3,
            "folio": "IT-AP-003",
            "ra_id": 2,
            "servicio_id": 6,
            "descripcion": "Problemas configurando el correo en mi celular.",
            "comentarios": "En espera de que el usuario traiga el dispositivo.",
            "fechaI": "2024-11-10 15:20:00",
            "estado": "Hold",
            "fechaF": None,
        },
        {
            "id": 4,
            "folio": "RH-LR-004",
            "ra_id": 6,
            "servicio_id": 8,
            "descripcion": "La impresora de RH no imprime a color.",
            "comentarios": "Se está revisando el nivel de tinta.",
            "fechaI": "2024-11-15 10:00:00",
            "estado": "Working",
            "fechaF": None,
        },
        {
            "id": 5,
            "folio": "MKT-DC-005",
            "ra_id": 7,
            "servicio_id": 4,
            "descripcion": "Mi laptop no enciende.",
            "comentarios": "Pendiente de diagnóstico.",
            "fechaI": "2024-12-01 08:45:00",
            "estado": "Hold",
            "fechaF": None,
        },
    ]
    show_see_dialog: bool = False
    show_delete_alert: bool = False
    ticket_to_see: Optional[Ticket] = None
    ticket_to_delete: Optional[Ticket] = None
    search_query: str = ""
    status_filter: str = "all"

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def show_see_modal(self, ticket: Ticket):
        self.ticket_to_see = ticket
        self.show_see_dialog = True

    @rx.event
    def close_see_modal(self):
        self.show_see_dialog = False
        self.ticket_to_see = None

    @rx.event
    def show_delete_confirmation(self, ticket: Ticket):
        self.ticket_to_delete = ticket
        self.show_delete_alert = True

    @rx.event
    def delete_ticket(self):
        if self.ticket_to_delete:
            self.tickets = [
                t for t in self.tickets if t["id"] != self.ticket_to_delete["id"]
            ]
        yield TicketState.cancel_delete

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.ticket_to_delete = None

    @rx.event
    def set_show_delete_alert(self, value: bool):
        self.show_delete_alert = value
        if not value:
            self.ticket_to_delete = None

    @rx.var
    def filtered_tickets(self) -> list[Ticket]:
        tickets = self.tickets
        if self.status_filter != "all":
            tickets = [t for t in tickets if t["estado"] == self.status_filter]
        if self.search_query:
            query = self.search_query.lower()
            tickets = [
                t
                for t in tickets
                if query in t["folio"].lower()
                or query in t["descripcion"].lower()
                or query in t["comentarios"].lower()
            ]
        return tickets

    @rx.var
    def hold_count(self) -> int:
        return len([t for t in self.tickets if t["estado"] == "Hold"])

    @rx.var
    def working_count(self) -> int:
        return len([t for t in self.tickets if t["estado"] == "Working"])

    @rx.var
    def finished_count(self) -> int:
        return len([t for t in self.tickets if t["estado"] == "Finish"])