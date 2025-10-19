import reflex as rx
from app.states.mantenimiento_state import MantenimientoState, Mantenimiento


def mantenimiento_row(mantenimiento: Mantenimiento) -> rx.Component:
    return rx.el.tr(
        rx.el.td(mantenimiento["computer_nserie"], class_name="px-4 py-3 font-medium"),
        rx.el.td(mantenimiento["tipo"], class_name="px-4 py-3"),
        rx.el.td(mantenimiento["descripcion"], class_name="px-4 py-3"),
        rx.el.td(mantenimiento["fecha"], class_name="px-4 py-3"),
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
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
    )