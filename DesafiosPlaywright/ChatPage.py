from base_page import BasePage
from playwright.sync_api import Locator, Page, expect


class ChatPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.room_label = page.locator("#room")
        self.status = page.locator("#status")
        self.name_input = page.locator("#name")
        self.join_button = page.locator("#join")
        self.message_input = page.locator("#message")
        self.send_button = page.locator("#send")
        self.messages = page.locator("#messages li")

    def esperar_conectado(self) -> None:
        expect(self.status).to_have_text("Connected", timeout=10000)

    def unirse(self, nombre: str) -> None:
        self.name_input.fill(nombre)
        self.join_button.click()

    def enviar_mensaje(self, texto: str) -> None:
        self.message_input.fill(texto)
        self.send_button.click()

    def ultimo_mensaje(self) -> Locator:
        return self.messages.last

    def textos_mensajes(self) -> list[str]:
        return self.messages.all_inner_texts()
