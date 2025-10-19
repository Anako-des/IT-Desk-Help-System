import reflex as rx
from app.states.mantenimiento_state import MantenimientoState, Mantenimiento


def mantenimiento_row(mantenimiento: Mantenimiento) -> rx.Component:
    return rx.el.tr(
        rx.el.td(mantenimiento["computer_nserie"], class_name="px-4 py-3 font-medium"),
        rx.el.td(mantenimiento["tipo"], class_name="px-4 py-3"),
        rx.el.td(mantenimiento["descripcion"], class_name="px-4 py-3"),
        rx.el.td(mantenimiento["fecha"], class_name="px-4 py-3"),
    )


def add_maintenance_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add Maintenance Record"),
            rx.dialog.description(
                "Fill in the details for the new maintenance record."
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Device S/N", class_name="font-medium text-gray-700"),
                    rx.el.input(
                        name="computer_nserie",
                        placeholder="Enter device serial number",
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Type", class_name="font-medium text-gray-700"),
                    rx.el.input(
                        name="tipo",
                        placeholder="e.g., Preventivo, Correctivo",
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Description", class_name="font-medium text-gray-700"),
                    rx.el.input(
                        name="descripcion",
                        placeholder="Describe the maintenance done",
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=MantenimientoState.close_add_modal,
                        type="button",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Add Record",
                        type="submit",
                        class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=MantenimientoState.add_mantenimiento,
                reset_on_submit=True,
            ),
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "background": "white",
                "padding": "2rem",
                "borderRadius": "1rem",
                "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
                "width": "90vw",
                "maxWidth": "500px",
            },
        ),
        open=MantenimientoState.show_add_dialog,
    )


def mantenimiento_page_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Maintenance Records", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "View all maintenance records for devices.",
                    class_name="text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="mr-2 h-4 w-4"),
                "Add Maintenance",
                on_click=MantenimientoState.show_add_modal,
                class_name="flex items-center px-4 py-2 rounded-lg bg-[#C00264] text-white font-medium hover:bg-[#B2419B]",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search by S/N, type, or description...",
                    on_change=MantenimientoState.set_search_query,
                    class_name="pl-10 w-full bg-white border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                ),
                class_name="relative w-full max-w-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Device S/N", class_name="text-left font-medium p-3"),
                        rx.el.th("Type", class_name="text-left font-medium p-3"),
                        rx.el.th("Description", class_name="text-left font-medium p-3"),
                        rx.el.th("Date", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        MantenimientoState.filtered_mantenimientos, mantenimiento_row
                    )
                ),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden bg-white",
        ),
        add_maintenance_dialog(),
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
    )