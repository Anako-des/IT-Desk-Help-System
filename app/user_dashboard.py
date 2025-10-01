import reflex as rx
from app.states.ticket_state import TicketState, Ticket
from app.states.auth_state import AuthState


def user_ticket_row(ticket: Ticket) -> rx.Component:
    return rx.el.tr(
        rx.el.td(ticket["folio"], class_name="px-4 py-3 font-medium"),
        rx.el.td(ticket["description"], class_name="px-4 py-3"),
        rx.el.td(
            rx.el.span(
                ticket["status"],
                class_name=rx.match(
                    ticket["status"],
                    (
                        "Hold",
                        "bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs w-fit",
                    ),
                    (
                        "Working",
                        "bg-[#F25D07] bg-opacity-20 text-[#F25D07] px-2 py-1 rounded-full text-xs w-fit",
                    ),
                    "bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs w-fit",
                ),
            ),
            class_name="px-4 py-3",
        ),
    )


def user_dashboard() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    f"Welcome, {AuthState.user['name']}",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Here are the tickets you have submitted.",
                    class_name="text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="mr-2 h-4 w-4"),
                "Add Ticket",
                class_name="flex items-center px-4 py-2 rounded-lg bg-[#C00264] text-white font-medium hover:bg-[#B2419B]",
            ),
            class_name="flex items-center justify-between mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Folio", class_name="text-left font-medium p-3"),
                        rx.el.th("Description", class_name="text-left font-medium p-3"),
                        rx.el.th("Status", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(TicketState.tickets, user_ticket_row)),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden bg-white",
        ),
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
    )