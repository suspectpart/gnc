#! /usr/bin/env python3
import argparse
import locale
import requests
from config import config
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'de_DE.UTF8')


class Euros(object):
    """Represents Euros, formats them nicely"""

    def __init__(self, amount):
        self.__amount = amount

    def amount(self):
        """Numeric Euros amount"""
        return self.__amount

    def __str__(self):
        return locale.currency(self.__amount)

    def __repr__(self):
        return self.__str__()

    def __format__(self, format_spec):
        return format(str(self), format_spec)


class GrossToNet(object):

    def __init__(self, config):
        self.__url = "https://www.brutto-netto-rechner.info/"
        self.__config = config

    def calculate_for(self, monthly_gross):
        """Calculates monthly net from monthly gross"""
        params = {**self.__config, **{"f_bruttolohn": monthly_gross}}
        response = requests.post(self.__url, params)
        html = BeautifulSoup(response.text, 'html.parser')
        return Outcome(html.find("table", attrs={"class": "rechner"}))


class Outcome(object):

    def __init__(self, html):
        self.__html = html

    def gross_per_month(self):
        """Brutto (pro Monat)"""
        return self.__get_amount_from_row(2)

    def non_cash_benefit(self):
        """Geldwerter Vorteil"""
        return self.__get_amount_from_row(3)

    def church_tax(self):
        """Kirchensteuer"""
        return self.__get_amount_from_row(7)

    def solidarity(self):
        """Solidaritätszuschlag"""
        return self.__get_amount_from_row(6)

    def wage_tax(self):
        """Lohnsteuer"""
        return self.__get_amount_from_row(8)

    def taxes(self):
        """Gesamtsteuern (Lohnsteuer + Kirchensteuer + Solidaritätszuschlag)"""
        return self.__get_amount_from_row(10)

    def pension_insurance(self):
        """Rentenversicherung"""
        return self.__get_amount_from_row(13)

    def unemployment_insurance(self):
        """Arbeitslosenversicherung"""
        return self.__get_amount_from_row(15)

    def health_insurance(self):
        """Krankenversicherung"""
        return self.__get_amount_from_row(16)

    def nursing_care_insurance(self):
        """Pflegeversicherung"""
        return self.__get_amount_from_row(17)

    def insurances(self):
        """Sozialabgaben"""
        return self.__get_amount_from_row(19)

    def net_per_month(self):
        """Netto (pro Monat)"""
        return self.__get_amount_from_row(21)

    def __get_amount_from_row(self, row_num):
        row = self.__html.find_all("tr")[row_num]
        amount = row.find("td", attrs={"class": "right_column"}).text
        return Euros(locale.atof(str(amount).strip().strip("€")))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="gnc",
                                     description='Convert monthly gross to net.',
                                     epilog="Change calculation params in config.py accordingly.")
    parser.add_argument('gross',
                        metavar="<gross>",
                        type=int,
                        help='monthly gross (in euros)')

    monthly_gross = parser.parse_args().gross

    result = GrossToNet(config).calculate_for(monthly_gross)

    print(" {: >12}\t Brutto pro Monat".format(result.gross_per_month()))
    print("+{: >12}\t Geldwerter Vorteil\n".format(result.non_cash_benefit()))
    print(" {: >12}\t Solidaritätszuschlag".format(result.solidarity()))
    print(" {: >12}\t Kirchensteuer".format(result.church_tax()))
    print(" {: >12}\t Lohnsteuer".format(result.wage_tax()))
    print("-{: >12}\t Steuern\n".format(result.taxes()))
    print(" {: >12}\t Rentenversicherung".format(result.pension_insurance()))
    print(" {: >12}\t Arbeitslosenversicherung".format(
        result.unemployment_insurance()))
    print(" {: >12}\t Krankenversicherung".format(result.health_insurance()))
    print(" {: >12}\t Pflegeversicherung".format(
        result.nursing_care_insurance()))
    print("-{: >12}\t Sozialabgaben\n".format(result.insurances()))
    print("={: >12}\t Netto pro Monat".format(result.net_per_month()))
