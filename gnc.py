#! /usr/bin/env python3
import argparse
import locale
import requests
from bs4 import BeautifulSoup
import config

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


class GrossToNetCalculator(object):

    def __init__(self, profile):
        self.__url = "https://www.brutto-netto-rechner.info/"
        self.__profile = profile

    def outcome_for(self, monthly_gross):
        """Calculates monthly outcome from gross"""
        params = {**self.__profile, **{"f_bruttolohn": monthly_gross}}
        response = requests.post(self.__url, params)
        html = BeautifulSoup(response.text, 'html.parser')
        return Outcome(html.find("table", attrs={"class": "rechner"}))


class Outcome(object):
    """Provides results of gross-to-net calculation"""

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

    def __str__(self):
        outcome_listing = " {: >12}\t Brutto pro Monat\n".format(
            self.gross_per_month())
        outcome_listing += "+{: >12}\t Geldwerter Vorteil\n\n".format(
            self.non_cash_benefit())
        outcome_listing += " {: >12}\t Solidaritätszuschlag\n".format(
            self.solidarity())
        outcome_listing += " {: >12}\t Kirchensteuer\n".format(
            self.church_tax())
        outcome_listing += " {: >12}\t Lohnsteuer\n".format(self.wage_tax())
        outcome_listing += "-{: >12}\t Steuern\n\n".format(self.taxes())
        outcome_listing += " {: >12}\t Rentenversicherung\n".format(
            self.pension_insurance())
        outcome_listing += " {: >12}\t Arbeitslosenversicherung\n".format(
            self.unemployment_insurance())
        outcome_listing += " {: >12}\t Krankenversicherung\n".format(
            self.health_insurance())
        outcome_listing += " {: >12}\t Pflegeversicherung\n".format(
            self.nursing_care_insurance())
        outcome_listing += "-{: >12}\t Sozialabgaben\n\n".format(
            self.insurances())
        outcome_listing += "={: >12}\t Netto pro Monat".format(
            self.net_per_month())

        return outcome_listing


class Program(object):
    """Wraps main logic to keep __main__ clean"""

    def run(self, profile):
        """Run calculation with user-defined profile"""
        parser = argparse.ArgumentParser(prog="gnc",
                                         description='Convert monthly gross to net.',
                                         epilog="Change calculation params in config.py accordingly.")
        parser.add_argument('gross',
                            metavar="<gross>",
                            type=float,
                            help='monthly gross (in euros)')

        monthly_gross = parser.parse_args().gross

        calculator = GrossToNetCalculator(profile)
        outcome = calculator.outcome_for(monthly_gross)

        print(outcome)


if __name__ == "__main__":
    Program().run(config.PROFILE)
