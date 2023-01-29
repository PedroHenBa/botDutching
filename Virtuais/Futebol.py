from requests import Response
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from help.getChildrens import getChildrens
import requests
import json

class Futebol:

    def __init__(self, driver, dutching):
        self.driver = driver
        self.dutching = dutching

        self.GAMES = [
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[4]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div",
                "name": "Copa"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[4]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div/div",
                "name": "Liga Americas"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[4]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[6]/div[2]/div/div",
                "name": "Premier"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[4]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[7]/div[2]/div/div",
                "name": "Campeões"
            },
        ]

        self.SITE_MAP = {
            "classes": {
                "tempoJogos": "virtuals-event-box__timer",
                "odds": "div.markets__market:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div > div > button > span:nth-child(2)"
            }
        }


    def retornaMelhorJogo(self, jogos):

        melhorOdd = {
            "name": '',
            "totalPorcentagem": 99999999,
            "timer": '',
            "porcentagensWinning": '',
            "valorApostaTotal": ''
        }

        for jogo in jogos:
            if jogo['totalPorcentagem'] < melhorOdd['totalPorcentagem']:
                melhorOdd['totalPorcentagem'] = jogo['totalPorcentagem']
                melhorOdd['timer'] = jogo['timer']
                melhorOdd['porcentagensWinning'] = jogo['porcentagensWinning']
                melhorOdd['valorApostaTotal'] = jogo['valorApostaTotal']
                if "name" in jogo:
                    melhorOdd['name'] = jogo['name']
                else:
                    melhorOdd['name'] = ''

        return melhorOdd

    def clicarCorridasPlayFord(self):
        valorApostaGratis = 60

        melhoresJogos = []

        for game in self.GAMES:
            buttonPlayford = self.driver.find_element(By.XPATH, game["xpath"])
            ActionChains(self.driver).move_to_element(buttonPlayford).click(buttonPlayford).perform()
            time.sleep(3)
            jogos = self.pegarTodasCorridas()

            melhorOdd = self.retornaMelhorJogo(jogos)
            melhorOdd['name'] = game['name']

            melhoresJogos.append(melhorOdd)
            time.sleep(2)

        bestGame = self.retornaMelhorJogo(melhoresJogos)
        get = "value=" + str(valorApostaGratis) + "&"

        for gameEscolhido in bestGame['porcentagensWinning']:
            get += "&odds[]="+str(gameEscolhido["odd"])

        get += "&global_com=6.5&same_market=true&"

        for i in range(1, len(bestGame['porcentagensWinning']) + 1):
            get += "ids[]=value" + str(i) + "&"


        res = requests.get('https://www.academiadasapostasbrasil.com/calculator/calc_dutching?' + get)

        results = json.loads(res.text)

        finalResult = {
            'name': '',
            'profit': 0,
            'apostas': [],
            'timer': '',
            'totalPorcentagem': ''
        }


        for i in range(1, len(bestGame['porcentagensWinning']) + 1):
            value = "#value" + str(i)
            finalResult['apostas'].append({'valor': results['values'][value], 'odd': bestGame['porcentagensWinning'][i-1]['odd']})

        finalResult['profit'] = results['profit_value']
        finalResult['timer'] = bestGame['timer']
        finalResult['totalPorcentagem'] = bestGame['totalPorcentagem']
        finalResult['name'] = bestGame['name']

        porcentagemDeGanho = (100 * (finalResult['profit'] + valorApostaGratis)) / valorApostaGratis


        print("nome: " + finalResult['name'])
        print("tempo: " + str(finalResult['timer']))
        print("total perdido: " + str(finalResult['profit']))
        print("porcentagem do valor total: " + str(porcentagemDeGanho))
        print(*finalResult['apostas'], sep='\n')
        print('\n')



    def pegarTodasCorridas(self):
        todasCorridas = []
        corridas = self.driver.find_elements(By.CLASS_NAME, self.SITE_MAP["classes"]["tempoJogos"])

        for corrida in corridas:
            self.driver.execute_script("arguments[0].click();", corrida)
            timer = getChildrens(driver=self.driver, element=corrida)
            time.sleep(2)
            dados = self.pegarTodosElementosOdds()
            dados['timer'] = timer.strip()
            todasCorridas.append(dados)

        return todasCorridas

    def pegarTodosElementosOdds(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR, self.SITE_MAP["classes"]["odds"])
        odds = []
        for e in elements:
            odd = getChildrens(driver=self.driver, element=e)
            odds.append(float(odd.strip()) - 1)
        dados = self.dutching.calculoDutching(odds)

        return dados