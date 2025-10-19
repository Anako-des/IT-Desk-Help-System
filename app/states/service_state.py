import reflex as rx
from typing import TypedDict, Optional


class Service(TypedDict):
    id: int
    nombre: str
    caracteristicas: str
    tipo: str


class ServiceState(rx.State):
    services: list[Service] = [
        {
            "id": 1,
            "nombre": "Instalación de Software",
            "caracteristicas": "Instalación y configuración de aplicaciones de software.",
            "tipo": "Software",
        },
        {
            "id": 2,
            "nombre": "Mantenimiento Preventivo",
            "caracteristicas": "Limpieza y revisión de componentes de hardware.",
            "tipo": "Hardware",
        },
        {
            "id": 3,
            "nombre": "Soporte de Red",
            "caracteristicas": "Resolución de problemas de conectividad a la red.",
            "tipo": "Redes",
        },
        {
            "id": 4,
            "nombre": "Reparación de Hardware",
            "caracteristicas": "Diagnóstico y reparación de componentes físicos.",
            "tipo": "Hardware",
        },
        {
            "id": 5,
            "nombre": "Respaldo de Información",
            "caracteristicas": "Creación de copias de seguridad de datos importantes.",
            "tipo": "Datos",
        },
        {
            "id": 6,
            "nombre": "Configuración de Correo",
            "caracteristicas": "Soporte para cuentas de correo electrónico.",
            "tipo": "Software",
        },
        {
            "id": 7,
            "nombre": "Actualización de Sistema",
            "caracteristicas": "Instalación de actualizaciones de sistema operativo.",
            "tipo": "Software",
        },
        {
            "id": 8,
            "nombre": "Soporte para Impresoras",
            "caracteristicas": "Resolución de problemas relacionados con impresoras.",
            "tipo": "Hardware",
        },
        {
            "id": 9,
            "nombre": "Capacitación de Usuario",
            "caracteristicas": "Entrenamiento sobre el uso de nuevo software o hardware.",
            "tipo": "Capacitación",
        },
        {
            "id": 10,
            "nombre": "Gestión de Antivirus",
            "caracteristicas": "Instalación y actualización de software de seguridad.",
            "tipo": "Seguridad",
        },
    ]
    show_add_dialog: bool = False
    show_edit_dialog: bool = False
    show_delete_alert: bool = False
    editing_service: Optional[Service] = None
    service_to_delete: Optional[Service] = None
    search_query: str = ""
    next_id: int = 11

    @rx.var
    def filtered_services(self) -> list[Service]:
        """This computed var filters the service list based on the search query.
        In a database-backed app, this filtering would happen in the SQL query.
        SQL Query (example): SELECT * FROM Servicios WHERE nombre LIKE '%query%' OR caracteristicas LIKE '%query%'
        """
        if not self.search_query:
            return self.services
        return [
            s
            for s in self.services
            if self.search_query.lower() in s["nombre"].lower()
            or self.search_query.lower() in s["caracteristicas"].lower()
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
    def add_service(self, form_data: dict):
        """Adds a new service record.
        SQL Query: INSERT INTO Servicios (nombre, caracteristicas, tipo_id) VALUES (...);
        """
        new_service = Service(
            id=self.next_id,
            nombre=form_data["nombre"],
            caracteristicas=form_data["caracteristicas"],
            tipo=form_data["tipo"],
        )
        self.services.append(new_service)
        self.next_id += 1
        return ServiceState.close_add_modal

    @rx.event
    def show_edit_modal(self, service: Service):
        self.editing_service = service
        self.show_edit_dialog = True

    @rx.event
    def close_edit_modal(self):
        self.show_edit_dialog = False
        self.editing_service = None

    @rx.event
    def update_service(self, form_data: dict):
        """Updates an existing service record.
        SQL Query: UPDATE Servicios SET nombre = ..., caracteristicas = ..., tipo_id = ... WHERE ID = ...;
        """
        if self.editing_service is None:
            return
        service_id = self.editing_service["id"]
        for i, service in enumerate(self.services):
            if service["id"] == service_id:
                self.services[i]["nombre"] = form_data["nombre"]
                self.services[i]["caracteristicas"] = form_data["caracteristicas"]
                self.services[i]["tipo"] = form_data["tipo"]
                break
        return ServiceState.close_edit_modal

    @rx.event
    def show_delete_confirmation(self, service: Service):
        self.service_to_delete = service
        self.show_delete_alert = True

    @rx.event
    def delete_service(self):
        """Deletes a service record.
        SQL Query: DELETE FROM Servicios WHERE ID = ...;
        """
        if self.service_to_delete:
            self.services = [
                s for s in self.services if s["id"] != self.service_to_delete["id"]
            ]
        return ServiceState.cancel_delete

    @rx.event
    def cancel_delete(self):
        self.show_delete_alert = False
        self.service_to_delete = None