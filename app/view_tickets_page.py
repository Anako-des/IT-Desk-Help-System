import reflex as rx
from app.states.view_ticket_state import ViewTicketState, VistaDetalladaTicket
from app.states.ticket_state import Ticket, TicketState

def_dialog_style = {
    "position": "fixed",
    "top": "50%",
    "left": "50%",
    "transform": "translate(-50%, -50%)",
    "background": "white",
    "padding": "2rem",
    "borderRadius": "1rem",
    "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "width": "90vw",
    "maxWidth": "600px",
}


def ticket_detail_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Ticket Details"),
            rx.dialog.description("Complete information for the selected ticket."),
            rx.el.div(
                rx.el.div(
                    rx.el.strong("Folio: "),
                    ViewTicketState.selected_ticket_details["folio"],
                ),
                rx.el.div(
                    rx.el.strong("Solicitante: "),
                    ViewTicketState.selected_ticket_details["solicitante_nombre"],
                ),
                rx.el.div(
                    rx.el.strong("Dispositivo: "),
                    ViewTicketState.selected_ticket_details["dispositivo_nombre"],
                ),
                rx.el.div(
                    rx.el.strong("Servicio: "),
                    ViewTicketState.selected_ticket_details["servicio_nombre"],
                ),
                rx.el.div(
                    rx.el.strong("Descripción: "),
                    ViewTicketState.selected_ticket_details["descripcion"],
                ),
                rx.el.div(
                    rx.el.strong("Comentarios: "),
                    ViewTicketState.selected_ticket_details["comentarios"],
                ),
                rx.el.div(
                    rx.el.strong("Fecha Inicio: "),
                    ViewTicketState.selected_ticket_details["fechaI"],
                ),
                rx.el.div(
                    rx.el.strong("Estado: "),
                    ViewTicketState.selected_ticket_details["estado"],
                ),
                rx.el.div(
                    rx.el.strong("Fecha Fin: "),
                    rx.cond(
                        ViewTicketState.selected_ticket_details["fechaF"],
                        ViewTicketState.selected_ticket_details["fechaF"],
                        "N/A",
                    ),
                ),
                rx.el.div(
                    rx.el.strong("Attachment: "),
                    rx.cond(
                        ViewTicketState.selected_ticket_details["foto"],
                        rx.el.image(
                            src=rx.get_upload_url(
                                ViewTicketState.selected_ticket_details["foto"]
                            ),
                            class_name="max-w-xs mt-2 rounded",
                        ),
                        rx.el.span("No attachment"),
                    ),
                ),
                class_name="space-y-2 mt-4 text-sm",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=ViewTicketState.close_detail_modal,
                    class_name="mt-6 px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                ),
                class_name="flex justify-end",
            ),
            style=def_dialog_style,
        ),
        open=ViewTicketState.show_detail_modal,
    )


def view_ticket_row(ticket: Ticket) -> rx.Component:
    return rx.el.tr(
        rx.el.td(ticket["folio"], class_name="px-4 py-3 font-medium"),
        rx.el.td(ticket["ra_id"].to_string(), class_name="px-4 py-3"),
        rx.el.td(ticket["servicio_id"].to_string(), class_name="px-4 py-3"),
        rx.el.td(ticket["description"], class_name="px-4 py-3 truncate max-w-xs"),
        rx.el.td(ticket["comentarios"], class_name="px-4 py-3 truncate max-w-xs"),
        rx.el.td(ticket["fechaI"], class_name="px-4 py-3"),
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
        rx.el.td(
            rx.cond(ticket["fechaF"], ticket["fechaF"], "-"), class_name="px-4 py-3"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="w-4 h-4"),
                    on_click=lambda: ViewTicketState.show_ticket_details(ticket),
                    class_name="text-gray-600 hover:text-gray-900",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: TicketState.show_delete_confirmation(ticket),
                    class_name="text-red-500 hover:text-red-700",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3",
        ),
    )


def view_tickets_page() -> rx.Component:
    from app.app import sidebar, delete_ticket_alert

    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1(
                "View All Tickets", class_name="text-2xl font-bold text-gray-900 mb-6"
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Folio", class_name="text-left font-medium p-3"),
                            rx.el.th("RA ID", class_name="text-left font-medium p-3"),
                            rx.el.th(
                                "Service ID", class_name="text-left font-medium p-3"
                            ),
                            rx.el.th(
                                "Description", class_name="text-left font-medium p-3"
                            ),
                            rx.el.th(
                                "Comments", class_name="text-left font-medium p-3"
                            ),
                            rx.el.th(
                                "Start Date", class_name="text-left font-medium p-3"
                            ),
                            rx.el.th("Status", class_name="text-left font-medium p-3"),
                            rx.el.th(
                                "End Date", class_name="text-left font-medium p-3"
                            ),
                            rx.el.th("Actions", class_name="text-left font-medium p-3"),
                            class_name="border-b bg-gray-50",
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ViewTicketState.tickets_for_view, view_ticket_row)
                    ),
                    class_name="w-full text-sm",
                ),
                class_name="border rounded-lg overflow-x-auto bg-white",
            ),
            class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
        ),
        ticket_detail_modal(),
        delete_ticket_alert(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )