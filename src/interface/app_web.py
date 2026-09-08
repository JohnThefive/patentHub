import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Gerador de Patentes INPI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Estruturação de Minuta de Patente (INPI)")
st.caption(
    "Preencha as seções técnicas abaixo para estruturar o Relatório Descritivo "
    "conforme as diretrizes da Instrução Normativa INPI/PR nº 30/2013."
)

st.divider()

# Abas organizadas pelo fluxo lógico de redação
aba_identificacao, aba_contexto, aba_detalhes, aba_revisao = st.tabs([
    "1. Identificação",
    "2. Contexto & Problema",
    "3. Detalhamento da Invenção",
    "4. Pré-visualização"
])

with aba_identificacao:
    st.subheader("Dados Básicos da Tecnologia")
    
    titulo = st.text_input(
        "Título da Invenção",
        placeholder="Ex: SISTEMA E MÉTODO PARA MONITORAMENTO TÉRMICO EM MANUFATURA ADITIVA",
        help="Deve ser conciso, claro e não conter marcas, nomes fantasia ou adjetivos elogiosos."
    )
    
    campo_invencao = st.text_area(
        "Campo da Invenção",
        placeholder="A presente invenção insere-se no campo da engenharia mecânica e ciência dos materiais, mais especificamente voltada a...",
        help="Delimita o setor técnico de aplicação da invenção.",
        height=120
    )

with aba_contexto:
    st.subheader("Estado da Técnica e Solução Proposta")
    
    estado_tecnica = st.text_area(
        "Estado da Técnica (Soluções Existentes e Gargalos)",
        placeholder="Atualmente, os métodos convencionais utilizam sensores externos que apresentam as seguintes limitações técnicas...",
        help="Descreva o que já existe publicamente e onde as soluções atuais falham.",
        height=180
    )
    
    objetivos_invencao = st.text_area(
        "Objetivos e Vantagens da Invenção",
        placeholder="A presente invenção visa superar as desvantagens citadas propondo um mecanismo que reduz o tempo de resposta em...",
        help="Destaque o problema técnico resolvido e os diferenciais da sua solução.",
        height=150
    )

with aba_detalhes:
    st.subheader("Descrição Técnica e Figuras")
    
    breve_descricao_figuras = st.text_area(
        "Breve Descrição das Figuras (Opcional)",
        placeholder="A Figura 1 apresenta o diagrama de blocos do sistema.\nA Figura 2 ilustra a vista explodida do atuador...",
        help="Liste cada figura e explique sucintamente o que ela ilustra.",
        height=120
    )
    
    descricao_detalhada = st.text_area(
        "Descrição Detalhada da Invenção",
        placeholder="Conforme ilustrado na Figura 1, o sistema compreende uma unidade de processamento (1) conectada a uma pluralidade de sensores (2)...",
        help="O coração da patente. Explique detalhadamente como reproduzir a tecnologia, referenciando as numerações das figuras.",
        height=220
    )
    
    resumo = st.text_area(
        "Resumo",
        placeholder="A presente invenção refere-se a um sistema de monitoramento térmico...",
        help="Texto corrido entre 50 e 250 palavras para indexação em bases de dados.",
        height=120
    )

with aba_revisao:
    st.subheader("Validação Preliminar")
    
    # Verificação de campos obrigatórios vazios
    campos_obrigatorios = {
        "Título": titulo,
        "Campo da Invenção": campo_invencao,
        "Estado da Técnica": estado_tecnica,
        "Objetivos da Invenção": objetivos_invencao,
        "Descrição Detalhada": descricao_detalhada,
        "Resumo": resumo
    }
    
    faltantes = [nome for nome, valor in campos_obrigatorios.items() if not valor.strip()]
    
    if faltantes:
        st.warning(f"Campos obrigatórios ainda não preenchidos: {', '.join(faltantes)}")
    else:
        st.success("Todas as seções obrigatórias foram preenchidas!")
        
    st.markdown("### Resumo Estruturado")
    st.write(f"**Título:** {titulo if titulo else '*(não informado)*'}")
    st.write(f"**Campo da Invenção:** {campo_invencao if campo_invencao else '*(não informado)*'}")
    st.write(f"**Objetivo:** {objetivos_invencao if objetivos_invencao else '*(não informado)*'}")
    
    st.button("Gerar Minuta (.docx)", type="primary", disabled=bool(faltantes))