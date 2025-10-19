import reflex as rx
from app.states.ra_state import RAState, RA

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
    "maxWidth": "500px",
}


def form_field(
    label: str,
    name: str,
    placeholder: str,
    default_value: rx.Var[str] | str = "",
    type: str = "text",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            default_value=default_value,
            type=type,
            class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
        ),
        class_name="mb-4",
    )


def form_select_field(
    label: str,
    name: str,
    options: rx.Var[list],
    option_value_key: str,
    option_label_key: str,
    placeholder: str,
    default_value: rx.Var[str] | str = "",
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700"),
        rx.el.select(
            rx.el.option(placeholder, value="", disabled=True),
            rx.foreach(
                options,
                lambda option: rx.el.option(
                    option[option_label_key], value=option[option_value_key]
                ),
            ),
            name=name,
            default_value=default_value,
            class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50 bg-white",
        ),
        class_name="mb-4",
    )


def add_ra_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add New Assignment"),
            rx.dialog.description("Assign a device to a user."),
            rx.el.form(
                form_select_field(
                    "User",
                    "user_rfc",
                    RAState.users,
                    "userName",
                    "name",
                    "Select a user",
                ),
                form_select_field(
                    "Computer",
                    "dispositivo_nserie",
                    RAState.computers,
                    "nserie",
                    "name",
                    "Select a computer",
                ),
                form_field("Assignment Date", "fechaA", "", type="date"),
                form_field("Comments", "comentarios", "Enter comments..."),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=RAState.close_add_modal,
                        type="button",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Add Assignment",
                        type="submit",
                        class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=RAState.add_ra,
                reset_on_submit=True,
            ),
            style=def_dialog_style,
        ),
        open=RAState.show_add_dialog,
    )


def edit_ra_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Assignment"),
            rx.dialog.description("Update the assignment details below."),
            rx.el.form(
                form_select_field(
                    "User",
                    "user_rfc",
                    RAState.users,
                    "userName",
                    "name",
                    "Select a user",
                    default_value=RAState.editing_ra["user_rfc"].to_string(),
                ),
                form_select_field(
                    "Computer",
                    "dispositivo_nserie",
                    RAState.computers,
                    "nserie",
                    "name",
                    "Select a computer",
                    default_value=RAState.editing_ra["dispositivo_nserie"].to_string(),
                ),
                form_field(
                    "Comments",
                    "comentarios",
                    "",
                    default_value=RAState.editing_ra["comentarios"].to_string(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=RAState.close_edit_modal,
                        type="button",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Save Changes",
                        type="submit",
                        class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=RAState.update_ra,
            ),
            style=def_dialog_style,
        ),
        open=RAState.show_edit_dialog,
    )


def delete_ra_alert() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete Assignment"),
            rx.alert_dialog.description(
                "Are you sure you want to delete this assignment? This action cannot be undone."
            ),
            rx.el.div(
                rx.alert_dialog.cancel(
                    rx.el.button(
                        "Cancel",
                        on_click=RAState.cancel_delete,
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    )
                ),
                rx.alert_dialog.action(
                    rx.el.button(
                        "Delete",
                        on_click=RAState.delete_ra,
                        class_name="px-4 py-2 rounded bg-red-500 text-white hover:bg-red-600",
                    )
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
            style=def_dialog_style,
        ),
        open=RAState.show_delete_alert,
    )


def ra_row(ra: RA) -> rx.Component:
    return rx.el.tr(
        rx.el.td(ra["user_rfc"], class_name="px-4 py-3 font-medium"),
        rx.el.td(ra["dispositivo_nserie"], class_name="px-4 py-3"),
        rx.el.td(ra["fechaA"], class_name="px-4 py-3"),
        rx.el.td(ra["comentarios"], class_name="px-4 py-3 truncate max-w-xs"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: RAState.show_edit_modal(ra),
                    class_name="text-gray-600 hover:text-gray-900",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: RAState.show_delete_confirmation(ra),
                    class_name="text-red-500 hover:text-red-700",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3",
        ),
    )


def ra_page_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Resource Assignment (RA)",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Manage all user-device assignments.", class_name="text-gray-500"
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="mr-2 h-4 w-4"),
                "Add Assignment",
                on_click=RAState.show_add_modal,
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
                    placeholder="Search by Username, Device S/N, or comments...",
                    on_change=RAState.set_search_query,
                    class_name="pl-10 w-full bg-white border border-gray-300 rounded-lg py-2 px-4 focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                ),
                class_name="relative w-full max-w-lg",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Username", class_name="text-left font-medium p-3"),
                        rx.el.th("Device S/N", class_name="text-left font-medium p-3"),
                        rx.el.th(
                            "Assignment Date", class_name="text-left font-medium p-3"
                        ),
                        rx.el.th("Comments", class_name="text-left font-medium p-3"),
                        rx.el.th("Actions", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(RAState.filtered_ras, ra_row)),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden bg-white",
        ),
        add_ra_dialog(),
        edit_ra_dialog(),
        delete_ra_alert(),
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
    )