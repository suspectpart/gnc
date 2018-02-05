PROFILE = {
    "f_bruttolohn": 3000.0,                             # default value, ignore
    "f_abrechnungszeitraum": "monat",                   # right now, only "monat".
    "f_geld_werter_vorteil": None,                      # [None|<float>]
    "f_abrechnungsjahr": 2018,                          # yyyy
    "f_steuerfreibetrag": None,                         # [None|<float>]
    "f_steuerklasse": 3,                                # [1-6]
    "f_kirche": "ja",                                   # ["ja"|"nein"]
    "f_bundesland": "baden-wuerttemberg",               # ["bayern"| ... | "schleswig-holstein"| ... |"thueringen"| . .. ]
    "f_alter": 25,                                      # [15-75]
    "f_kinder": "nein",                                 # ["ja"|nein]
    "f_kinderfreibetrag": 0,                            # [0, 0.5, 1, 1.5 ... 6]
    "f_krankenversicherung": "pflichtversichert",       # ["pflichtversichert"|"privat_versichert"|"freiwillig_versichert"]
    "f_private_kv": None,                               # f_krankenversicherung == "privat_versichert" ? <float> : None
    "f_arbeitgeberzuschuss_pkv": "ja",                  # ["ja"|"nein"]
    "f_KVZ": 1.1,                                       # <float>
    "f_rentenversicherung": "pflichtversichert",        # ["pflichtversichert"|"nicht_pflichtversichert"|"ag_pflichtanteil"|"an_pflichtanteil"]
    "f_arbeitslosenversicherung": "pflichtversichert",  # ["pflichtversichert"|"nicht_pflichtversichert"|"ag_pflichtanteil"|"an_pflichtanteil"]
    "ok": 1
}
