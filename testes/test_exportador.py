from pathlib import Path
from src.core.modelos import DesenhoItem, RelatorioDescritivoPI
from src.exportador.gerador_docx import gerar_relatorio_pi


def executar_teste_geracao():
    print("=" * 60)
    print("Iniciando teste de geração local do Relatório Descritivo (PI)...")
    print("=" * 60)

    # 1. Cria os dados de exemplo correspondentes ao que o template espera
    dados_exemplo = RelatorioDescritivoPI(
        titulo="SISTEMA E MÉTODO INTELIGENTE PARA MONITORAMENTO TÉRMICO EM MANUFATURA ADITIVA",
        campo_da_invencao=(
            "A presente invenção insere-se no campo da engenharia mecânica e computação aplicada, "
            "mais especificamente voltada a sistemas de controle e sensoriamento térmico em tempo "
            "real para processos industriais de manufatura aditiva metálica."
        ),
        estado_da_tecnica=(
            "Atualmente, os processos convencionais de manufatura aditiva utilizam pirômetros ópticos "
            "ou termopares fixos externos. Esses dispositivos apresentam tempo de resposta lento e baixa "
            "resolução espacial, impossibilitando a detecção precoce de zonas de superaquecimento na poça de fusão."
        ),
        problema_e_vantagens=(
            "A presente invenção visa superar as desvantagens citadas propondo uma malha fechada de monitoramento "
            "multiespectral em alta frequência, reduzindo em até 40% a taxa de descarte de peças por empenamento térmico."
        ),
        desenhos=[
            DesenhoItem(
                numero_figura="1",
                descricao_breve="apresenta o diagrama esquemático em blocos do sistema de monitoramento.",
            ),
            DesenhoItem(
                numero_figura="2",
                descricao_breve="ilustra o fluxo operacional do algoritmo de controle térmico preditivo.",
            ),
        ],
        paragrafos_descricao=[
            (
                "Conforme ilustrado na Figura 1, o sistema compreende uma unidade de processamento central (1) "
                "acoplada a uma câmera termográfica multiespectral (2) e um bico extrusor (3)."
            ),
            (
                "A câmera multiespectral (2) captura imagens térmicas da poça de fusão a uma taxa de 500 quadros "
                "por segundo, transmitindo os dados via barramento de alta velocidade para a unidade central (1)."
            ),
            (
                "Em caso de desvio térmico superior a 5% da temperatura de referência, o algoritmo preditivo "
                "ajusta dinamicamente a potência do feixe laser antes da deposição da camada subsequente."
            ),
        ],
        exemplos_concretizacao=(
            "Em uma concretização preferencial da invenção, o módulo sensor foi integrado a uma impressora 3D "
            "do tipo DED (Directed Energy Deposition), operando com liga de titânio Ti-6Al-4V e comprovando a "
            "estabilidade da poça de fusão durante 12 horas consecutivas de operação ininterrupta."
        ),
    )

    # 2. Caminho do arquivo de saída
    caminho_saida = Path(__file__).resolve().parent / "saida_teste_relatorio.docx"

    # 3. Executa a geração
    arquivo_gerado = gerar_relatorio_pi(dados_exemplo, caminho_saida)

    print(f"\n[SUCESSO] Documento gerado com êxito!")
    print(f"Caminho do arquivo: {arquivo_gerado.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    executar_teste_geracao()
