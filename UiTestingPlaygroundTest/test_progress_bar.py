from config import BASE_URL
from ProgressBarPage import ProgressBarPage


def test_arranca_en_25_por_ciento_sin_haber_iniciado(page):
    progress_bar_page = ProgressBarPage(page)
    page.goto(f"{BASE_URL}/progressbar")

    assert progress_bar_page.porcentaje_actual() == 25
    assert progress_bar_page.resultado_numerico() is None


def test_detener_antes_del_primer_segundo_no_deja_avanzar(page):
    progress_bar_page = ProgressBarPage(page)
    page.goto(f"{BASE_URL}/progressbar")

    # El primer incremento de la barra no sigue el delay aleatorio de los
    # siguientes: la página lo programa con un setTimeout fijo de 1000ms
    # (`setTimeout(_makeProgress, 1000)`), separado del delay random que
    # usa cada paso posterior. Start y Stop ejecutados uno después del otro,
    # sin ninguna espera entremedio, caen siempre dentro de esa primera
    # ventana fija -- a diferencia de esperar un porcentaje más alto, este
    # caso no depende de ninguna condición de carrera y da el mismo
    # resultado en cualquier corrida.
    progress_bar_page.iniciar()
    progress_bar_page.detener()

    assert progress_bar_page.porcentaje_actual() == 25
    # El propio _setResult() de la página trata el 25% como "todavía no
    # arrancó" (`ratio == 25 ? "n/a" : ratio - 75`), no como un resultado de
    # -50: sin al menos un incremento real, no hay ninguna diferencia contra
    # el 75% que tenga sentido mostrar.
    assert progress_bar_page.resultado_numerico() is None


def test_detener_al_llegar_a_75_por_ciento_da_un_resultado_cercano_a_cero(page):
    progress_bar_page = ProgressBarPage(page)
    page.goto(f"{BASE_URL}/progressbar")

    progress_bar_page.iniciar()
    progress_bar_page.esperar_porcentaje_minimo(75)
    progress_bar_page.detener()

    porcentaje_al_detener = progress_bar_page.porcentaje_actual()
    resultado = progress_bar_page.resultado_numerico()

    # El objetivo de la página es minimizar la diferencia contra 75, no
    # pegarle exacto: el label de resultado es justamente "ratio - 75" leído
    # en el instante del click. Como la barra avanza de a 1 punto por vez,
    # apenas se cumple la condición del sondeo (>= 75) el valor real está en
    # 75 casi siempre, pero el click a Stop no es instantáneo y puede
    # alcanzar a correr un paso más antes de que el handler lo registre.
    assert resultado == porcentaje_al_detener - 75
    assert 0 <= porcentaje_al_detener - 75 <= 3


def test_detener_frena_la_barra_y_ya_no_sigue_avanzando(page):
    progress_bar_page = ProgressBarPage(page)
    page.goto(f"{BASE_URL}/progressbar")

    progress_bar_page.iniciar()
    progress_bar_page.esperar_porcentaje_minimo(50)
    progress_bar_page.detener()
    valor_al_detener = progress_bar_page.porcentaje_actual()

    # Stop() solo pone `started = false`: el propio loop de incremento es el
    # que revisa esa bandera y se corta antes de programar el siguiente
    # paso. Si Stop no detuviera nada de verdad, la barra seguiría subiendo
    # sola con el tiempo. Hay que darle tiempo real de sobra (más que el
    # delay máximo de un paso, ~500ms) para confiar en que no es que
    # todavía no le tocaba avanzar.
    page.wait_for_timeout(1500)

    assert progress_bar_page.porcentaje_actual() == valor_al_detener
