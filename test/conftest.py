def pytest_addoption(parser):
    parser.addoption(
        "--program_name",
        action="store",
        default="multply.s",
        help="Nome do arquivo de programa C a ser testado"
    )

import pytest

@pytest.fixture
def program_name(request):
    return request.config.getoption("--program_name")
