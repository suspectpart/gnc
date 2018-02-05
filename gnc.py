#! /usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')


class GrossToNet(object):

    def __init__(self):
        self.__url = "https://www.brutto-netto-rechner.info/"

    def calculate_for(self, params):
        response = requests.post(self.__url, params)
        html = BeautifulSoup(response.text, 'html.parser')
        return Result(html.find("table", attrs={"class": "rechner"}))


class Result(object):

    def __init__(self, html):
        self.__html = html

    def gross_per_month(self):
        return self.__get_amount_from_row(2)

    def non_cash_benefit(self):
        return self.__get_amount_from_row(3)

    def church_tax(self):
        return self.__get_amount_from_row(7)

    def solidarity(self):
        return self.__get_amount_from_row(6)

    def wage_tax(self):
        return self.__get_amount_from_row(8)

    def pension_insurance(self):
        return self.__get_amount_from_row(13)

    def unemployment_insurance(self):
        return self.__get_amount_from_row(15)
    
    def health_insurance(self):
        return self.__get_amount_from_row(16)

    def nursing_care_insurance(self):
        return self.__get_amount_from_row(17)
    
    def taxes(self):
        return self.wage_tax() + self.church_tax() + self.solidarity()

    def insurances(self):
        return self.pension_insurance() + self.unemployment_insurance() + self.health_insurance() + self.nursing_care_insurance()

    def net_per_month(self):
        return self.__get_amount_from_row(21)

    def __get_amount_from_row(self, row_num):
        raw_value = str(self.__html.find_all("tr")[row_num].find(
            "td", attrs={"class": "right_column"}).text)
        return locale.atof(raw_value.strip().strip("€"))


params = {
    "f_bruttolohn": 3000,
    "f_abrechnungszeitraum": "monat",
    "f_geld_werter_vorteil": None,
    "f_abrechnungsjahr": "2018",
    "f_steuerfreibetrag": None,
    "f_steuerklasse": 3,
    "f_kirche": "ja",
    "f_bundesland": "baden-wuerttemberg",
    "f_alter": 25,
    "f_kinder": "nein",
    "f_kinderfreibetrag": 0,
    "f_krankenversicherung": "pflichtversichert",
    "f_private_kv": None,
    "f_arbeitgeberzuschuss_pkv": "ja",
    "f_KVZ": 1.1,
    "f_rentenversicherung": "pflichtversichert",
    "f_arbeitslosenversicherung": "pflichtversichert",
    "ok": 1
}

if __name__ == "__main__":
    result = GrossToNet().calculate_for(params)
    print("Brutto pro Monat: %s" % locale.currency(result.gross_per_month()))
    print("Geldwerter Vorteil: %s" % locale.currency(result.solidarity()))
    print("Solidaritätszuschlag: %s" % locale.currency(result.solidarity()))
    print("Kirchensteuer: %s" % locale.currency(result.church_tax()))
    print("Lohnsteuer: %s" % locale.currency(result.wage_tax()))
    print("Steuern: %s" % locale.currency(result.taxes()))
    print("Rentenversicherung: %s" % locale.currency(result.pension_insurance()))
    print("Arbeitslosenversicherung: %s" % locale.currency(result.unemployment_insurance()))
    print("Krankenversicherung: %s" % locale.currency(result.health_insurance()))
    print("Pflegeversicherung: %s" % locale.currency(result.nursing_care_insurance()))
    print("Sozialabgaben: %s" % locale.currency(result.insurances()))
    print("Netto pro Monat: %s" % locale.currency(result.net_per_month()))
