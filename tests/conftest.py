import pytest

from database import OrcamentoRepository
from services import CalculoService


@pytest.fixture
def calculo_service() -> CalculoService:
    return CalculoService()


@pytest.fixture
def repositorio(tmp_path) -> OrcamentoRepository:
    return OrcamentoRepository(tmp_path / "teste_imobiliaria.db")
