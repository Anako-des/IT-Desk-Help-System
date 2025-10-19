import reflex as rx
from typing import TypedDict, Optional
import datetime
from app.states.computer_state import Computer, ComputerState


class Mantenimiento(TypedDict):
    id: int
    computer_nserie: str
    tipo: str
    descripcion: str
    fecha: str


class MantenimientoState(rx.State):
    mantenimientos: list[Mantenimiento] = [
        {
            "id": 1,
            "computer_nserie": "DELL-LAT-7420-01",
            "tipo": "Preventivo",
            "descripcion": "Limpieza interna y actualización de BIOS.",
            "fecha": "2024-06-15",
        },
        {
            "id": 2,
            "computer_nserie": "HP-ED-800-02",
            "tipo": "Correctivo",
            "descripcion": "Se reemplazó la fuente de poder.",
            "fecha": "2024-05-20",
        },
        {
            "id": 3,
            "computer_nserie": "LEN-TP-X1C-03",
            "tipo": "Preventivo",
            "descripcion": "Reinstalación de sistema operativo.",
            "fecha": "2024-07-01",
        },
        {
            "id": 4,
            "computer_nserie": "BRO-HL-L2380-06",
            "tipo": "Correctivo",
            "descripcion": "Cambio de tóner y limpieza de rodillos.",
            "fecha": "2024-08-10",
        },
        {
            "id": 5,
            "computer_nserie": "DELL-XPS-15-07",
            "tipo": "Preventivo",
            "descripcion": "Actualización de drivers y limpieza.",
            "fecha": "2024-09-05",
        },
        {
            "id": 6,
            "computer_nserie": "HP-ED-800-02",
            "tipo": "Preventivo",
            "descripcion": "Optimización de inicio.",
            "fecha": "2024-11-20",
        },
        {
            "id": 7,
            "computer_nserie": "DELL-LAT-7420-01",
            "tipo": "Correctivo",
            "descripcion": "Se reconectó el flex de la pantalla.",
            "fecha": "2025-01-18",
        },
        {
            "id": 8,
            "computer_nserie": "HP-SP-X360-08",
            "tipo": "Software",
            "descripcion": "Eliminación de malware.",
            "fecha": "2025-02-22",
        },
        {
            "id": 9,
            "computer_nserie": "LEN-TP-X1C-03",
            "tipo": "Hardware",
            "descripcion": "Aumento de memoria RAM a 16GB.",
            "fecha": "2025-03-10",
        },
        {
            "id": 10,
            "computer_nserie": "BRO-HL-L2380-06",
            "tipo": "Preventivo",
            "descripcion": "Limpieza general de la unidad.",
            "fecha": "2025-04-02",
        },
    ]
    computers: list[Computer] = ComputerState.computers
    search_query: str = ""
    show_add_dialog: bool = False
    next_id: int = 11

    @rx.event
    def show_add_modal(self):
        self.show_add_dialog = True

    @rx.event
    def close_add_modal(self):
        self.show_add_dialog = False

    @rx.event
    def add_mantenimiento(self, form_data: dict):
        new_mantenimiento = Mantenimiento(
            id=self.next_id,
            computer_nserie=form_data["computer_nserie"],
            tipo=form_data["tipo"],
            descripcion=form_data["descripcion"],
            fecha=form_data.get("fecha", datetime.date.today().isoformat()),
        )
        self.mantenimientos.append(new_mantenimiento)
        self.next_id += 1
        return MantenimientoState.close_add_modal

    @rx.var
    def filtered_mantenimientos(self) -> list[Mantenimiento]:
        if not self.search_query:
            return self.mantenimientos
        return [
            m
            for m in self.mantenimientos
            if self.search_query.lower() in m["computer_nserie"].lower()
            or self.search_query.lower() in m["tipo"].lower()
            or self.search_query.lower() in m["descripcion"].lower()
        ]

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query