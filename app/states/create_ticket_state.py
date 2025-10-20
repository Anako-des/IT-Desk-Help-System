import reflex as rx
import datetime
from typing import Optional
from app.states.ticket_state import TicketState, Ticket
from app.states.user_state import UserState
from app.states.computer_state import ComputerState
from app.states.service_state import ServiceState
from app.states.ra_state import RAState


class CreateTicketState(rx.State):
    users = UserState.users
    computers = ComputerState.computers
    services = ServiceState.services
    ras = RAState.ras
    next_ticket_id: int = 11

    @rx.event
    async def create_ticket(self, form_data: dict):
        ticket_state = await self.get_state(TicketState)
        new_ticket = Ticket(
            id=self.next_ticket_id,
            folio=f"IT-NEW-{self.next_ticket_id}",
            solicitante=form_data.get("solicitante"),
            description=form_data["description"],
            responsables=form_data.get("responsables", ""),
            status="Hold",
            fecha_creacion=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ra_id=int(form_data.get("ra_id", 0)),
            servicio_id=int(form_data.get("servicio_id", 0)),
            comentarios=form_data.get("comentarios", ""),
            foto=None,
            fechaI=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fechaF=None,
        )
        ticket_state.tickets.append(new_ticket)
        self.next_ticket_id += 1
        return rx.redirect("/")