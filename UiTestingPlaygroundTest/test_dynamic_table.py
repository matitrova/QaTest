from config import BASE_URL
from DynamicTablePage import DynamicTablePage


def test_cpu_de_chrome_coincide_con_el_label(page):
    dynamic_table_page = DynamicTablePage(page)

    # Los valores son al azar en cada visita, así que el único chequeo
    # posible es que las dos fuentes coincidan entre sí -- no hay un valor
    # fijo esperado. Se repite en varias recargas para no validar una sola
    # combinación de orden de columnas y filas.
    for _ in range(5):
        page.goto(f"{BASE_URL}/dynamictable")
        assert dynamic_table_page.cpu_de_chrome() == dynamic_table_page.cpu_del_label()


def test_el_orden_de_las_columnas_cambia_entre_recargas(page):
    dynamic_table_page = DynamicTablePage(page)
    page.goto(f"{BASE_URL}/dynamictable")
    primer_orden = dynamic_table_page.nombres_de_columnas()

    # La columna de nombre del proceso es la única que siempre queda
    # primera; el resto se reordena al azar en cada recarga.
    assert primer_orden[0] == "Name"
    assert set(primer_orden) == {"Name", "CPU", "Disk", "Memory", "Network"}

    ordenes_distintos = False
    for _ in range(5):
        page.reload()
        orden = dynamic_table_page.nombres_de_columnas()
        assert orden[0] == "Name"
        if orden != primer_orden:
            ordenes_distintos = True
    assert ordenes_distintos


def test_la_fila_de_chrome_cambia_de_posicion_entre_recargas(page):
    dynamic_table_page = DynamicTablePage(page)
    page.goto(f"{BASE_URL}/dynamictable")
    primera_posicion = dynamic_table_page.nombres_de_procesos_en_orden().index("Chrome")

    posiciones_distintas = False
    for _ in range(5):
        page.reload()
        posicion = dynamic_table_page.nombres_de_procesos_en_orden().index("Chrome")
        if posicion != primera_posicion:
            posiciones_distintas = True
    assert posiciones_distintas
