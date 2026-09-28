from pathlib import Path
from PIL import Image, ImageDraw
from src.core.modelos import (
    DesenhoItem,
    PatentePICompleta,
    ReivindicacaoItem,
    RelatorioDescritivoPI,
    ResumoPI,
)
from src.exportador.gerador_docx import gerar_pacote_completo_pi

def criar_imagem_mock(caminho: Path):
    """Cria uma imagem simples com moldura para testar a inserção de figuras."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 580, 380], outline="black", width=3)
    draw.text((200, 190), "MOCK DE FIGURA 1 - INPI", fill="black")
    img.save(caminho)

def main():
    print("=" * 60)
    print("TESTE LOCAL: GERAÇÃO DO PACOTE COMPLETO DE PATENTE (PI)")
    print("=" * 60)

    # 1. Cria uma imagem de teste
    caminho_imagem = Path("testes/temp_figura_1.png")
    criar_imagem_mock(caminho_imagem)

    # 2. Monta o objeto completo PatentePICompleta
    patente = PatentePICompleta(
        relatorio=RelatorioDescritivoPI(
            titulo="SISTEMA INTELIGENTE DE CONTROLE TÉRMICO EM MANUFATURA ADITIVA",
            campo_da_invencao="Engenharia mecânica e ciência dos materiais aplicada à manufatura aditiva.",
            estado_da_tecnica="Processos convencionais apresentam tempo de resposta lento gerando descarte de peças.",
            problema_e_vantagens="A invenção reduz defeitos térmicos em até 40% usando sensoriamento em malha fechada.",
            desenhos=[
                DesenhoItem(numero_figura="1", caminho_imagem=str(caminho_imagem), descricao_breve="apresenta o diagrama em blocos.")
            ],
            paragrafos_descricao=[
                "Conforme ilustrado na Figura 1, o sistema compreende uma unidade de processamento central (1).",
                "O sensor térmico transmite dados a 500 Hz para o módulo de controle."
            ],
            exemplos_concretizacao="Em um ensaio de 12 horas com liga de titânio Ti-6Al-4V, a estabilidade foi de 99,8%."
        ),
        quadro_reivindicatorio=[
            ReivindicacaoItem(
                numero=1,
                tipo="independente",
                preambulo="SISTEMA INTELIGENTE DE CONTROLE TÉRMICO EM MANUFATURA ADITIVA",
                caracterizacao="compreender um sensor óptico de alta frequência acoplado a um controlador adaptativo de malha fechada"
            ),
            ReivindicacaoItem(
                numero=2,
                tipo="dependente",
                dependencia=1,
                preambulo="SISTEMA INTELIGENTE DE CONTROLE TÉRMICO",
                caracterizacao="o sensor óptico operar em uma taxa de amostragem de pelo menos 500 Hz"
            )
        ],
        desenhos=[
            DesenhoItem(numero_figura="1", caminho_imagem=str(caminho_imagem))
        ],
        resumo=ResumoPI(
            titulo="SISTEMA INTELIGENTE DE CONTROLE TÉRMICO EM MANUFATURA ADITIVA",
            texto=(
                "A presente invenção refere-se a um sistema inteligente de controle térmico "
                "aplicado à manufatura aditiva metálica. O sistema introduz um mecanismo em "
                "malha fechada capaz de monitorar em tempo real a temperatura da poça de fusão "
                "por meio de sensoriamento óptico de alta frequência acoplado a um atuador. "
                "Diferencia-se do estado da técnica por corrigir dinamicamente variações térmicas "
                "antes da deposição da camada subsequente, garantindo integridade estrutural e "
                "reduzindo drasticamente a taxa de refugo em peças aeroespaciais de titânio."
            )
        )
    )

    # 3. Executa a geração do pacote na pasta 'testes/saida_pacote_pi'
    pasta_saida = Path("testes/saida_pacote_pi")
    resultados = gerar_pacote_completo_pi(
        patente=patente,
        pasta_destino=pasta_saida,
        exportar_pdf=False,  # Mude para True se já instalou o docx2pdf e tem o Word
        criar_zip=True
    )

    print("\n[SUCESSO] Pacote gerado!")
    for nome, caminho in resultados.items():
        print(f" -> {nome}: {caminho}")

if __name__ == "__main__":
    main()