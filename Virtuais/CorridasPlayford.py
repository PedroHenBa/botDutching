class CorddiasPlayford:

    def __init__(self, driver):
        self.driver = driver

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
