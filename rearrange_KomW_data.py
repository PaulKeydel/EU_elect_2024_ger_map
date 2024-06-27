import pandas as pd

def create_df_KomW24() -> pd.DataFrame:
    df = pd.DataFrame(columns=["AGS", "LKName", "Wahlberechtigte", "Wählende", "Gültige", "LINKE"])

    df_SN24 = pd.read_csv("KW24_SN.csv", header=0, sep=';')
    df_BB24 = pd.read_csv("KW24_BB.csv", header=0, sep=';')
    df_LSA24 = pd.read_csv("KW24_LSA.csv", header=0, sep=';')
    df_MV24 = pd.read_csv("KW24_MV.csv", header=0, sep=';')
    df_SL24 = pd.read_csv("KW24_SL.csv", header=0, sep=';')

    df = pd.concat([df, df_SN24[["WK-Nr", "WK-Name", "Wahlberechtigte", "Wähler", "gültige Stimmen", "DIE LINKE"]].rename(columns={"WK-Nr": "AGS", "WK-Name": "LKName", "Wahlberechtigte": "Wahlberechtigte", "Wähler": "Wählende", "gültige Stimmen": "Gültige", "DIE LINKE": "LINKE"})])
    df = pd.concat([df, df_BB24[["Gebietsschlüssel", "Name des Gebietes", "Wahlberechtigte insgesamt", "Wählende", "Gültige Stimmen", "DIE LINKE"]].rename(columns={"Gebietsschlüssel": "AGS", "Name des Gebietes": "LKName", "Wahlberechtigte insgesamt": "Wahlberechtigte", "Wählende": "Wählende", "Gültige Stimmen": "Gültige", "DIE LINKE": "LINKE"})])
    df = pd.concat([df, df_LSA24[["Schlüsselnummer", "Name", "A - Wahlberechtigte", "B - Wähler", "D - Gültige Stimmen", "D03 - DIE LINKE"]].rename(columns={"Schlüsselnummer": "AGS", "Name": "LKName", "A - Wahlberechtigte": "Wahlberechtigte", "B - Wähler": "Wählende", "D - Gültige Stimmen": "Gültige", "D03 - DIE LINKE": "LINKE"})])
    df = pd.concat([df, df_MV24[["Kreis", "Kreisname", "Wahlberechtigte", "Wähler", "Gültige Stimmen", "DIE LINKE"]].rename(columns={"Kreis": "AGS", "Kreisname": "LKName", "Wahlberechtigte": "Wahlberechtigte", "Wähler": "Wählende", "Gültige Stimmen": "Gültige", "DIE LINKE": "LINKE"})])
    df = pd.concat([df, df_SL24[["Nr", "Gebiet", "Wahlberechtigte", "Wähler", "Gültige", "DIE LINKE"]].rename(columns={"Nr": "AGS", "Gebiet": "LKName", "Wahlberechtigte": "Wahlberechtigte", "Wähler": "Wählende", "Gültige": "Gültige", "DIE LINKE": "LINKE"})])

    #df.loc[len(df)] = [123456, "Tesst", 1, 2, 4, 6]
    return df

if __name__ == "__main__":
    pd_kw24 = create_df_KomW24()
    print(pd_kw24)