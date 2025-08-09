import pandas as pd
import numpy as np

# === Dateipfade ===
path_result = "../../TestOutputs/Population.csv"
path_reference = "referenceFile.csv"

# === Optionen ===
sort_columns = True         # Spalten alphabetisch sortieren
tolerance = None            # Beispiel: 1e-8 erlaubt kleine Abweichungen, None = exakt

# === Dateien einlesen (Tab-getrennt) ===
df_result = pd.read_csv(path_result, sep='\t')
df_reference = pd.read_csv(path_reference, sep='\t')

# === Spalten sortieren (optional) ===
if sort_columns:
    df_result = df_result.reindex(sorted(df_result.columns), axis=1)
    df_reference = df_reference.reindex(sorted(df_reference.columns), axis=1)

# === Formate angleichen (z.B. Index zurücksetzen) ===
df_result.reset_index(drop=True, inplace=True)
df_reference.reset_index(drop=True, inplace=True)

# === Formale Vergleichsfunktion ===
def compare_dataframes(df1, df2, tolerance=None):
    if df1.shape != df2.shape:
        print(f"❌ Unterschiedliche Formate: {df1.shape} vs {df2.shape}")
        return False

    unequal_cells = []

    for row in range(df1.shape[0]):
        for col in df1.columns:
            val1 = df1.at[row, col]
            val2 = df2.at[row, col]

            try:
                # numerischer Vergleich mit Toleranz
                if tolerance is not None and pd.notna(val1) and pd.notna(val2):
                    if not np.isclose(val1, val2, atol=tolerance, rtol=tolerance):
                        unequal_cells.append((row, col, val1, val2))
                else:
                    if pd.isna(val1) and pd.isna(val2):
                        continue
                    if val1 != val2:
                        unequal_cells.append((row, col, val1, val2))
            except Exception as e:
                unequal_cells.append((row, col, val1, val2))

    if unequal_cells:
        print(f"❌ {len(unequal_cells)} unterschiedliche Werte gefunden:\n")
        for row, col, val1, val2 in unequal_cells:
            print(f" - Zeile {row}, Spalte '{col}': Referenz = {val2}, Ergebnis = {val1}")
        return False
    else:
        print("✅ Die Dateien stimmen in allen Zellen überein.")
        return True

# === Vergleich durchführen ===
compare_dataframes(df_result, df_reference, tolerance=tolerance)
