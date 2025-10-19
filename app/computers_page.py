import reflex as rx
from app.states.computer_state import ComputerState, Computer

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
    label: str, name: str, placeholder: str, default_value: rx.Var[str] | str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            default_value=default_value,
            class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
        ),
        class_name="mb-4",
    )


def add_computer_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add New Computer"),
            rx.dialog.description("Fill in the details for the new computer."),
            rx.el.form(
                form_field("Serial Number", "nserie", "Enter device's serial number"),
                form_field("Name", "name", "Enter device name (e.g., Laptop Pro)"),
                form_field("Brand", "marca", "Enter device brand"),
                form_field("Type", "tipo", "Enter device type (e.g., Laptop)"),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ComputerState.close_add_modal,
                        type="button",
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    ),
                    rx.el.button(
                        "Add Computer",
                        type="submit",
                        class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=ComputerState.add_computer,
                reset_on_submit=True,
            ),
            style=def_dialog_style,
        ),
        open=ComputerState.show_add_dialog,
    )


def edit_computer_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Computer"),
            rx.dialog.description("Update the computer information below."),
            rx.el.form(
                form_field(
                    "Serial Number",
                    "nserie",
                    "",
                    default_value=ComputerState.editing_computer["nserie"].to_string(),
                ),
                form_field(
                    "Name",
                    "name",
                    "",
                    default_value=ComputerState.editing_computer["name"].to_string(),
                ),
                form_field(
                    "Brand",
                    "marca",
                    "",
                    default_value=ComputerState.editing_computer["marca"].to_string(),
                ),
                form_field(
                    "Type",
                    "tipo",
                    "",
                    default_value=ComputerState.editing_computer["tipo"].to_string(),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=ComputerState.close_edit_modal,
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
                on_submit=ComputerState.update_computer,
            ),
            style=def_dialog_style,
        ),
        open=ComputerState.show_edit_dialog,
    )


def delete_computer_alert() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete Computer"),
            rx.alert_dialog.description(
                "Are you sure you want to delete this computer? This action cannot be undone."
            ),
            rx.el.div(
                rx.alert_dialog.cancel(
                    rx.el.button(
                        "Cancel",
                        on_click=ComputerState.cancel_delete,
                        class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                    )
                ),
                rx.alert_dialog.action(
                    rx.el.button(
                        "Delete",
                        on_click=ComputerState.delete_computer,
                        class_name="px-4 py-2 rounded bg-red-500 text-white hover:bg-red-600",
                    )
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
            style=def_dialog_style,
        ),
        open=ComputerState.show_delete_alert,
    )


def computer_row(computer: Computer) -> rx.Component:
    return rx.el.tr(
        rx.el.td(computer["nserie"], class_name="px-4 py-3 font-medium"),
        rx.el.td(computer["name"], class_name="px-4 py-3"),
        rx.el.td(computer["marca"], class_name="px-4 py-3"),
        rx.el.td(computer["tipo"], class_name="px-4 py-3"),
        rx.el.td(computer["fechaS"], class_name="px-4 py-3"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: ComputerState.show_edit_modal(computer),
                    class_name="text-gray-600 hover:text-gray-900",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: ComputerState.show_delete_confirmation(computer),
                    class_name="text-red-500 hover:text-red-700",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-4 py-3",
        ),
    )


def computers_page_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Computer Management", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage all computers and devices in the system.",
                    class_name="text-gray-500",
                ),
                class_name="flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="mr-2 h-4 w-4"),
                "Add Computer",
                on_click=ComputerState.show_add_modal,
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
                    placeholder="Search by serial number, name, or brand...",
                    on_change=ComputerState.set_search_query,
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
                        rx.el.th(
                            "Serial Number", class_name="text-left font-medium p-3"
                        ),
                        rx.el.th("Name", class_name="text-left font-medium p-3"),
                        rx.el.th("Brand", class_name="text-left font-medium p-3"),
                        rx.el.th("Type", class_name="text-left font-medium p-3"),
                        rx.el.th(
                            "Acquisition Date", class_name="text-left font-medium p-3"
                        ),
                        rx.el.th("Actions", class_name="text-left font-medium p-3"),
                        class_name="border-b bg-gray-50",
                    )
                ),
                rx.el.tbody(rx.foreach(ComputerState.filtered_computers, computer_row)),
                class_name="w-full text-sm",
            ),
            class_name="border rounded-lg overflow-hidden bg-white",
        ),
        add_computer_dialog(),
        edit_computer_dialog(),
        delete_computer_alert(),
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
    )