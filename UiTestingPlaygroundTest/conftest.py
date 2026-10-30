import pytest

from config import BASE_URL
from AjaxDataPage import AjaxDataPage
from AlertsPage import AlertsPage
from ClassAttributePage import ClassAttributePage
from ClickPage import ClickPage
from ClientDelayPage import ClientDelayPage
from DynamicIdPage import DynamicIdPage
from DynamicTablePage import DynamicTablePage
from HiddenLayersPage import HiddenLayersPage
from LoadDelayPage import LoadDelayPage
from MouseOverPage import MouseOverPage
from NbspPage import NbspPage
from OverlappedPage import OverlappedPage
from ProgressBarPage import ProgressBarPage
from SampleAppPage import SampleAppPage
from ScrollbarsPage import ScrollbarsPage
from ShadowDomPage import ShadowDomPage
from TextInputPage import TextInputPage
from VerifyTextPage import VerifyTextPage
from VisibilityPage import VisibilityPage

# Cada test de esta suite abría su propio Page Object y navegaba a la misma
# URL fija que todos los demás tests del archivo, repitiendo esas dos líneas
# en los ~80 tests de las 19 páginas. Estas fixtures navegan una sola vez por
# test y entregan el Page Object ya listo, dejando en cada test solo la
# interacción que de verdad varía entre un caso y otro.


@pytest.fixture
def ajax_data_page(page):
    page.goto(f"{BASE_URL}/ajax")
    return AjaxDataPage(page)


@pytest.fixture
def alerts_page(page):
    page.goto(f"{BASE_URL}/alerts")
    return AlertsPage(page)


@pytest.fixture
def class_page(page):
    page.goto(f"{BASE_URL}/classattr")
    return ClassAttributePage(page)


@pytest.fixture
def click_page(page):
    page.goto(f"{BASE_URL}/click")
    return ClickPage(page)


@pytest.fixture
def client_delay_page(page):
    page.goto(f"{BASE_URL}/clientDelay")
    return ClientDelayPage(page)


@pytest.fixture
def dynamic_id_page(page):
    page.goto(f"{BASE_URL}/dynamicid")
    return DynamicIdPage(page)


@pytest.fixture
def dynamic_table_page(page):
    page.goto(f"{BASE_URL}/dynamictable")
    return DynamicTablePage(page)


@pytest.fixture
def hidden_layers_page(page):
    page.goto(f"{BASE_URL}/hiddenlayers")
    return HiddenLayersPage(page)


@pytest.fixture
def load_delay_page(page):
    page.goto(f"{BASE_URL}/loaddelay")
    return LoadDelayPage(page)


@pytest.fixture
def mouse_over_page(page):
    page.goto(f"{BASE_URL}/mouseover")
    return MouseOverPage(page)


@pytest.fixture
def nbsp_page(page):
    page.goto(f"{BASE_URL}/nbsp")
    return NbspPage(page)


@pytest.fixture
def overlapped_page(page):
    page.goto(f"{BASE_URL}/overlapped")
    return OverlappedPage(page)


@pytest.fixture
def progress_bar_page(page):
    page.goto(f"{BASE_URL}/progressbar")
    return ProgressBarPage(page)


@pytest.fixture
def sample_app_page(page):
    page.goto(f"{BASE_URL}/sampleapp")
    return SampleAppPage(page)


@pytest.fixture
def scrollbars_page(page):
    page.goto(f"{BASE_URL}/scrollbars")
    return ScrollbarsPage(page)


@pytest.fixture
def shadow_dom_page(page):
    page.goto(f"{BASE_URL}/shadowdom")
    return ShadowDomPage(page)


@pytest.fixture
def text_input_page(page):
    page.goto(f"{BASE_URL}/textinput")
    return TextInputPage(page)


@pytest.fixture
def verify_text_page(page):
    page.goto(f"{BASE_URL}/verifytext")
    return VerifyTextPage(page)


@pytest.fixture
def visibility_page(page):
    page.goto(f"{BASE_URL}/visibility")
    return VisibilityPage(page)
