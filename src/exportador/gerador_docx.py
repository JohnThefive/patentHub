from pathlib import Path
from docxtpl import DocxTemplate
from src.core.modelos import RelatorioDescritivoPI

# Diretório raiz do projeto PatentHub
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent.parent

TEMPLATE_RELATORIO_PI = (
    DIRETORIO_RAIZ
    / "Assets"
    / "templates"
    / "arquivos_patente_pi"
    / "01_template_PI_relatorio_descritivo.docx"
)


def gerar_relatorio_pi(dados: RelatorioDescritivoPI, caminho_saida: Path) -> Path:
    """
    Carrega o template Word do Relatório Descritivo de PI,
    aplica os dados através do docxtpl (Jinja2) e salva o documento preenchido.
    """
    if not TEMPLATE_RELATORIO_PI.exists():
        raise FileNotFoundError(f"Template não encontrado em: {TEMPLATE_RELATORIO_PI}")

    doc = DocxTemplate(TEMPLATE_RELATORIO_PI)

    # O template utiliza a chave 'relatorio' como namespace (ex: {{ relatorio.titulo }})
    contexto = {
        "relatorio": dados.model_dump()
    }

    doc.render(contexto)

    # Garante que a pasta de destino exista
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)

    return caminho_saida
