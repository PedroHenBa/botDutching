
class Dutching:

    def calculoDutching(self, odds):
        dados = {}

        dados['porcentagensWinning'] = []
        dados['totalPorcentagem'] = 0

        for odd in odds:
            dicionario = {}
            proporcao = 1 / odd

            dicionario['odd'] = odd
            dicionario['porcentagem'] = proporcao

            dados['totalPorcentagem'] += proporcao
            dados['porcentagensWinning'].append(dicionario)

        dados['valorApostaTotal'] = 0
        for dadosOdd in dados['porcentagensWinning']:
            dadosOdd['valorAposta'] = float("{:.2f}".format((dadosOdd['porcentagem'] / dados['totalPorcentagem']) * 100))
            dados['valorApostaTotal'] += dadosOdd['valorAposta']


        return dados