import reflex as rx
from typing import TypedDict, Optional
from sqlalchemy import text


class Service(TypedDict):
    ID: int
    nombre: str
    caracteristicas: str
    tipo: str


class ServiceState(rx.State):
    services: list[Service] = []
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_service: Optional[Service] = None
    service_to_delete: Optional[Service] = None
    search_query: str = ""

    @rx.var
    def filtered_services(self) -> list[Service]:
        if not self.search_query:
            return self.services
        query = self.search_query.lower()
        return [
            s
            for s in self.services
            if query in s["nombre"].lower() or query in s["caracteristicas"].lower()
        ]

    @rx.event(background=True)
    async def load_services(self):
        async with self:
            self.services = []
        async with rx.asession() as session:
            query = text(
                "SELECT ID, nombre, caracteristicas, tipo FROM Servicios ORDER BY nombre"
            )
            result = await session.execute(query)
            services_data = [dict(row) for row in result.mappings()]
            async with self:
                self.services = services_data

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def show_add_modal(self):
        self.show_add_dialog = True

    @rx.event
    def close_add_modal(self):
        self.show_add_dialog = False

    @rx.event(background=True)
    async def add_service(self, form_data: dict):
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "INSERT INTO Servicios (nombre, caracteristicas, tipo) VALUES (:nombre, :caracteristicas, :tipo)"
                )
                await session.execute(query, form_data)
        async with self:
            yield ServiceState.close_add_modal
            yield ServiceState.load_services

    @rx.event
    def show_edit_modal(self, service: Service):
        self.editing_service = service
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_service = None

    @rx.event(background=True)
    async def update_service(self, form_data: dict):
        if self.editing_service is None:
            return
        async with rx.asession() as session:
            async with session.begin():
                query = text(
                    "UPDATE Servicios SET nombre = :nombre, caracteristicas = :caracteristicas, tipo = :tipo WHERE ID = :service_id"
                )
                await session.execute(
                    query,
                    {
                        "nombre": form_data["nombre"],
                        "caracteristicas": form_data["caracteristicas"],
                        "tipo": form_data["tipo"],
                        "service_id": self.editing_service["ID"],
                    },
                )
        async with self:
            yield ServiceState.close_edit_modal
            yield ServiceState.load_services

    @rx.event
    def show_delete_confirmation(self, service: Service):
        self.service_to_delete = service
        self.show_delete_alert = True

    @rx.event(background=True)
    async def delete_service(self):
        if self.service_to_delete:
            async with rx.asession() as session:
                async with session.begin():
                    query = text("DELETE FROM Servicios WHERE ID = :service_id")
                    await session.execute(
                        query, {"service_id": self.service_to_delete["ID"]}
                    )
        async with self:
            yield ServiceState.cancel_delete
            yield ServiceState.load_services

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.service_to_delete = None