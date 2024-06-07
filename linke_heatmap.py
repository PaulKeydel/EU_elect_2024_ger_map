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

avg_eu24 = 0.6

valid_votes = dict([(2019, []), (2024, [])])
abs_votes_linke = dict([(2019, []), (2024, [])])
electorate = dict([(2019, []), (2024, [])])
num_voters = dict([(2019, []), (2024, [])])
diff_votes_linke = []
results_linke_24 = []
for _, row in dfgeo.iterrows():
    ags = int(row["AGS"])
    if not (df_eu19["Nr"] == ags).any():
        print("ERROR: AGS not found in results from 2019!")
    valid_votes[2019].append(df_eu19["Gültige"].loc[df_eu19["Nr"] == ags].item())
    abs_votes_linke[2019].append(df_eu19["DIE LINKE"].loc[df_eu19["Nr"] == ags].item())
    rel_votes_linke_19 = 100 * abs_votes_linke[2019][-1] / valid_votes[2019][-1]
    rel_votes_linke_24 = avg_eu24
    diff_votes_linke.append(rel_votes_linke_24 - rel_votes_linke_19)
    results_linke_24.append(rel_votes_linke_24)
    electorate[2019].append(df_eu19["Wahlberechtigte"].loc[df_eu19["Nr"] == ags].item())
    num_voters[2019].append(df_eu19["Wähler/-innen"].loc[df_eu19["Nr"] == ags].item())
    electorate[2024].append(df_eu19["Wahlberechtigte"].loc[df_eu19["Nr"] == ags].item())
    num_voters[2024].append(df_eu19["Wähler/-innen"].loc[df_eu19["Nr"] == ags].item())
elect_turnout_19 = 100.0 * sum(num_voters[2019]) / sum(electorate[2019])
elect_turnout_24 = 100.0 * sum(num_voters[2024]) / sum(electorate[2024])
avg_eu19 = 100.0 * sum(abs_votes_linke[2019]) / sum(valid_votes[2019])

#print summary
print("Wahlergebnisse DIE LINKE bundesweit:")
print("  EU2019: " + f"{avg_eu19:.2f}" + "%")
print("  EU2024: " + f"{avg_eu24:.2f}" + "%")
print("Wahlbeteiligung DIE LINKE bundesweit:")
print("  EU2024: " + f"{elect_turnout_24:.2f}" + "%")

#add electoral data to the geopraphical dataframe
dfgeo["diff_votes_linke"] = diff_votes_linke
dfgeo["results_linke_24"] = results_linke_24
dfgeo["linke_24_germany"] = [avg_eu24] * len(dfgeo)
dfgeo["election_turnout"] = [100.0 * x / y for x, y in zip(num_voters[2024], electorate[2024])]
dfgeo["turnout_germany"] = [elect_turnout_24] * len(dfgeo)

#reindexing the dataframe in order to achieve a better look
i0 = dfgeo[~dfgeo["AGS"].astype('int').isin(relev_ags)].index
i1 = dfgeo[dfgeo["AGS"].astype('int').isin(relev_ags)].index
dfgeo = dfgeo.reindex(list(i0) + list(i1))
#print(dfgeo)

#plot maps with election results and changes with reference to 2019
fig, axs = plt.subplots(1, 2, figsize=(15, 10))

cn = int(math.ceil(np.nanmax(results_linke_24)))
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
axs[0].set_title("LINKE: Ergebnisse der EU-Wahl 2024 in %")
axs[0].text(5.7, 47, "gesamt DE 2024: " + f"{avg_eu24:.2f}" + "% LINKE, " + f"{elect_turnout_24:.2f}" + "% Wahlbeteiligung")

cn = int(math.ceil(np.nanmax(list(map(abs, diff_votes_linke)))))
dfgeo.plot(
    ax=axs[1],
    alpha=0.7,
    column="diff_votes_linke",
    linewidth=0.1,
    edgecolor="grey",
    categorical=False,
    legend=True,
    cmap="coolwarm", #"seismic"
    norm=mpl.colors.Normalize(vmin=-cn, vmax=cn),
    missing_kwds=dict(color="white")
)
axs[1].set_xticks([])
axs[1].set_yticks([])
axs[1].set_title("LINKE: Gewinne und Verluste zur Wahl 2019 in %")
axs[1].text(5.7, 47, "gesamt DE 2019: " + f"{avg_eu19:.2f}" + "% LINKE, " + f"{elect_turnout_19:.2f}" + "% Wahlbeteiligung")
plt.savefig("Linke_heatmap.pdf", format="pdf", bbox_inches="tight")

#create interactive plot
cn = int(math.ceil(np.nanmax([abs(d - (avg_eu24 - avg_eu19)) for d in diff_votes_linke])))
m = dfgeo.explore(column="diff_votes_linke",
                  tooltip="GEN",
                  tooltip_kwds=dict(labels=False),
                  popup=["BEZ", "GEN", "AGS", "results_linke_24", "diff_votes_linke", "election_turnout", "linke_24_germany", "turnout_germany"],
                  popup_kwds=dict(aliases=["Einheit:", "Name:", "AGS:", "Ergebnis LINKE [%]:", "Unterschied zu 2019 [%]:", "Wahlbeteiligung [%]:", "gesamt LINKE [%]:", "gesamt Wahlbeteiligung [%]:"]),
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