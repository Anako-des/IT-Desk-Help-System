import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("activity", class_name="h-8 w-8 text-[#C00264]"),
                rx.el.span("IT Helpdesk", class_name="text-2xl font-bold"),
                href="/",
                class_name="flex items-center gap-2 font-semibold mb-8",
            ),
            rx.el.h1("Sign in to your account", class_name="text-2xl font-bold mb-2"),
            rx.el.p(
                "Enter your credentials to access your account.",
                class_name="text-gray-500 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Username", class_name="font-medium text-gray-700"),
                    rx.el.input(
                        name="username",
                        placeholder="jhernandez or your_email@example.com",
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="font-medium text-gray-700"),
                    rx.el.input(
                        name="password",
                        type="password",
                        placeholder="•••••••••",
                        class_name="w-full mt-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#C00264]/50",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.el.p(
                            AuthState.error_message,
                            class_name="text-red-500 text-sm mb-4",
                        )
                    ),
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full px-4 py-2 rounded-lg bg-[#C00264] text-white font-medium hover:bg-[#B2419B]",
                ),
                on_submit=AuthState.login,
            ),
            class_name="w-full max-w-md p-8 bg-white rounded-xl shadow-md border",
        ),
        class_name="flex items-center justify-center min-h-screen bg-[#EAEFF3] font-['Inter']",
    )