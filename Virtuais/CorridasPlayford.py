from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
from selenium import webdriver

class CorridasPlayford:

    def __init__(self, driver, dutching ):
        self.driver = driver
        self.dutching = dutching

        self.SITE_MAP = {
            "buttons": {
                "corridaPlayford": {
                    "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/div/div/div/div/div[5]/div/div[2]/div[2]/div[2]/div/div/a"
                },
                "corridas": {
                    "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/section/div/div[2]/div[2]/div[1]/div/div/div[1]/div[3]/div/div/div/p[2]"
                }
            },
            "Odds": {
                "buttonCavalos": {
                    "xpath": "/html/body/div[1]/div/section[2]/div[5]/div[2]/section/section/section/div/div[3]/div/div[2]/button[1]/span[2]"
                }
            }
        }

    def clicarCorridasPlayFord(self):
        buttonPlayford = self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["corridaPlayford"]["xpath"])
        action = ActionChains(self.driver)
        ActionChains(self.driver).move_to_element(buttonPlayford).click(buttonPlayford).perform()
        time.sleep(5)
        corridas = self.pegarTodasCorridas()
        menorPorcentagem = 999999999
        timer = ''
        apostas = []

        for corrida in corridas:
            if(corrida['totalPorcentagem'] < menorPorcentagem):
                menorPorcentagem = corrida['totalPorcentagem']
                timer = corrida['timer']
                apostas = corrida['porcentagensWinning']

        print(menorPorcentagem)
        print('\n')
        print(timer)
        print('\n')
        print(*apostas, sep='\n')
        print('\n')


    def pegarTodasCorridas(self):
        todasCorridas = []
        corridas = self.driver.find_elements(By.CLASS_NAME, "virtuals-event-box__timer")

        for corrida in corridas:
            self.driver.execute_script("arguments[0].click();", corrida)
            timer = self.driver.execute_script("""
                        var parent = arguments[0];
                        var child = parent.firstChild;
                        var ret = "";
                        while(child) {
                            if (child.nodeType === Node.TEXT_NODE)
                                ret += child.textContent;
                            child = child.nextSibling;
                        }
                        return ret;
                        """, corrida)
            time.sleep(2)
            dados = self.pegarTodosElementosOdds()
            dados['timer'] = timer.strip()
            todasCorridas.append(dados)
        return todasCorridas

    def pegarTodosElementosOdds(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "selections__selection__odd")
        odds = []
        for e in elements:
            odd = self.driver.execute_script("""
            var parent = arguments[0];
            var child = parent.firstChild;
            var ret = "";
            while(child) {
                if (child.nodeType === Node.TEXT_NODE)
                    ret += child.textContent;
                child = child.nextSibling;
            }
            return ret;
            """, e)
            odds.append(float(odd.strip()) - 1)
        dados = self.dutching.calculoDutching(odds)
        return dados