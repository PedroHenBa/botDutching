
class Dutching:

    def calculoDutching(self, odds):
        dados = {}

        dados['porcentagensWinning'] = []
        dados['totalPorcentagem'] = 0

        for odd in odds:
            dicionario = {}
            proporcao = 1 / odd

            dicionario['odd'] = odd

            dados['totalPorcentagem'] += proporcao
            dados['porcentagensWinning'].append(dicionario)

        return dados