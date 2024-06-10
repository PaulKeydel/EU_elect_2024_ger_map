# EU_elect_2024_ger_map
Ein kleines Python-Projekt zur geografischen Auswertung der LINKEn Wahlergebnisse bei der Europawahl 2024. Gewinne und Verluste der Partei zwischen der Europawahl 2019 und 2024 sind auf einer (interaktiven) Karte dargestellt - auf Ebene der Landkreise und kreisfreien Städte.

## Wahlergebnisse auf Landkreisebene
Zur Europawahl 2024 hat DIE LINKE im Vergleich zur letzten EU-Wahl in fast allen Landkreisen und kreisfreien Städten verloren. Einzig in Mainz ist ein minimaler Zugewinn von 0.3% der Stimmen zu beobachten. Den größten Verlust (-13%) verzeichnet Suhl. Ein Überblick über die Wahlergebnisse der Partei und über die prozentualen Verluste in den einzelnen Landkreisen:
![Ergebnisse 2024 und Verluste](https://github.com/PaulKeydel/EU_elect_2024_ger_map/blob/main/Linke_heatmap.svg)

## Interaktive Karte
Auf einer [interaktiven Karte](https://paulkeydel.github.io/EU_elect_2024_ger_map/index.html) sind weitere Unterschiede zur letzten Wahl dargestellt. Die schwarz umrandeten Landkreise markieren wo der LINKE EU-Bus den Wahlkampf unterstützt hat. Die Farbcodierung der lokalen Verluste ist in dieser Karte nicht bei null zentriert, sondern um den mittleren bundesdeutschen Verlust von -2,75% (EU-2019: 5,5%, EU-2024: 2,75%). Damit werden diejenigen Landkreise und kreisfreie Städte rötlich eingefärbt, die weniger Stimmen verloren haben als es im bundesdeutschen Mittel der Fall ist.

## Datenquellen
* [Wahlergebnisse 2019](https://www.bundeswahlleiterin.de/dam/jcr/095b092a-780e-45e1-aca9-caafe903b126/ew19_kerg.csv)
* [Wahlergebnisse 2024](https://www.bundeswahlleiterin.de/dam/jcr/ac86fe50-a479-4f3d-bfc1-96b007c1a66d/ew24_kerg.csv)
* [geografischer Datensatz](https://github.com/jgehrcke/covid-19-germany-gae/tree/master/geodata)