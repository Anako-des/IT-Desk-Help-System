import reflex as rx
from app.states.ticket_state import TicketState, Ticket
from app.states.auth_state import AuthState
from app.states.user_state import UserState
from app.states.computer_state import ComputerState
from app.states.ra_state import RAState
from app.states.service_state import ServiceState
from app.users_page import users_page_content
from app.computers_page import computers_page_content
from app.ra_page import ra_page_content
from app.services_page import services_page_content
from app.login_page import login_page
from app.user_dashboard import user_dashboard


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
            rx.el.div(
                rx.el.a(
                    rx.icon("activity", class_name="h-6 w-6 text-[#C00264]"),
                    rx.el.span("IT Helpdesk", class_name="sr-only"),
                    href="/",
                    class_name="flex items-center gap-2 font-semibold",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                    "Logout",
                    on_click=AuthState.logout,
                    class_name="ml-auto text-sm font-medium text-gray-600 hover:text-gray-900",
                ),
                class_name="flex h-[60px] items-center border-b px-6 w-full",
            )
        ),
        rx.el.div(
            rx.el.nav(
                sidebar_item("Dashboard", "home", "/"),
                sidebar_item("Users", "users", "/users"),
                sidebar_item("Computers", "laptop", "/computers"),
                sidebar_item("RA", "file-text", "/ra"),
                sidebar_item("Services", "settings", "/services"),
                sidebar_item("Ticket", "ticket", "#"),
                class_name="grid items-start px-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto py-2",
        ),
        class_name="hidden border-r bg-white md:flex md:flex-col",
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
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: TicketState.show_edit_modal(ticket),
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
                placeholder="Search by folio...",
                on_change=TicketState.set_search_query,
                class_name="pl-10 w-full bg-white border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
            ),
            class_name="relative w-full max-w-sm",
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
                        rx.el.th("Description", class_name="text-left font-medium p-3"),
                        rx.el.th("Status", class_name="text-left font-medium p-3"),
                        rx.el.th("Actions", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(TicketState.filtered_tickets, ticket_row)),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden bg-white",
        ),
    )


def edit_ticket_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Ticket"),
            rx.dialog.description("Update the ticket information below."),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Description", class_name="font-medium"),
                    rx.el.input(
                        name="description",
                        default_value=TicketState.editing_ticket["description"].to(str),
                        class_name="w-full mt-1 p-2 border rounded",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Status", class_name="font-medium"),
                    rx.el.select(
                        rx.el.option("Hold", value="Hold"),
                        rx.el.option("Working", value="Working"),
                        rx.el.option("Finish", value="Finish"),
                        name="status",
                        default_value=TicketState.editing_ticket["status"].to(str),
                        class_name="w-full mt-1 p-2 border rounded bg-white",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=TicketState.close_edit_modal,
                        type="button",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Save Changes",
                        type="submit",
                        class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                on_submit=TicketState.update_ticket,
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
        open=TicketState.show_edit_dialog,
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


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard(),
        edit_ticket_dialog(),
        delete_ticket_alert(),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Inter'] bg-[#EAEFF3]",
    )


def user_dashboard_page() -> rx.Component:
    return rx.el.div(
        rx.el.header(
            rx.el.div(
                rx.el.a(
                    rx.icon("activity", class_name="h-6 w-6 text-[#C00264]"),
                    rx.el.span("IT Helpdesk", class_name="sr-only"),
                    href="/",
                    class_name="flex items-center gap-2 font-semibold",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="w-4 h-4 mr-2"),
                    "Logout",
                    on_click=AuthState.logout,
                    class_name="ml-auto text-sm font-medium text-gray-600 hover:text-gray-900 flex items-center",
                ),
                class_name="flex items-center h-full px-6 w-full",
            ),
            class_name="h-[60px] border-b bg-white",
        ),
        user_dashboard(),
        class_name="min-h-screen w-full font-['Inter'] bg-[#EAEFF3]",
    )


def index() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_logged_in,
            rx.cond(AuthState.is_admin, admin_dashboard_page(), user_dashboard_page()),
            login_page(),
        )
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
app.add_page(index, on_load=[AuthState.check_login, TicketState.load_tickets])
app.add_page(login_page, route="/login")
app.add_page(
    users_page, route="/users", on_load=[AuthState.check_login, UserState.load_users]
)
app.add_page(
    computers_page,
    route="/computers",
    on_load=[AuthState.check_login, ComputerState.load_computers],
)
app.add_page(
    ra_page, route="/ra", on_load=[AuthState.check_login, RAState.load_all_data]
)
app.add_page(
    services_page,
    route="/services",
    on_load=[AuthState.check_login, ServiceState.load_services],
)