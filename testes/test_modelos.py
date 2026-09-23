import pytest
from pydantic import ValidationError
from src.core.modelos import DesenhoItem, RelatorioDescritivoPI


def test_criacao_relatorio_valido():
    relatorio = RelatorioDescritivoPI(
        titulo="Dispositivo de Teste",
        campo_da_invencao="Engenharia Mecânica",
        estado_da_tecnica="Técnica anterior existente",
        problema_e_vantagens="Supera limitações existentes",
        desenhos=[
            DesenhoItem(numero_figura="1", descricao_breve="mostra o protótipo.")
        ],
        paragrafos_descricao=["Primeiro parágrafo", "Segundo parágrafo"],
        exemplos_concretizacao="Exemplo prático de uso.",
    )
    assert relatorio.titulo == "Dispositivo de Teste"
    assert len(relatorio.desenhos) == 1
    assert len(relatorio.paragrafos_descricao) == 2


def test_campos_obrigatorios_faltantes():
    with pytest.raises(ValidationError):
        # Falta 'titulo' e outros obrigatórios
        RelatorioDescritivoPI(
            campo_da_invencao="Engenharia Mecânica",
        )
