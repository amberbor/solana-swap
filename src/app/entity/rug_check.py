from src.custom_logger import logger


class RugCheckEntity:

    def __init__(self, response):
        try:
            if response.status_code != 200:
                self.pass_checks = False

            self.holders = response.get("topHolders", [])
            self.nr_holders = len(self.holders)

            risks = response.get("risks")
            self.risks = risks
            self.risk_danger = False
            self.risk_warn = False
            for i in risks:
                level = i.get("level")
                if level == "danger":
                    self.risk_danger == True
                elif level == "warn":
                    self.risk_warn == True
            self.risk_score = response.get("score")

            self.pass_checks = True
            if self.nr_holders > 3 or self.risk_danger or self.risk_warn:
                self.pass_checks = False

        except Exception as e:
            logger.error(f"Rug Check Error: {e}")
