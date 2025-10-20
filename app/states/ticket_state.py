import reflex as rx
from typing import TypedDict, Optional


class Ticket(TypedDict):
    id: int
    folio: str
    solicitante: Optional[str]
    description: str
    responsables: str
    status: str
    fecha_creacion: str
    ra_id: int
    servicio_id: int
    comentarios: str
    foto: Optional[str]
    fechaI: str
    fechaF: Optional[str]


class TicketState(rx.State):
    tickets: list[Ticket] = [
        {
            "id": 1,
            "folio": "IT-RH-001",
            "solicitante": "rhernandez",
            "description": "Necesito instalar la suite de Adobe.",
            "responsables": "rperez",
            "status": "Working",
            "fecha_creacion": "2024-10-01 09:30:00",
            "ra_id": 1,
            "servicio_id": 1,
            "comentarios": "Se requiere licencia.",
            "foto": "uploads/adobe.png",
            "fechaI": "2024-10-01 09:30:00",
            "fechaF": None,
        },
        {
            "id": 2,
            "folio": "FIN-JT-002",
            "solicitante": "jtorres",
            "description": "No tengo acceso a la carpeta de Finanzas.",
            "responsables": "rhernandez",
            "status": "Finish",
            "fecha_creacion": "2024-10-05 11:00:00",
            "ra_id": 5,
            "servicio_id": 3,
            "comentarios": "Permisos asignados.",
            "foto": None,
            "fechaI": "2024-10-05 11:00:00",
            "fechaF": "2024-10-05 12:00:00",
        },
        {
            "id": 3,
            "folio": "IT-AP-003",
            "solicitante": "rperez",
            "description": "Problemas configurando el correo en mi celular.",
            "responsables": "gbaez",
            "status": "Hold",
            "fecha_creacion": "2024-11-10 15:20:00",
            "ra_id": 2,
            "servicio_id": 6,
            "comentarios": "Pendiente de validación de usuario.",
            "foto": None,
            "fechaI": "2024-11-10 15:20:00",
            "fechaF": None,
        },
        {
            "id": 4,
            "folio": "RH-LR-004",
            "solicitante": "lramirez",
            "description": "La impresora de RH no imprime a color.",
            "responsables": "rhernandez",
            "status": "Working",
            "fecha_creacion": "2024-11-15 10:00:00",
            "ra_id": 6,
            "servicio_id": 8,
            "comentarios": "Revisando niveles de tinta.",
            "foto": "uploads/impresora.jpg",
            "fechaI": "2024-11-15 10:00:00",
            "fechaF": None,
        },
        {
            "id": 5,
            "folio": "MKT-DC-005",
            "solicitante": "dcastro",
            "description": "Mi laptop no enciende.",
            "responsables": "rperez",
            "status": "Hold",
            "fecha_creacion": "2024-12-01 08:45:00",
            "ra_id": 7,
            "servicio_id": 4,
            "comentarios": "Posible fallo de hardware.",
            "foto": None,
            "fechaI": "2024-12-01 08:45:00",
            "fechaF": None,
        },
        {
            "id": 6,
            "folio": "PRO-VR-006",
            "solicitante": "vromero",
            "description": "El equipo está muy lento, requiere mantenimiento.",
            "responsables": "gbaez",
            "status": "Finish",
            "fecha_creacion": "2025-01-20 12:00:00",
            "ra_id": 8,
            "servicio_id": 2,
            "comentarios": "Se realizó limpieza y optimización.",
            "foto": None,
            "fechaI": "2025-01-20 12:00:00",
            "fechaF": "2025-01-21 14:00:00",
        },
        {
            "id": 7,
            "folio": "VTA-FN-007",
            "solicitante": "fnavarro",
            "description": "Necesito la última actualización de Windows.",
            "responsables": "rhernandez, rperez",
            "status": "Working",
            "fecha_creacion": "2025-02-15 14:00:00",
            "ra_id": 9,
            "servicio_id": 7,
            "comentarios": "Descargando actualizaciones.",
            "foto": None,
            "fechaI": "2025-02-15 14:00:00",
            "fechaF": None,
        },
        {
            "id": 8,
            "folio": "FIN-SV-008",
            "solicitante": "svega",
            "description": "Solicito respaldo de mi carpeta de Documentos.",
            "responsables": "gbaez",
            "status": "Finish",
            "fecha_creacion": "2025-03-03 13:00:00",
            "ra_id": 10,
            "servicio_id": 5,
            "comentarios": "Respaldo completado en la nube.",
            "foto": "uploads/backup.zip",
            "fechaI": "2025-03-03 13:00:00",
            "fechaF": "2025-03-03 15:30:00",
        },
        {
            "id": 9,
            "folio": "IT-GB-009",
            "solicitante": "gbaez",
            "description": "Creo que tengo un virus, salen pop-ups.",
            "responsables": "rhernandez, gbaez",
            "status": "Hold",
            "fecha_creacion": "2025-04-01 10:10:00",
            "ra_id": 3,
            "servicio_id": 10,
            "comentarios": "Análisis de seguridad en curso.",
            "foto": None,
            "fechaI": "2025-04-01 10:10:00",
            "fechaF": None,
        },
        {
            "id": 10,
            "folio": "VTA-ML-010",
            "solicitante": "mlopez",
            "description": "Necesito capacitación para usar el nuevo CRM.",
            "responsables": "rperez",
            "status": "Working",
            "fecha_creacion": "2025-04-05 16:00:00",
            "ra_id": 4,
            "servicio_id": 9,
            "comentarios": "Sesión programada para el viernes.",
            "foto": None,
            "fechaI": "2025-04-05 16:00:00",
            "fechaF": None,
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
            query = self.search_query.lower()
            tickets = [
                t
                for t in tickets
                if query in t["folio"].lower()
                or (t["solicitante"] and query in t["solicitante"].lower())
                or query in t["responsables"].lower()
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