from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from help.getChildrens import getChildrens

class Futebol:

    def __init__(self, driver, dutching):
        self.driver = driver
        self.dutching = dutching

        self.GAMES = [
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[2]/div[2]/div/div",
                "name": "Copa"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div/div",
                "name": "Liga Americas"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[6]/div[2]/div/div",
                "name": "Premier"
            },
            {
                "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[1]/div/div[2]/div[7]/div[2]/div/div",
                "name": "Campeões"
            },

        ]

        self.SITE_MAP = {
            "classes": {
                "tempoJogos": "virtuals-event-box__timer",
                "odds": "div.markets__market:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div > div > button > span:nth-child(2)"
            }
        }

    def clicarCorridasPlayFord(self):

        for game in self.GAMES:
            buttonPlayford = self.driver.find_element(By.XPATH, game["xpath"])
            ActionChains(self.driver).move_to_element(buttonPlayford).click(buttonPlayford).perform()
            time.sleep(3)
            jogos = self.pegarTodasCorridas()

            menorPorcentagem = 999999999
            timer = ''
            odds = []

            for jogo in jogos:
                if (jogo['totalPorcentagem'] < menorPorcentagem):
                    menorPorcentagem = jogo['totalPorcentagem']
                    timer = jogo['timer']
                    odds = jogo['porcentagensWinning']

            print(game["name"])
            print(menorPorcentagem)
            print(timer)
            print(*odds, sep='\n')
            print('\n')
            time.sleep(2)



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