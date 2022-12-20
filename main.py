from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from fp.fp import FreeProxy
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class Spoofer(object):
    def __init__(self, country_id=['US'], rand=True, anonym=True):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self):
        ua = UserAgent()
        proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
        ip = proxy.split("://")[1]
        return ua.random, ip

class Betano:
    def __init__(self):
        self.helperSpoofer = Spoofer()
        self.CHROME_OPTIONS = webdriver.ChromeOptions()
        self.CHROME_OPTIONS.add_experimental_option("detach", True)
        self.CHROME_OPTIONS.add_argument("--no-sandbox");
        self.CHROME_OPTIONS.add_argument("--mute-audio");

        # self.CHROME_OPTIONS.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
        # self.CHROME_OPTIONS.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)

        self.SITE_LINK = "https://br.betano.com/"
        self.SITE_MAP = {
            "buttons": {
                "closeAd": {
                    "xpath": "/html/body/div[1]/div/section[2]/div[7]/div/div/div[1]/button"
                },
                "iniciarSessao": {
                    "xpath": "/html/body/div[1]/div/section[2]/section/header/div[1]/div[2]/div[4]/a[2]"
                },
                "virtuais": {
                    "xpath": "/html/body/div[1]/div/section[2]/section/header/div[1]/div[1]/nav/ul/li[5]/a"
                },
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

        self.PATH = Service("/home/pedro/Downloads/teste/chromedriver")
        self.driver = webdriver.Chrome(service=self.PATH, options=self.CHROME_OPTIONS)
        self.driver.maximize_window()

    def abrirSite(self):
        time.sleep(2)
        self.driver.get(self.SITE_LINK)
        time.sleep(5)

    def fecharAd(self):
        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["closeAd"]["xpath"]).click()
        time.sleep(2)

    def clicarVirtutais(self):
        self.driver.find_element(By.XPATH, self.SITE_MAP["buttons"]["virtuais"]["xpath"]).click()
        time.sleep(3)

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
        print(apostas)
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


    def calculoTotalPorcentagem(self, odds):
        dados = {}

        dados['porcentagensWinning'] = []
        dados['totalPorcentagem'] = 0

        for odd in odds:
            dicionario = {}
            proporcao = 1/odd

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
        dados = self.calculoTotalPorcentagem(odds)
        return dados

betano = Betano()
betano.abrirSite()
betano.fecharAd()
betano.clicarVirtutais()
betano.clicarCorridasPlayFord()
