from playwright.sync_api import expect

from config import BASE_URL
from JavascriptAlertsPage import JavascriptAlertsPage


# Playwright descarta (dismiss) los diálogos JS automáticamente si no hay
# un listener registrado antes de que aparezcan -- a diferencia de Selenium,
# acá no existe un "switch_to.alert" posterior al click. Por eso el
# page.once("dialog", ...) siempre va ANTES de disparar la acción que
# abre el diálogo, y se usa "once" (no "on") para no dejar el handler
# pegado y afectar al resto de los tests.

def test_alert_simple(page):
    alerts_page = JavascriptAlertsPage(page)
    page.goto(f"{BASE_URL}/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.accept())
    alerts_page.hacer_clic_en_alert()

    expect(alerts_page.result_text).to_have_text("You successfully clicked an alert")


def test_confirm_aceptado(page):
    alerts_page = JavascriptAlertsPage(page)
    page.goto(f"{BASE_URL}/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.accept())
    alerts_page.hacer_clic_en_confirm()

    expect(alerts_page.result_text).to_have_text("You clicked: Ok")


def test_confirm_cancelado(page):
    alerts_page = JavascriptAlertsPage(page)
    page.goto(f"{BASE_URL}/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.dismiss())
    alerts_page.hacer_clic_en_confirm()

    expect(alerts_page.result_text).to_have_text("You clicked: Cancel")


def test_prompt_con_texto(page):
    alerts_page = JavascriptAlertsPage(page)
    page.goto(f"{BASE_URL}/javascript_alerts")

    texto_ingresado = "Automatizado con Playwright"
    page.once("dialog", lambda dialog: dialog.accept(texto_ingresado))
    alerts_page.hacer_clic_en_prompt()

    expect(alerts_page.result_text).to_have_text(f"You entered: {texto_ingresado}")


def test_prompt_cancelado(page):
    alerts_page = JavascriptAlertsPage(page)
    page.goto(f"{BASE_URL}/javascript_alerts")

    page.once("dialog", lambda dialog: dialog.dismiss())
    alerts_page.hacer_clic_en_prompt()

    expect(alerts_page.result_text).to_have_text("You entered: null")
