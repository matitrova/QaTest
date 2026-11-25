from base_page import BasePage
from playwright.sync_api import Locator, Page, expect


class WebsocketPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.connect_button: Locator = page.locator("#connect")
        self.disconnect_button: Locator = page.locator("#disconnect")
        self.connection_status: Locator = page.locator("#connection")
        self.message_input: Locator = page.locator("#message")
        self.send_button: Locator = page.locator("#send")
        self.messages: Locator = page.locator("#messages li")

    def conectar(self) -> None:
        self.connect_button.click()

    def desconectar(self) -> None:
        self.disconnect_button.click()

    def esperar_conectado(self) -> None:
        expect(self.connection_status).to_have_text("Connected", timeout=10000)

    def esperar_desconectado(self) -> None:
        expect(self.connection_status).to_contain_text("Disconnected", timeout=10000)

    def enviar_mensaje(self, texto: str) -> None:
        self.message_input.fill(texto)
        self.send_button.click()

    def ultimo_mensaje(self) -> Locator:
        return self.messages.last

    def textos_mensajes(self) -> list[str]:
        return self.messages.all_inner_texts()
