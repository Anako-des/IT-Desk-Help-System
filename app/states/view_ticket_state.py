import reflex as rx
from typing import TypedDict, Optional
from app.states.ticket_state import Ticket, TicketState


class VistaDetalladaTicket(TypedDict):
    folio: str
    ra_id: int
    servicio_id: int
    descripcion: str
    comentarios: Optional[str]
    fechaI: str
    estado: str
    fechaF: Optional[str]
    foto: Optional[str]
    solicitante_nombre: Optional[str]
    dispositivo_nombre: Optional[str]
    servicio_nombre: Optional[str]


class ViewTicketState(TicketState):
    show_detail_modal: bool = False
    selected_ticket_details: Optional[VistaDetalladaTicket] = None

    @rx.var
    def tickets_for_view(self) -> list[Ticket]:
        return self.tickets

    @rx.event
    async def show_ticket_details(self, ticket: Ticket):
        from app.states.user_state import UserState
        from app.states.computer_state import ComputerState
        from app.states.service_state import ServiceState

        user_state = await self.get_state(UserState)
        computer_state = await self.get_state(ComputerState)
        service_state = await self.get_state(ServiceState)
        solicitante = next(
            (u for u in user_state.users if u["userName"] == ticket["solicitante"]),
            None,
        )
        dispositivo = next(
            (c for c in computer_state.computers if c["id"] == ticket["ra_id"]), None
        )
        servicio = next(
            (s for s in service_state.services if s["id"] == ticket["servicio_id"]),
            None,
        )
        details = VistaDetalladaTicket(
            folio=ticket["folio"],
            ra_id=ticket["ra_id"],
            servicio_id=ticket["servicio_id"],
            descripcion=ticket["description"],
            comentarios=ticket["comentarios"],
            fechaI=ticket["fechaI"],
            estado=ticket["status"],
            fechaF=ticket["fechaF"],
            foto=ticket["foto"],
            solicitante_nombre=solicitante["name"] if solicitante else "N/A",
            dispositivo_nombre=dispositivo["name"] if dispositivo else "N/A",
            servicio_nombre=servicio["nombre"] if servicio else "N/A",
        )
        self.selected_ticket_details = details
        self.show_detail_modal = True

    @rx.event
    def close_detail_modal(self):
        self.show_detail_modal = False
        self.selected_ticket_details = None

    @rx.event
    async def delete_ticket_from_view(self, ticket: Ticket):
        ticket_state = await self.get_state(TicketState)
        ticket_state.tickets = [
            t for t in ticket_state.tickets if t["id"] != ticket["id"]
        ]