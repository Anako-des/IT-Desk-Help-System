import reflex as rx
from typing import TypedDict, Optional
from sqlalchemy import text


class Ticket(TypedDict):
    ID: int
    folio: str
    description: str
    status: str


class TicketState(rx.State):
    tickets: list[Ticket] = []
    user_tickets: list[Ticket] = []
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_ticket: Optional[Ticket] = None
    ticket_to_delete: Optional[Ticket] = None
    search_query: str = ""
    status_filter: str = "all"

    @rx.event(background=True)
    async def load_tickets(self):
        async with self:
            self.tickets = []
        async with rx.asession() as session:
            query = text(
                "SELECT ID, folio, descripcion, estado as status FROM Ticket ORDER BY fechaI DESC"
            )
            result = await session.execute(query)
            tickets_data = [dict(row) for row in result.mappings()]
            async with self:
                self.tickets = tickets_data

    @rx.event(background=True)
    async def load_user_tickets(self, user_id: int):
        async with self:
            self.user_tickets = []
        async with rx.asession() as session:
            query = text("""
                SELECT t.ID, t.folio, t.descripcion, t.estado as status 
                FROM Ticket t 
                JOIN RA ra ON t.ra_id = ra.ID 
                WHERE ra.user_id = :user_id 
                ORDER BY t.fechaI DESC
                """)
            result = await session.execute(query, {"user_id": user_id})
            tickets_data = [dict(row) for row in result.mappings()]
            async with self:
                self.user_tickets = tickets_data

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

    @rx.event(background=True)
    async def update_ticket(self, form_data: dict):
        if self.editing_ticket is None:
            return
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "UPDATE Ticket SET descripcion = :description, estado = :status WHERE ID = :ticket_id"
                )
                await session.execute(
                    query,
                    {
                        "description": form_data["description"],
                        "status": form_data["status"],
                        "ticket_id": self.editing_ticket["ID"],
                    },
                )
        async with self:
            yield TicketState.close_edit_modal
            yield TicketState.load_tickets

    @rx.event
    def show_delete_confirmation(self, ticket: Ticket):
        self.ticket_to_delete = ticket
        self.show_delete_alert = True

    @rx.event(background=True)
    async def delete_ticket(self):
        if self.ticket_to_delete:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM Ticket WHERE ID = :ticket_id")
                    await session.execute(
                        query, {"ticket_id": self.ticket_to_delete["ID"]}
                    )
        async with self:
            yield TicketState.cancel_delete
            yield TicketState.load_tickets

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
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