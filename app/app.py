import reflex as rx
from app.states.ticket_state import TicketState, Ticket
from app.users_page import users_page_content
from app.computers_page import computers_page_content
from app.ra_page import ra_page_content
from app.services_page import services_page_content
from app.mantenimiento_page import mantenimiento_page_content


def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium"),
            href=href,
            class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
        class_name="w-full",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("activity", class_name="h-6 w-6 text-[#C00264]"),
                rx.el.span("IT Helpdesk", class_name="sr-only"),
                href="/",
                class_name="flex items-center gap-2 font-semibold",
            ),
            class_name="flex h-[60px] items-center border-b px-6",
        ),
        rx.el.div(
            rx.el.nav(
                sidebar_item("Dashboard", "home", "/"),
                sidebar_item("Users", "users", "/users"),
                sidebar_item("Computers", "laptop", "/computers"),
                sidebar_item("RA", "file-text", "/ra"),
                sidebar_item("Services", "settings", "/services"),
                sidebar_item("Maintenance", "wrench", "/mantenimiento"),
                sidebar_item("Ticket", "ticket", "/tickets"),
                class_name="grid items-start px-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto py-2",
        ),
        class_name="hidden border-r bg-white md:block",
    )


def stat_card(
    title: str, value: rx.Var[int], color: str, icon_name: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(title, class_name="text-sm font-medium text-gray-500"),
                rx.el.p(value, class_name="text-4xl font-bold"),
            ),
            rx.icon(icon_name, class_name="w-8 h-8 text-gray-500"),
            class_name="flex items-center justify-between",
        ),
        class_name=f"p-6 rounded-lg shadow-sm {color}",
    )


def ticket_row(ticket: Ticket) -> rx.Component:
    return rx.el.tr(
        rx.el.td(ticket["folio"], class_name="px-4 py-3 font-medium"),
        rx.el.td(ticket["ra_id"], class_name="px-4 py-3"),
        rx.el.td(ticket["servicio_id"], class_name="px-4 py-3"),
        rx.el.td(ticket["descripcion"], class_name="px-4 py-3 max-w-xs truncate"),
        rx.el.td(ticket["comentarios"], class_name="px-4 py-3 max-w-xs truncate"),
        rx.el.td(ticket["fechaI"], class_name="px-4 py-3"),
        rx.el.td(
            rx.el.span(
                ticket["estado"],
                class_name=rx.match(
                    ticket["estado"],
                    (
                        "Hold",
                        "bg-gray-200 text-gray-800 px-2 py-1 rounded-full text-xs w-fit",
                    ),
                    (
                        "Working",
                        "bg-[#F25D07] bg-opacity-20 text-[#F25D07] px-2 py-1 rounded-full text-xs w-fit",
                    ),
                    (
                        "Finish",
                        "bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs w-fit",
                    ),
                    "bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs w-fit",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(ticket["fechaF"], class_name="px-4 py-3"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="w-4 h-4"),
                    on_click=lambda: TicketState.show_see_modal(ticket),
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


def search_filter_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
            ),
            rx.el.input(
                placeholder="Search by folio, requester, or responsible...",
                on_change=TicketState.set_search_query,
                class_name="pl-10 w-full bg-white border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
            ),
            class_name="relative w-full max-w-md",
        ),
        rx.el.select(
            rx.el.option("All Statuses", value="all"),
            rx.el.option("Hold", value="Hold"),
            rx.el.option("Working", value="Working"),
            rx.el.option("Finish", value="Finish"),
            on_change=TicketState.set_status_filter,
            default_value="all",
            class_name="bg-white border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
        ),
        class_name="flex items-center gap-4 mb-4",
    )


def tickets_table() -> rx.Component:
    return rx.el.div(
        rx.el.h2("All Tickets", class_name="text-xl font-semibold mb-4"),
        search_filter_bar(),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Folio", class_name="text-left font-medium p-3"),
                        rx.el.th("RA ID", class_name="text-left font-medium p-3"),
                        rx.el.th("Service ID", class_name="text-left font-medium p-3"),
                        rx.el.th("Description", class_name="text-left font-medium p-3"),
                        rx.el.th("Comments", class_name="text-left font-medium p-3"),
                        rx.el.th("Start Date", class_name="text-left font-medium p-3"),
                        rx.el.th("Status", class_name="text-left font-medium p-3"),
                        rx.el.th("End Date", class_name="text-left font-medium p-3"),
                        rx.el.th("Actions", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(TicketState.filtered_tickets, ticket_row)),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-x-auto bg-white",
        ),
    )


def see_ticket_details(label: str, value: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="font-semibold text-gray-600"),
        rx.el.p(value, class_name="text-gray-800"),
        class_name="mb-3",
    )


def see_ticket_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Ticket Details"),
            rx.dialog.description("Viewing ticket details."),
            rx.el.div(
                see_ticket_details(
                    "Folio", TicketState.ticket_to_see["folio"].to_string()
                ),
                see_ticket_details(
                    "RA ID", TicketState.ticket_to_see["ra_id"].to_string()
                ),
                see_ticket_details(
                    "Service ID", TicketState.ticket_to_see["servicio_id"].to_string()
                ),
                see_ticket_details(
                    "Description", TicketState.ticket_to_see["descripcion"].to_string()
                ),
                see_ticket_details(
                    "Comments", TicketState.ticket_to_see["comentarios"].to_string()
                ),
                see_ticket_details(
                    "Start Date", TicketState.ticket_to_see["fechaI"].to_string()
                ),
                see_ticket_details(
                    "Status", TicketState.ticket_to_see["estado"].to_string()
                ),
                see_ticket_details(
                    "End Date", TicketState.ticket_to_see["fechaF"].to_string()
                ),
                class_name="mt-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=TicketState.close_see_modal,
                    class_name="mt-4 px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                ),
                class_name="flex justify-end",
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
                "maxWidth": "600px",
            },
        ),
        open=TicketState.show_see_dialog,
    )


def delete_ticket_alert() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete Ticket"),
            rx.alert_dialog.description(
                "Are you sure you want to delete this ticket? This action cannot be undone."
            ),
            rx.el.div(
                rx.alert_dialog.cancel(
                    rx.el.button(
                        "Cancel",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    )
                ),
                rx.alert_dialog.action(
                    rx.el.button(
                        "Delete",
                        on_click=TicketState.delete_ticket,
                        class_name="px-4 py-2 rounded bg-red-500 text-white hover:bg-red-600",
                    )
                ),
                class_name="flex justify-end gap-3 mt-4",
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
                "maxWidth": "450px",
            },
        ),
        open=TicketState.show_delete_alert,
    )


def dashboard() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            stat_card("Hold", TicketState.hold_count, "bg-gray-200", "circle_pause"),
            stat_card(
                "Working", TicketState.working_count, "bg-[#F25D07]/20", "loader"
            ),
            stat_card(
                "Finish", TicketState.finished_count, "bg-green-500/20", "check_check"
            ),
            class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-3",
        ),
        rx.el.div(tickets_table(), class_name="mt-8"),
        class_name="flex-1 p-6 space-y-6",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard(),
        delete_ticket_alert(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def users_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        users_page_content(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def computers_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        computers_page_content(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def ra_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        ra_page_content(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def services_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        services_page_content(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def mantenimiento_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        mantenimiento_page_content(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def tickets_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            tickets_table(),
            see_ticket_dialog(),
            delete_ticket_alert(),
            class_name="p-6",
        ),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(users_page, route="/users")
app.add_page(computers_page, route="/computers")
app.add_page(ra_page, route="/ra")
app.add_page(services_page, route="/services")
app.add_page(mantenimiento_page, route="/mantenimiento")
app.add_page(tickets_page, route="/tickets")