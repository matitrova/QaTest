import time

from config import BASE_URL
from AlertsPage import AlertsPage


# A diferencia de /javascript_alerts (DesafiosPlaywright/JavascriptAlertsPage.py),
# acá Confirm y Prompt no escriben ningún resultado en el DOM: lo único que
# producen es un SEGUNDO alert() que la propia página dispara con un
# setTimeout(1000ms) después de la respuesta al primero. No alcanza con
# page.once() (hay dos diálogos en la misma interacción, no uno), así que el
# handler queda registrado con page.on() y se saca explícitamente al final de
# cada test para no dejarlo pegado.


def test_alert_simple(page):
    alerts_page = AlertsPage(page)
    page.goto(f"{BASE_URL}/alerts")

    dialogos = []

    def manejar(dialog):
        dialogos.append((dialog.type, dialog.message))
        dialog.accept()

    page.once("dialog", manejar)
    alerts_page.hacer_clic_en_alert()

    assert dialogos == [("alert", "Today is a working day.\nOr less likely a holiday.")]


def test_confirm_aceptado_dispara_un_segundo_alert_con_yes_despues_de_un_segundo(page):
    alerts_page = AlertsPage(page)
    page.goto(f"{BASE_URL}/alerts")

    dialogos = []
    tiempos = []

    def manejar(dialog):
        dialogos.append((dialog.type, dialog.message))
        tiempos.append(time.monotonic())
        dialog.accept()

    page.on("dialog", manejar)
    alerts_page.hacer_clic_en_confirm()
    page.wait_for_timeout(1500)
    page.remove_listener("dialog", manejar)

    assert dialogos == [
        ("confirm", "Today is Friday.\nDo you agree?"),
        ("alert", "Yes"),
    ]
    # setTimeout() es una demora mínima garantizada, nunca un tope: el segundo
    # alert no puede llegar antes de 1000ms contados desde que se respondió al
    # confirm, aunque sí puede tardar algo más bajo carga.
    assert tiempos[1] - tiempos[0] >= 0.9


def test_confirm_cancelado_dispara_un_segundo_alert_con_no(page):
    alerts_page = AlertsPage(page)
    page.goto(f"{BASE_URL}/alerts")

    dialogos = []

    def manejar(dialog):
        dialogos.append((dialog.type, dialog.message))
        dialog.dismiss()

    page.on("dialog", manejar)
    alerts_page.hacer_clic_en_confirm()
    page.wait_for_timeout(1500)
    page.remove_listener("dialog", manejar)

    assert dialogos == [
        ("confirm", "Today is Friday.\nDo you agree?"),
        ("alert", "No"),
    ]


def test_prompt_con_texto_dispara_un_segundo_alert_con_el_valor_ingresado(page):
    alerts_page = AlertsPage(page)
    page.goto(f"{BASE_URL}/alerts")

    texto_ingresado = "perros"
    dialogos = []

    def manejar(dialog):
        dialogos.append((dialog.type, dialog.message))
        dialog.accept(texto_ingresado)

    page.on("dialog", manejar)
    alerts_page.hacer_clic_en_prompt()
    page.wait_for_timeout(1500)
    page.remove_listener("dialog", manejar)

    assert dialogos == [
        ("prompt", 'Choose "cats" or \'dogs\'.\nEnter your value:'),
        ("alert", f"User value: {texto_ingresado}"),
    ]


def test_prompt_cancelado_el_segundo_alert_muestra_no_answer(page):
    # El prompt cancelado no deja el valor vacío: la propia página reemplaza
    # el null que devuelve dismiss() por el string "no answer" antes de
    # mostrar el segundo alert, así que el resultado no es el mismo que
    # aceptar el prompt con un campo en blanco.
    alerts_page = AlertsPage(page)
    page.goto(f"{BASE_URL}/alerts")

    dialogos = []

    def manejar(dialog):
        dialogos.append((dialog.type, dialog.message))
        dialog.dismiss()

    page.on("dialog", manejar)
    alerts_page.hacer_clic_en_prompt()
    page.wait_for_timeout(1500)
    page.remove_listener("dialog", manejar)

    assert dialogos == [
        ("prompt", 'Choose "cats" or \'dogs\'.\nEnter your value:'),
        ("alert", "User value: no answer"),
    ]
