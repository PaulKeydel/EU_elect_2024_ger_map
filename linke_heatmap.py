import pandas as pd
import geopandas as gpd
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

#read election results and geographical data
#geodata was taken from https://github.com/jgehrcke/covid-19-germany-gae/tree/master/geodata
dfgeo = gpd.read_file("DE-counties.geojson")
df_eu19 = pd.read_csv("ew19_kerg_mod.csv", header=0, sep=';')
df_eu24 = pd.read_csv("ew24_kerg_mod.csv", header=0, sep=';')
df_SN24 = pd.read_csv("KW24_SN.csv", header=0, sep=';')
df_BB24 = pd.read_csv("KW24_BB.csv", header=0, sep=';')
df_LSA24 = pd.read_csv("KW24_LSA.csv", header=0, sep=';')

#define list of relevant AGS
relev_ags = [6635, #Waldeck-Frankenberg
             6533, #Limburg-Weilburg
             7231, #Bernkastel-Wittlich
             7135, #Cochem-Zell
             7211, #Trier, kreisfreie Stadt
             7232, #Eifelkreis Bitburg-Prüm
             5358, #Düren
             5316, #Leverkusen, Stadt
             5170, #Wesel
             5112, #Duisburg, Stadt
             5913, #Dortmund, Stadt
             5562, #Recklinghausen
             5962, #Märkischer Kreis
             5120, #Remscheid, Stadt
             5122, #Solingen, Klingenstadt
             5124, #Wuppertal, Stadt
             5162, #Rhein-Kreis Neuss
             5515, #Münster, Stadt
             ]

valid_votes = dict([("EU19", []), ("EU24", []), ("KOM24", [])])
abs_votes_linke = dict([("EU19", []), ("EU24", []), ("KOM24", [])])
electorate = dict([("EU19", []), ("EU24", []), ("KOM24", [])])
num_voters = dict([("EU19", []), ("EU24", []), ("KOM24", [])])
diff_votes_linke = []
lost_voters_24 = []
for _, row in dfgeo.iterrows():
    ags = int(row["AGS"])
    assert(ags > 1000)
    if (df_eu19["Nr"] == ags).any():
        valid_votes["EU19"].append(df_eu19["Gültige"].loc[df_eu19["Nr"] == ags].item())
        abs_votes_linke["EU19"].append(df_eu19["DIE LINKE"].loc[df_eu19["Nr"] == ags].item())
        electorate["EU19"].append(df_eu19["Wahlberechtigte"].loc[df_eu19["Nr"] == ags].item())
        num_voters["EU19"].append(df_eu19["Wähler/-innen"].loc[df_eu19["Nr"] == ags].item())
    else:
        print("ERROR: AGS not found in results from 2019!")
    if (df_eu24["Nr"] == ags).any() or (ags == 16056):
        if (ags == 16056):
            #Eisenach ist als ehemalig kreisfreie Stadt in den Wartburgkreis eingemeindet worden
            ags = 16063
        valid_votes["EU24"].append(df_eu24["Gültige Stimmen"].loc[df_eu24["Nr"] == ags].item())
        abs_votes_linke["EU24"].append(df_eu24["DIE LINKE"].loc[df_eu24["Nr"] == ags].item())
        electorate["EU24"].append(df_eu24["Wahlberechtigte"].loc[df_eu24["Nr"] == ags].item())
        num_voters["EU24"].append(df_eu24["Wählende"].loc[df_eu24["Nr"] == ags].item())
    else:
        print("ERROR: AGS not found in results from 2024!")
    if (df_LSA24["Schlüsselnummer"] == ags).any():
        valid_votes["KOM24"].append(df_LSA24["D - Gültige Stimmen"].loc[df_LSA24["Schlüsselnummer"] == ags].item())
        abs_votes_linke["KOM24"].append(df_LSA24["D03 - DIE LINKE"].loc[df_LSA24["Schlüsselnummer"] == ags].item())
        electorate["KOM24"].append(df_LSA24["A - Wahlberechtigte"].loc[df_LSA24["Schlüsselnummer"] == ags].item())
        num_voters["KOM24"].append(df_LSA24["B - Wähler"].loc[df_LSA24["Schlüsselnummer"] == ags].item())
    elif (df_SN24["WK-Nr"] == ags).any():
        valid_votes["KOM24"].append(df_SN24["gültige Stimmen"].loc[df_SN24["WK-Nr"] == ags].item())
        abs_votes_linke["KOM24"].append(df_SN24["DIE LINKE"].loc[df_SN24["WK-Nr"] == ags].item())
        electorate["KOM24"].append(df_SN24["Wahlberechtigte"].loc[df_SN24["WK-Nr"] == ags].item())
        num_voters["KOM24"].append(df_SN24["Wähler"].loc[df_SN24["WK-Nr"] == ags].item())
    elif (df_BB24["Gebietsschlüssel"] == ags).any():
        valid_votes["KOM24"].append(df_BB24["Gültige Stimmen"].loc[df_BB24["Gebietsschlüssel"] == ags].item())
        abs_votes_linke["KOM24"].append(df_BB24["DIE LINKE"].loc[df_BB24["Gebietsschlüssel"] == ags].item())
        electorate["KOM24"].append(df_BB24["Wahlberechtigte insgesamt"].loc[df_BB24["Gebietsschlüssel"] == ags].item())
        num_voters["KOM24"].append(df_BB24["Wählende"].loc[df_BB24["Gebietsschlüssel"] == ags].item())
    else:
        valid_votes["KOM24"].append(np.nan)
        abs_votes_linke["KOM24"].append(np.nan)
        electorate["KOM24"].append(np.nan)
        num_voters["KOM24"].append(np.nan)
    rel_votes_linke_19 = 100 * abs_votes_linke["EU19"][-1] / valid_votes["EU19"][-1]
    rel_votes_linke_24 = 100 * abs_votes_linke["EU24"][-1] / valid_votes["EU24"][-1]
    diff_votes_linke.append(rel_votes_linke_24 - rel_votes_linke_19)
    lost_voters_24.append(num_voters["EU24"][-1] * (rel_votes_linke_24 - rel_votes_linke_19) / 100)
elect_turnout_19 = 100.0 * sum(num_voters["EU19"]) / sum(electorate["EU19"])
elect_turnout_24 = 100.0 * sum(num_voters["EU24"]) / sum(electorate["EU24"])
avg_eu19 = 100.0 * sum(abs_votes_linke["EU19"]) / sum(valid_votes["EU19"])
avg_eu24 = 100.0 * np.nansum(abs_votes_linke["EU24"]) / np.nansum(valid_votes["EU24"])

#print summary
print("Wahlergebnisse DIE LINKE bundesweit:")
print("  EU2019: " + f"{avg_eu19:.2f}" + "%")
print("  EU2024: " + f"{avg_eu24:.2f}" + "%")
print("Wahlbeteiligung DIE LINKE bundesweit:")
print("  EU2019: " + f"{elect_turnout_19:.2f}" + "%")
print("  EU2024: " + f"{elect_turnout_24:.2f}" + "%")
print("Stimmendifferenz in Landkreisen:")
print("  größte: " + f"{max(diff_votes_linke):.2f}" + "% (" + dfgeo["GEN"].iloc[np.argmax(diff_votes_linke)] + ")")
print("  kleinste: " + f"{min(diff_votes_linke):.2f}" + "% (" + dfgeo["GEN"].iloc[np.argmin(diff_votes_linke)] + ")")
print("  Anzahl positive: " + str(sum(np.array(diff_votes_linke) >= 0)))

#add electoral data to the geopraphical dataframe
dfgeo["diff_votes_linke"] = diff_votes_linke
dfgeo["results_linke_24"] = [100 * x / y for x, y in zip(abs_votes_linke["EU24"], valid_votes["EU24"])]
dfgeo["results_linke_kom"] = [100 * x / y for x, y in zip(abs_votes_linke["KOM24"], valid_votes["KOM24"])]
dfgeo["lost_voters_24"] = list(map(round, lost_voters_24))
dfgeo["linke_24_germany"] = [avg_eu24] * len(dfgeo)
dfgeo["election_turnout"] = [100.0 * x / y for x, y in zip(num_voters["EU24"], electorate["EU24"])]
dfgeo["turnout_germany"] = [elect_turnout_24] * len(dfgeo)

#reindexing the dataframe in order to achieve a better look
i0 = dfgeo[~dfgeo["AGS"].astype('int').isin(relev_ags)].index
i1 = dfgeo[dfgeo["AGS"].astype('int').isin(relev_ags)].index
dfgeo = dfgeo.reindex(list(i0) + list(i1))
#print(dfgeo)

#plot maps with election results and changes with reference to 2019
def plot_maps_to_file(plot_mode: int, title_left, title_right, text_left = "", text_right = ""):
    assert(plot_mode == 0 or plot_mode == 1)
    fig, axs = plt.subplots(1, 2, figsize=(15, 10))

    cn = int(math.ceil(np.nanmax(dfgeo["results_linke_24"])))
    dfgeo.plot(
        ax=axs[0],
        alpha=0.7,
        column="results_linke_24",
        linewidth=0.1,
        edgecolor="grey",
        categorical=False,
        legend=True,
        cmap="Reds",
        norm=mpl.colors.Normalize(vmin=0, vmax=cn),
        missing_kwds=dict(color="white")
    )
    axs[0].set_xticks([])
    axs[0].set_yticks([])
    axs[0].set_title(title_left)
    axs[0].text(5.7, 47, text_left)

    col_name = "diff_votes_linke" if plot_mode==0 else "results_linke_kom"
    cn = int(math.ceil(np.nanmax(abs(dfgeo[col_name]))))
    vmin = -cn if plot_mode==0 else 0
    cmap = "coolwarm" if plot_mode==0 else "PuRd"
    dfgeo.plot(
        ax=axs[1],
        alpha=0.7,
        column=col_name,
        linewidth=0.1,
        edgecolor="grey",
        categorical=False,
        legend=True,
        cmap=cmap, #"seismic"
        norm=mpl.colors.Normalize(vmin=vmin, vmax=cn),
        missing_kwds=dict(color="white")
    )
    axs[1].set_xticks([])
    axs[1].set_yticks([])
    axs[1].set_title(title_right)
    axs[1].text(5.7, 47, text_right)

    f_name_pdf = "Linke_heatmap.pdf" if plot_mode==0 else "Linke_heatmap_komm.pdf"
    f_name_svg = "Linke_heatmap.svg" if plot_mode==0 else "Linke_heatmap_komm.svg"
    plt.savefig(f_name_pdf, format="pdf", bbox_inches="tight")
    plt.savefig(f_name_svg, format="svg", bbox_inches="tight")

plot_maps_to_file(plot_mode=0,
                  title_left="LINKE: Ergebnisse der EU-Wahl 2024 in %",
                  title_right="LINKE: Gewinne und Verluste zur Wahl 2019 in %",
                  text_left="gesamt DE 2024: " + f"{avg_eu24:.2f}" + "% LINKE, " + f"{elect_turnout_24:.2f}" + "% Wahlbeteiligung",
                  text_right="gesamt DE 2019: " + f"{avg_eu19:.2f}" + "% LINKE, " + f"{elect_turnout_19:.2f}" + "% Wahlbeteiligung")
plot_maps_to_file(plot_mode=1,
                  title_left="LINKE: Ergebnisse der EU-Wahl 2024 in %",
                  title_right="LINKE: Ergebnisse der Kommunal-Wahlen 2024 in %")

#create interactive plot
cn = int(math.ceil(np.nanmax([abs(d - (avg_eu24 - avg_eu19)) for d in diff_votes_linke])))
m = dfgeo.explore(column="diff_votes_linke",
                  tooltip="GEN",
                  tooltip_kwds=dict(labels=False),
                  popup=["BEZ", "GEN", "AGS", "results_linke_24", "diff_votes_linke", "election_turnout", "lost_voters_24", "linke_24_germany", "turnout_germany"],
                  popup_kwds=dict(aliases=["Einheit:", "Name:", "AGS:", "Ergebnis LINKE [%]:", "Unterschied zu 2019 [%]:", "Wahlbeteiligung [%]:", "Wähler gewonnen/verloren:", "gesamt LINKE [%]:", "gesamt Wahlbeteiligung [%]:"]),
                  categorical=False,
                  legend=True,
                  cmap="coolwarm",
                  vmin=-cn + (avg_eu24 - avg_eu19),
                  vmax=cn + (avg_eu24 - avg_eu19),
                  missing_kwds=dict(color="white"),
                  style_kwds=dict(style_function=lambda x: {"color":"black" if int(x["properties"]["AGS"]) in relev_ags else "white",
                                                            "weight":2 if int(x["properties"]["AGS"]) in relev_ags else 1}),
                  legend_kwds=dict(caption="LINKE: Unterschied zu 2019, zentriert um den mittleren Verlust [" + f"{(avg_eu24 - avg_eu19):.2f}" + "%]"))
#m.save("auswertung_gesamt.html")
m.save("index.html")