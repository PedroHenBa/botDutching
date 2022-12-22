
class Dutching:

    def calculoDutching(self, odds):
        dados = {}

        dados['porcentagensWinning'] = []
        dados['totalPorcentagem'] = 0

        for odd in odds:
            dicionario = {}
            proporcao = 1 / odd

            dicionario['porcentagem'] = float("{:.2f}".format(proporcao))
            dicionario['odd'] = odd

            dados['totalPorcentagem'] += proporcao
            dados['porcentagensWinning'].append(dicionario)

        valorRestantePorcentagem = dados['totalPorcentagem'] - 1
        diminuirDeCadaPorcentagem = valorRestantePorcentagem / len(odds)

        for aposta in dados['porcentagensWinning']:
            aposta['porcentagem'] -= diminuirDeCadaPorcentagem
            aposta['valorAposta'] = float("{:.2f}".format(aposta['porcentagem'] * 100))

        return dados