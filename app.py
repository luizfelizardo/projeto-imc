from flask import Flask, render_template, request

app = Flask(__name__)

# --- Funções de Lógica do IMC ---
def calcular_imc(peso, altura):
    """
    Calcula o Índice de Massa Corporal (IMC).

    Argumentos:
    peso (float): O peso da pessoa em quilogramas (kg).
    altura (float): A altura da pessoa em metros (m).

    Retorna:
    float: O valor do IMC calculado.
    """
    if altura <= 0:
        raise ValueError("A altura deve ser um valor positivo em metros.")
    imc = peso / (altura ** 2)
    return imc

def classificar_imc(imc):
    """
    Classifica o IMC em categorias de peso.

    Argumentos:
    imc (float): O valor do IMC a ser classificado.

    Retorna:
    str: A categoria de peso correspondente ao IMC.
    """
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    elif 30 <= imc < 34.9:
        return "Obesidade Grau I"
    elif 35 <= imc < 39.9:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III (Mórbida)"

def calcular_ajuste_peso(peso_atual, altura):
    """
    Calcula a quantidade de peso a ser ajustada para atingir a faixa de IMC normal.

    Argumentos:
    peso_atual (float): O peso atual da pessoa em quilogramas (kg).
    altura (float): A altura da pessoa em metros (m).

    Retorna:
    str: Uma mensagem com a sugestão de ajuste de peso.
    """
    imc_ideal_min = 18.5
    imc_ideal_max = 24.9

    # Calcula o peso correspondente ao IMC ideal máximo (para quem está acima do peso)
    peso_para_imc_max = imc_ideal_max * (altura ** 2)
    # Calcula o peso correspondente ao IMC ideal mínimo (para quem está abaixo do peso)
    peso_para_imc_min = imc_ideal_min * (altura ** 2)

    imc_atual = calcular_imc(peso_atual, altura) # Recalcula IMC aqui para garantir

    if imc_atual > imc_ideal_max:
        peso_a_perder = peso_atual - peso_para_imc_max
        return f"Para atingir o peso normal (IMC até {imc_ideal_max}), você precisaria perder aproximadamente {peso_a_perder:.2f} kg."
    elif imc_atual < imc_ideal_min:
        peso_a_ganhar = peso_para_imc_min - peso_atual
        return f"Para atingir o peso normal (IMC a partir de {imc_ideal_min}), você precisaria ganhar aproximadamente {peso_a_ganhar:.2f} kg."
    else:
        return "Seu peso já está na faixa considerada normal. Ótimo!"
# --- Fim das Funções de Lógica do IMC ---


@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    """Processa os dados do formulário, calcula o IMC e exibe os resultados."""
    try:
        # Obtém os dados do formulário
        peso_str = request.form['peso']
        altura_str = request.form['altura']

        # Converte para float, tratando vírgulas
        peso = float(peso_str.replace(',', '.'))
        altura = float(altura_str.replace(',', '.'))

        # Executa a lógica de negócio
        imc_calculado = calcular_imc(peso, altura)
        categoria_imc = classificar_imc(imc_calculado)
        sugestao_ajuste = calcular_ajuste_peso(peso, altura)

        # Renderiza a mesma página HTML, passando os resultados para ela
        return render_template(
            'index.html',
            imc=imc_calculado,
            classificacao=categoria_imc,
            ajuste_peso=sugestao_ajuste
        )
    except ValueError as e:
        # Em caso de erro de valor, renderiza a página com uma mensagem de erro
        return render_template('index.html', error=f"Erro de entrada: {e}. Por favor, insira números válidos.")
    except Exception as e:
        # Captura outros erros inesperados
        return render_template('index.html', error=f"Ocorreu um erro inesperado: {e}")

if __name__ == '__main__':
    # Quando você terminar de desenvolver, pode mudar debug=False para o modo de produção
    app.run(debug=True)