import reflex as rx
from typing import TypedDict, Optional
import datetime


class Ticket(TypedDict):
    id: int
    folio: str
    ra_id: Optional[int]
    service_id: Optional[int]
    description: str
    photo: Optional[str]
    comments: Optional[str]
    dateI: str
    status: str
    dateF: Optional[str]


class TicketState(rx.State):
    tickets: list[Ticket] = [
        {
            "id": 1,
            "folio": "IT-RH-001",
            "ra_id": 1,
            "service_id": 1,
            "description": "Necesito instalar la suite de Adobe.",
            "photo": "/placeholder.svg",
            "comments": "Urgente para proyecto.",
            "dateI": "2024-10-01 09:30:00",
            "status": "Working",
            "dateF": None,
        },
        {
            "id": 2,
            "folio": "FIN-JT-002",
            "ra_id": 5,
            "service_id": 3,
            "description": "No tengo acceso a la carpeta de Finanzas.",
            "photo": None,
            "comments": "Acceso de solo lectura.",
            "dateI": "2024-10-05 11:00:00",
            "status": "Finish",
            "dateF": "2024-10-05 12:00:00",
        },
        {
            "id": 3,
            "folio": "IT-AP-003",
            "ra_id": 2,
            "service_id": 6,
            "description": "Problemas configurando el correo en mi celular.",
            "photo": "/placeholder.svg",
            "comments": "Usuario no recuerda la contraseña.",
            "dateI": "2024-11-10 15:20:00",
            "status": "Hold",
            "dateF": None,
        },
        {
            "id": 4,
            "folio": "RH-LR-004",
            "ra_id": 6,
            "service_id": 8,
            "description": "La impresora de RH no imprime a color.",
            "photo": None,
            "comments": "Revisar niveles de tinta.",
            "dateI": "2024-11-15 10:00:00",
            "status": "Working",
            "dateF": None,
        },
        {
            "id": 5,
            "folio": "MKT-DC-005",
            "ra_id": 7,
            "service_id": 4,
            "description": "Mi laptop no enciende.",
            "photo": "/placeholder.svg",
            "comments": "Posible falla de batería.",
            "dateI": "2024-12-01 08:45:00",
            "status": "Hold",
            "dateF": None,
        },
    ]
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ticket: Optional[Ticket] = None
    ticket_to_delete: Optional[Ticket] = None
    search_query: str = ""
    status_filter: str = "all"
    next_id: int = 6

    @rx.event
    def show_add_modal(self):
        self.show_add_dialog = True

    @rx.event
    def close_add_modal(self):
        self.show_add_dialog = False

    @rx.event
    def add_ticket(self, form_data: dict):
        new_ticket = Ticket(
            id=self.next_id,
            folio=form_data["folio"],
            ra_id=int(form_data.get("ra_id")) if form_data.get("ra_id") else None,
            service_id=int(form_data.get("service_id"))
            if form_data.get("service_id")
            else None,
            description=form_data["description"],
            photo=None,
            comments=form_data.get("comments"),
            dateI=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="Hold",
            dateF=None,
        )
        self.tickets.append(new_ticket)
        self.next_id += 1
        return TicketState.close_add_modal

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status

    @rx.event
    def show_edit_modal(self, ticket: Ticket):
        self.editing_ticket = ticket
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_ticket = None

    @rx.event
    def update_ticket(self, form_data: dict):
        if self.editing_ticket is None:
            return
        ticket_id = self.editing_ticket["id"]
        for i, ticket in enumerate(self.tickets):
            if ticket["id"] == ticket_id:
                self.tickets[i]["description"] = form_data["description"]
                self.tickets[i]["status"] = form_data["status"]
                break
        yield TicketState.close_edit_modal

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
            tickets = [t for t in tickets if t["status"] == self.status_filter]
        if self.search_query:
            query = self.search_query.lower()
            tickets = [
                t
                for t in tickets
                if query in t["folio"].lower()
                or (t["comments"] and query in t["comments"].lower())
                or query in t["description"].lower()
            ]
        return tickets

    @rx.var
    def hold_count(self) -> int:
        return len([t for t in self.tickets if t["status"] == "Hold"])

    @rx.var
    def working_count(self) -> int:
        return len([t for t in self.tickets if t["status"] == "Working"])

    @rx.var
    def finished_count(self) -> int:
        return len([t for t in self.tickets if t["status"] == "Finish"])