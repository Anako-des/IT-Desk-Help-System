import reflex as rx
from app.states.create_ticket_state import CreateTicketState


def form_select_field(
    label: str,
    name: str,
    options: rx.Var[list],
    option_value_key: str,
    option_label_key: str,
    placeholder: str,
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
            class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50 bg-white",
        ),
        class_name="mb-4",
    )


def form_textarea_field(label: str, name: str, placeholder: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="font-medium text-gray-700"),
        rx.el.textarea(
            name=name,
            placeholder=placeholder,
            class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
        ),
        class_name="mb-4",
    )


def create_ticket_form() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "Create New Ticket", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Fill out the form below to submit a new IT support ticket.",
                class_name="text-gray-500",
            ),
            class_name="mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.fieldset(
                    rx.el.legend(
                        "Is this your own equipment?",
                        class_name="font-medium text-gray-700 mb-2",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="is_own_equipment",
                                value="yes",
                                on_click=CreateTicketState.set_is_own_equipment,
                                class_name="mr-2",
                                checked=CreateTicketState.is_own_equipment == "yes",
                            ),
                            "Yes",
                            class_name="flex items-center",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="is_own_equipment",
                                value="no",
                                on_click=CreateTicketState.set_is_own_equipment,
                                class_name="mr-2",
                                checked=CreateTicketState.is_own_equipment == "no",
                            ),
                            "No",
                            class_name="flex items-center",
                        ),
                        class_name="flex gap-4",
                    ),
                    class_name="mb-4 col-span-1 md:col-span-2",
                ),
                rx.el.div(
                    rx.el.label("Requester", class_name="font-medium text-gray-700"),
                    rx.el.select(
                        rx.el.option("Select a user", value="", disabled=True),
                        rx.foreach(
                            CreateTicketState.users,
                            lambda option: rx.el.option(
                                option["name"], value=option["userName"]
                            ),
                        ),
                        name="solicitante",
                        on_change=CreateTicketState.set_selected_requester,
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50 bg-white",
                    ),
                    class_name="mb-4",
                ),
                form_select_field(
                    "Device (RA ID)",
                    "ra_id",
                    CreateTicketState.filtered_devices,
                    "nserie",
                    "name",
                    "Select a device",
                ),
                form_select_field(
                    "Service",
                    "servicio_id",
                    CreateTicketState.services,
                    "id",
                    "nombre",
                    "Select a service",
                ),
                form_textarea_field(
                    "Description", "description", "Describe the issue in detail..."
                ),
                form_textarea_field(
                    "Comments", "comentarios", "Add any initial comments..."
                ),
                rx.el.div(
                    rx.el.label("Photo", class_name="font-medium text-gray-700"),
                    rx.upload.root(
                        rx.el.div(
                            rx.icon("cloud_upload", class_name="w-8 h-8 text-gray-400"),
                            rx.el.p("Click to select a file"),
                            class_name="text-center p-4 border-2 border-dashed rounded-md",
                        ),
                        id="photo_upload",
                        multiple=False,
                        accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
                        on_drop=CreateTicketState.handle_upload(
                            rx.upload_files(upload_id="photo_upload")
                        ),
                        class_name="mt-1",
                    ),
                    rx.foreach(
                        rx.selected_files("photo_upload"),
                        lambda file: rx.el.div(
                            file, class_name="text-sm text-gray-500"
                        ),
                    ),
                    class_name="mb-4",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    type="button",
                    on_click=rx.redirect("/"),
                    class_name="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300",
                ),
                rx.el.button(
                    "Create Ticket",
                    type="submit",
                    class_name="px-4 py-2 rounded bg-[#C00264] text-white hover:bg-[#B2419B]",
                ),
                class_name="flex justify-end gap-3 mt-6 pt-6 border-t",
            ),
            on_submit=CreateTicketState.create_ticket,
            reset_on_submit=True,
            class_name="bg-white p-8 rounded-lg shadow-sm",
        ),
        class_name="flex-1 p-6 space-y-6 bg-[#EAEFF3]",
        on_mount=CreateTicketState.on_load,
    )