import reflex as rx
import datetime
from typing import Optional
from app.states.ticket_state import TicketState, Ticket
from app.states.user_state import UserState, User
from app.states.computer_state import ComputerState, Computer
from app.states.service_state import ServiceState
from app.states.ra_state import RAState


class CreateTicketState(rx.State):
    users: list[User] = []
    computers: list[Computer] = []
    services: list[dict] = []
    all_ras: list[dict] = []
    next_ticket_id: int = 11
    is_own_equipment: str = "no"
    selected_requester: str = ""
    photo_filename: str | None = None

    @rx.event
    async def on_load(self):
        """Load initial data."""
        user_state = await self.get_state(UserState)
        computer_state = await self.get_state(ComputerState)
        service_state = await self.get_state(ServiceState)
        ra_state = await self.get_state(RAState)
        self.users = user_state.users
        self.computers = computer_state.computers
        self.services = service_state.services
        self.all_ras = ra_state.ras

    @rx.event
    def set_is_own_equipment(self):
        self.is_own_equipment = "yes" if self.is_own_equipment == "no" else "no"

    @rx.event
    def set_selected_requester(self, requester: str):
        self.selected_requester = requester

    @rx.var
    def filtered_devices(self) -> list[Computer]:
        if self.is_own_equipment == "yes":
            if not self.selected_requester:
                return []
            user_ras = [
                ra for ra in self.all_ras if ra["user_rfc"] == self.selected_requester
            ]
            user_devices_nserie = {ra["dispositivo_nserie"] for ra in user_ras}
            return [c for c in self.computers if c["nserie"] in user_devices_nserie]
        else:
            return [c for c in self.computers if c["tipo"] == "Impresora"]

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if files:
            upload_data = await files[0].read()
            unique_name = f"{datetime.datetime.now().timestamp()}_{files[0].name}"
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / unique_name
            with file_path.open("wb") as f:
                f.write(upload_data)
            self.photo_filename = unique_name

    @rx.event
    async def create_ticket(self, form_data: dict):
        ticket_state = await self.get_state(TicketState)
        new_ticket = Ticket(
            id=ticket_state.next_ticket_id,
            folio=f"IT-NEW-{ticket_state.next_ticket_id}",
            solicitante=form_data.get("solicitante"),
            description=form_data["description"],
            responsables="",
            status="Hold",
            fecha_creacion=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ra_id=int(form_data.get("ra_id", 0)),
            servicio_id=int(form_data.get("servicio_id", 0)),
            comentarios=form_data.get("comentarios", ""),
            foto=self.photo_filename,
            fechaI=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fechaF=None,
        )
        ticket_state.tickets.append(new_ticket)
        ticket_state.next_ticket_id += 1
        self.photo_filename = None
        self.is_own_equipment = form_data.get("is_own_equipment", "no")
        return rx.redirect("/")