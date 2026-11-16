from base_page import BasePage
from playwright.sync_api import Locator, Page


class DatePickersPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.date_input = page.locator("#date")
        self.time_input = page.locator("#time")
        self.datetime_input = page.locator("#datetime")
        self.month_input = page.locator("#month")
        self.week_input = page.locator("#week")
        self.resultado = page.locator("#native-result")
        self.campo_appointment = page.locator("#widget-date")
        self.boton_abrir_calendario = page.locator("#open-calendar")
        self.calendario = page.locator("#calendar")
        self.encabezado_mes = page.locator("#calendar-month")
        self.boton_mes_anterior = page.locator("#previous-month")
        self.boton_mes_siguiente = page.locator("#next-month")
        self.dias = page.locator("#calendar-days button")
        self.dia_seleccionado = page.locator("#calendar-days button.selected")

    def abrir_calendario(self) -> None:
        self.boton_abrir_calendario.click()

    def dia_por_numero(self, dia: int) -> Locator:
        return self.page.locator(f"#calendar-days button[data-date$='-{dia:02d}']")

    def elegir_dia(self, dia: int) -> None:
        self.dia_por_numero(dia).click()
