# gnc (gross-net-calculator)
CLI for [brutto-netto-rechner.info](https://www.brutto-netto-rechner.info/) using a local personal profile.

## Prerequisites
 - python3
 - requests
 - beautifulsoup4

## Configure
Change `config.py` to contain your personal profile data (explanations in that file).

## Run
```bash
$ ./gnc.py 1234.56
```
...should output something like:

```bash
    1234,00 €    Brutto pro Monat
+      0,00 €    Geldwerter Vorteil

       0,00 €    Solidaritätszuschlag
       0,00 €    Kirchensteuer
       0,00 €    Lohnsteuer
-      0,00 €    Steuern

     114,76 €    Rentenversicherung
      18,51 €    Arbeitslosenversicherung
     103,66 €    Krankenversicherung
      18,82 €    Pflegeversicherung
-    255,75 €    Sozialabgaben

=    978,25 €    Netto pro Monat
```

## Help
```bash
$ ./gnc.py -h
```

