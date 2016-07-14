import setuptools


# gemäß der Beschreibung von
# https://packaging.python.org/distributing/
setuptools.setup(
    name="eapi",
    url="https://github.com/pintman/ea_rpi_modul",
    version="0.1.2",
    description="Modul zur Ansteuerung eines EA-Moduls fuer den Raspberry Pi.",
    long_description="Ein Modul zu Ansteuerung eines Eingabe-Ausgabe-Moduls für den Raspberry. Für die Ausgabe dienen LEDs und für die Eingabe Taster. Es kommt im Bildungsbereich zum Einsatz.",
    author="Marco Bakera",
    packages=setuptools.find_packages())


# Mit dem folgenden Befehl kann ein neues Release veröffentlich werden
# python3 setup.py sdist upload
