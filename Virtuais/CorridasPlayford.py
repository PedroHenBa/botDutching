from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from help.getChildrens import getChildrens

class CorridasPlayford:

    def __init__(self, driver, dutching):
        self.driver = driver
        self.dutching = dutching

        self.SITE_MAP = {
            "buttons": {
                "corridaPlayford": {
                    "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[5]/div/div[2]/div[2]/div[2]/div/div/a"
                },
            },
            "classes": {
                "tempoCorridas": "virtuals-event-box__timer",
                "odds": "selections__selection__odd"
            }
        }

    def clicarCorridasPlayFord(self):
        buttonPlayford = self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["corridaPlayford"]["xpath"])
        ActionChains(self.driver).move_to_element(buttonPlayford).click(buttonPlayford).perform()
        time.sleep(5)

        corridas = self.pegarTodasCorridas()
        menorPorcentagem = 999999999
        timer = ''
        odds = []

        for corrida in corridas:
            if(corrida['totalPorcentagem'] < menorPorcentagem):
                menorPorcentagem = corrida['totalPorcentagem']
                timer = corrida['timer']
                odds = corrida['porcentagensWinning']

        print("playford")
        print(menorPorcentagem)
        print(timer)
        print(*odds, sep='\n')
        print('\n')


    def pegarTodasCorridas(self):
        todasCorridas = []
        corridas = self.driver.find_elements(By.CLASS_NAME, self.SITE_MAP["classes"]["tempoCorridas"])

        for corrida in corridas:
            self.driver.execute_script("arguments[0].click();", corrida)
            timer = getChildrens(driver=self.driver, element=corrida)
            time.sleep(2)
            dados = self.pegarTodosElementosOdds()
            dados['timer'] = timer.strip()
            todasCorridas.append(dados)

        return todasCorridas

    def pegarTodosElementosOdds(self):
        elements = self.driver.find_elements(By.CLASS_NAME, self.SITE_MAP["classes"]["odds"])
        odds = []
        for e in elements:
            odd = getChildrens(driver=self.driver, element=e)
            odds.append(float(odd.strip()) - 1)
        dados = self.dutching.calculoDutching(odds)
        return dados