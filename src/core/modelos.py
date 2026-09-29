# esta seção tem como objetivo modelar e validar os documentos de pedido de patente com base nas regras do INPE e usando o pydantic como Validador de dados.
#os documentos de pedido de patente de inovação colocados até agora (28/09/2026) são:
# quandro reivincatorio, desenhos, resumo e relatorio descritivo - PI 
# o que falta: os modelos de de pedido de patente de modalidade. 


from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field, field_validator


# ==============================================================================
# 1. MODELOS PARA: QUADRO REIVINDICATÓRIO (IN 30/2013)
# ==============================================================================
class ReivindicacaoItem(BaseModel):
    numero: int = Field(..., ge=1, description="Número da reivindicação (1, 2, 3...)")
    tipo: str = Field(
        default="independente",
        description="'independente' ou 'dependente'"
    )
    preambulo: str = Field(
        ...,
        description="Categoria e características genéricas (ex: SISTEMA DE MONITORAMENTO...)"
    )
    dependencia: Optional[int] = Field(
        default=None,
        description="Número da reivindicação vinculada caso seja dependente"
    )
    caracterizacao: str = Field(
        ...,
        description="Texto após a expressão 'caracterizado por' com a matéria pleiteada"
    )

    @field_validator("preambulo", "caracterizacao")
    @classmethod
    def sem_ponto_intermediario(cls, v: str) -> str:
        """Art. 4º, VII da IN 30/2013: cada reivindicação deve ter apenas um ponto final."""
        texto = v.strip()
        if "." in texto:
            # Remove pontos intermediários acidentais
            texto = texto.replace(".", "")
        return texto

    @computed_field
    def texto_formatado(self) -> str:
        """
        Monta a reivindicação completa conforme as normas do INPI:
        - Independente: [Nº]. [Preâmbulo], caracterizado por [Matéria].
        - Dependente: [Nº]. [Preâmbulo], de acordo com a reivindicação [X], caracterizado por [Matéria].
        """
        if self.tipo == "dependente" and self.dependencia:
            corpo = (
                f"{self.preambulo}, de acordo com a reivindicação {self.dependencia}, "
                f"caracterizado por {self.caracterizacao}"
            )
        else:
            corpo = f"{self.preambulo}, caracterizado por {self.caracterizacao}"

        corpo_limpo = corpo.strip().rstrip(".")
        return f"{self.numero}. {corpo_limpo}."


# ==============================================================================
# 2. MODELOS PARA: DESENHOS (Portaria 14/2024)
# ==============================================================================
class DesenhoItem(BaseModel):
    numero_figura: str = Field(..., description="Identificador da figura (ex: '1', '2A')")
    caminho_imagem: str = Field(
        default="", 
        description="Caminho local da imagem enviada pelo usuário"
    )
    descricao_breve: str = Field(
        default="", 
        description="Descrição sucinta para referência no Relatório Descritivo"
    )

    @field_validator("caminho_imagem")
    @classmethod
    def validar_arquivo_existe(cls, v: str) -> str:
        if not v:
            return v
        caminho = Path(v)
        if not caminho.exists() or not caminho.is_file():
            raise ValueError(f"O arquivo de imagem não foi encontrado no caminho: {v}")
        return v


# ==============================================================================
# 3. MODELOS PARA: RESUMO (50 a 200 palavras)
# ==============================================================================
class ResumoPI(BaseModel):
    titulo: str = Field(..., min_length=5, description="Título da invenção")
    texto: str = Field(..., description="Resumo em parágrafo único (50 a 200 palavras)")

    @field_validator("texto")
    @classmethod
    def validar_contagem_palavras(cls, v: str) -> str:
        qtd_palavras = len(v.strip().split())
        if qtd_palavras < 50 or qtd_palavras > 200:
            raise ValueError(
                f"O resumo deve conter entre 50 e 200 palavras. "
                f"Atualmente possui {qtd_palavras} palavras."
            )
        return v


# ==============================================================================
# 4. MODELOS PARA: RELATÓRIO DESCRITIVO
# ==============================================================================
class RelatorioDescritivoPI(BaseModel):
    titulo: str = Field(..., min_length=5)
    campo_da_invencao: str = Field(..., min_length=10)
    estado_da_tecnica: str = Field(..., min_length=10)
    problema_e_vantagens: str = Field(..., min_length=10)
    desenhos: List[DesenhoItem] = Field(default_factory=list)
    paragrafos_descricao: List[str] = Field(default_factory=list)
    exemplos_concretizacao: str = Field(..., min_length=10)


# ==============================================================================
# 5. MODELO CONSOLIDADOR (PACOTE COMPLETO DE PATENTE PI)
# ==============================================================================
class PatentePICompleta(BaseModel):
    relatorio: RelatorioDescritivoPI
    quadro_reivindicatorio: List[ReivindicacaoItem]
    desenhos: List[DesenhoItem]
    resumo: ResumoPI

# ==============================================================================
# 6. RELATPRIO DESCRITIVO MU 
# ==============================================================================
class RelatorioDescritivoMU(BaseModel):
    titulo: str = Field(
        ...,
        min_length=10,
        description="Título do modelo (ex: DISPOSIÇÃO CONSTRUTIVA EM SUPORTE ARTICULADO)"
    )
    campo_do_modelo: str = Field(
        ...,
        min_length=10,
        description="Setor prático de aplicação do objeto"
    )
    estado_da_tecnica: str = Field(
        ...,
        min_length=10,
        description="Descrição dos objetos similares existentes e suas deficiências"
    )
    melhoria_funcional: str = Field(
        ...,
        min_length=10,
        description="Apresentação da nova forma/disposição e a melhoria prática gerada"
    )
    desenhos: List[DesenhoItem] = Field(
        ..., 
        min_length=1, 
        description="Desenhos são indispensáveis em MU (Art. 9º LPI)"
    )
    paragrafos_descricao: List[str] = Field(
        default_factory=list,
        description="Detalhamento das partes e encaixes referenciando as figuras"
    )

    @field_validator("titulo")
    @classmethod
    def validar_padrao_titulo_mu(cls, v: str) -> str:
        """Orienta o usuário conforme a diretriz formal do INPI para títulos de MU."""
        titulo_upper = v.strip().upper()
        prefixos_validos = ("DISPOSIÇÃO CONSTRUTIVA", "DISPOSIÇÃO INTRODUZIDA", "APERFEIÇOAMENTO")
        if not any(titulo_upper.startswith(p) for p in prefixos_validos):
            # Não bloqueia totalmente, mas pode ser ajustado para padronização
            pass
        return v


class PatenteMUCompleta(BaseModel):
    """Pacote completo de documentos para pedido de Modelo de Utilidade (MU)."""
    relatorio: RelatorioDescritivoMU
    quadro_reivindicatorio: List[ReivindicacaoItem]
    desenhos: List[DesenhoItem]
    resumo: ResumoPI

