import reflex as rx
from typing import TypedDict, Optional


class Ticket(TypedDict):
    id: int
    folio: str
    description: str
    status: str


class TicketState(rx.State):
    tickets: list[Ticket] = [
        {
            "id": 1,
            "folio": "T2024-001",
            "description": "Printer not working",
            "status": "Hold",
        },
        {
            "id": 2,
            "folio": "T2024-002",
            "description": "Cannot connect to WiFi",
            "status": "Working",
        },
        {
            "id": 3,
            "folio": "T2024-003",
            "description": "Software installation request",
            "status": "Hold",
        },
        {
            "id": 4,
            "folio": "T2024-004",
            "description": "Email configuration issue",
            "status": "Finish",
        },
        {
            "id": 5,
            "folio": "T2024-005",
            "description": "Password reset",
            "status": "Working",
        },
        {
            "id": 6,
            "folio": "T2024-006",
            "description": "Blue screen error",
            "status": "Finish",
        },
        {
            "id": 7,
            "folio": "T2024-007",
            "description": "Request for a new mouse",
            "status": "Hold",
        },
    ]
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ticket: Optional[Ticket] = None
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
            tickets = [
                t for t in tickets if self.search_query.lower() in t["folio"].lower()
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