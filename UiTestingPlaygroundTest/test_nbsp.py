from NbspPage import ESPACIO_NO_SEPARABLE


def test_xpath_con_espacio_normal_no_encuentra_el_boton(nbsp_page):
    assert nbsp_page.xpath_con_espacio_normal().count() == 0


def test_xpath_con_nbsp_si_encuentra_el_boton(nbsp_page):
    assert nbsp_page.xpath_con_nbsp().count() == 1


def test_el_espacio_real_del_boton_es_un_nbsp(nbsp_page):
    assert ESPACIO_NO_SEPARABLE in nbsp_page.texto_crudo()


def test_get_by_role_encuentra_el_boton_sin_importar_el_tipo_de_espacio(nbsp_page):
    # A diferencia del XPath, el locator por rol y texto visible de
    # Playwright normaliza el nbsp a un espacio común al comparar, así que
    # encuentra el botón con un espacio normal en el texto buscado, aunque
    # el espacio real del botón sea un nbsp.
    assert nbsp_page.boton.count() == 1
    nbsp_page.boton.click()
