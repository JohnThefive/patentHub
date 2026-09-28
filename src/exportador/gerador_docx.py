import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from src.core.modelos import (
    DesenhoItem,
    PatentePICompleta,
    ReivindicacaoItem,
    RelatorioDescritivoPI,
    ResumoPI,
)

# Caminhos base dos templates em Assets
DIRETORIO_RAIZ = Path(__file__).resolve().parent.parent.parent
PASTA_TEMPLATES = DIRETORIO_RAIZ / "Assets" / "templates" / "arquivos_patente_pi"

TEMPLATE_RELATORIO = PASTA_TEMPLATES / "01_template_PI_relatorio_descritivo.docx"
TEMPLATE_REIVINDICACOES = PASTA_TEMPLATES / "02_Exemplo_de_PI_quadro_reinvendictorio.docx"
TEMPLATE_DESENHOS = PASTA_TEMPLATES / "03_Exemplo_de_PI _desenhos.docx"
TEMPLATE_RESUMO = PASTA_TEMPLATES / "04_Exemplo_de_PI_Resumo.docx"


# ==============================================================================
# FUNÇÃO AUXILIAR: CONVERSÃO PARA PDF
# ==============================================================================
def converter_docx_para_pdf(caminho_docx: Path) -> Optional[Path]:
    """
    Converte um arquivo .docx para .pdf usando o docx2pdf (requer MS Word no Windows).
    Retorna o caminho do PDF se bem-sucedido, ou None se falhar.
    """
    try:
        from docx2pdf import convert
        caminho_pdf = caminho_docx.with_suffix(".pdf")
        convert(str(caminho_docx), str(caminho_pdf))
        return caminho_pdf
    except Exception as e:
        print(f"[AVISO] Não foi possível converter {caminho_docx.name} para PDF: {e}")
        return None


# ==============================================================================
# 1. GERAÇÃO INDIVIDUAL DOS DOCUMENTOS (.DOCX)
# ==============================================================================
def gerar_relatorio_pi(dados: RelatorioDescritivoPI, caminho_saida: Path) -> Path:
    doc = DocxTemplate(TEMPLATE_RELATORIO)
    doc.render({"relatorio": dados.model_dump()})
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)
    return caminho_saida


def gerar_quadro_reivindicatorio_pi(reivindicacoes: List[ReivindicacaoItem], caminho_saida: Path) -> Path:
    doc = DocxTemplate(TEMPLATE_REIVINDICACOES)
    contexto = {
        "quadro_reivindicatorio": [r.model_dump() for r in reivindicacoes]
    }
    doc.render(contexto)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)
    return caminho_saida

# tecnicamente o mais dificil, testar profundamente.
def gerar_desenhos_pi(desenhos: List[DesenhoItem], caminho_saida: Path) -> Path:
    doc = DocxTemplate(TEMPLATE_DESENHOS)
    
    # Prepara cada imagem como InlineImage do docxtpl
    lista_desenhos_template = []
    for item in desenhos:
        img_obj = InlineImage(doc, str(item.caminho_imagem), width=Mm(150))
        lista_desenhos_template.append({
            "imagem": img_obj,
            "numero_figura": item.numero_figura
        })

    doc.render({"desenhos": lista_desenhos_template})
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)
    return caminho_saida


def gerar_resumo_pi(resumo: ResumoPI, caminho_saida: Path) -> Path:
    doc = DocxTemplate(TEMPLATE_RESUMO)
    doc.render({"resumo": resumo.model_dump()})
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    doc.save(caminho_saida)
    return caminho_saida


# ==============================================================================
# 2. PACOTE COMPLETO DE MINUTAS (PI)
# ==============================================================================
def gerar_pacote_completo_pi(
    patente: PatentePICompleta,
    pasta_destino: Path,
    exportar_pdf: bool = False,
    criar_zip: bool = True
) -> Dict[str, Path]:
    """
    Gera os 4 documentos formais do pedido de patente PI.
    Opcionalmente converte em PDF e empacota tudo em um arquivo .zip.
    """
    pasta_destino.mkdir(parents=True, exist_ok=True)
    arquivos_gerados: Dict[str, Path] = {}

    # 1. Relatório Descritivo
    arq_relatorio = pasta_destino / "01_Relatorio_Descritivo.docx"
    gerar_relatorio_pi(patente.relatorio, arq_relatorio)
    arquivos_gerados["relatorio_docx"] = arq_relatorio

    # 2. Quadro Reivindicatório
    arq_reivindicacoes = pasta_destino / "02_Quadro_Reivindicatorio.docx"
    gerar_quadro_reivindicatorio_pi(patente.quadro_reivindicatorio, arq_reivindicacoes)
    arquivos_gerados["reivindicacoes_docx"] = arq_reivindicacoes

    # 3. Desenhos
    arq_desenhos = pasta_destino / "03_Desenhos.docx"
    gerar_desenhos_pi(patente.desenhos, arq_desenhos)
    arquivos_gerados["desenhos_docx"] = arq_desenhos

    # 4. Resumo
    arq_resumo = pasta_destino / "04_Resumo.docx"
    gerar_resumo_pi(patente.resumo, arq_resumo)
    arquivos_gerados["resumo_docx"] = arq_resumo

    # Conversão opcional para PDF
    if exportar_pdf:
        for chave in list(arquivos_gerados.keys()):
            caminho_docx = arquivos_gerados[chave]
            pdf = converter_docx_para_pdf(caminho_docx)
            if pdf:
                arquivos_gerados[chave.replace("_docx", "_pdf")] = pdf

    # Compactação em ZIP
    if criar_zip:
        caminho_zip = pasta_destino / "Pacote_Minutas_PI.zip"
        with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for caminho in arquivos_gerados.values():
                zipf.write(caminho, arcname=caminho.name)
        arquivos_gerados["pacote_zip"] = caminho_zip

    return arquivos_gerados