import pandas as pd
import os
import re
from fuzzywuzzy import process
import csv

companies_to_keep = [
    "Acciona",
    "Acerinox",
    "Adecco",
    "Akzonobel",
    "Ajinomoto",
    "ACS",
    "Adyen",
    "Aegon",
    "AllHome",
    "Allianz",
    "Aquafil",
    "AmericaMovil",
    "Amadeus IT group",
    "Anglo American",
    "Applus",
    "ASTM",
    "Atlantia",
    "AXA",
    "Barloworld",
    "Berenberg",
    "BHP",
    "BP",
    "BT Group",
    "BuzziUnicem",
    "Bonava",
    "Canacol",
    "Cellnex",
    "Cembre",
    "Cermaq",
    "Cipla",
    "Coloplast",
    "CSL",
    "DNO",
    "DSM",
    "Dundee",
    "Duratex",
    "E.SUN",
    "Empresascopec",
    "Ecopetrol",
    "Enagas",
    "Enav",
    "Ence",
    "Endesa",
    "Enel",
    "ENI",
    "Equinor",
    "ERG",
    "EsaiCo",
    "Essity",
    "EVRAZ",
    "Ferrovial",
    "Feralpi",
    "FILA",
    "Fortum",
    "GVS",
    "Heimstaden",
    "HellasGold",
    "Hess Corp",
    "IAG",
    "Iberdrola",
    "Iberostar",
    "Inditex",
    "Indra",
    "Jakpro",
    "KPN",
    "Legal & General",
    "Leonardo",
    "Lush",
    "megaamc",
    "mapfre",
    "MunichRE",
    "National Grid",
    "NN",
    "Nordgold",
    "Norsk Hydro",
    "NTT",
    "Omron",
    "Orica",
    "Orsted",
    "Palex",
    "Pearson",
    "Petropavlosk",
    "Philipps",
    "Piaggio",
    "PLDT",
    "Prisa",
    "Prudential",
    "Prysmian",
    "RAK",
    "Randstad",
    "Red Electrica",
    "Repsol",
    "Rio Tinto",
    "Royal Unibrew",
    "Ruffino",
    "SAESGetters",
    "San Lorenzo",
    "Schroders",
    "Shell",
    "sumitomo",
    "saipem",
    "Siltronic",
    "Snam",
    "South32",
    "SGR",
    "SSE",
    "sjp",
    "Standard Chartered",
    "Swiss Re",
    "Swisslife",
    "Tasty Bidco",
    "Teck",
    "Telefonica",
    "Telenor",
    "Terna Spa",
    "TIM",
    "TKH",
    "TotalEnergies",
    "Unilever",
    "uniper",
    "Usiminas",
    "Vedanta",
    "Vodafone",
    "Wesfarmers",
    "Yara",
    "SOL",
]


def convert_xlsx_to_csv(xlsx_file_path):
    # Read the XLSX file
    df = pd.read_excel(xlsx_file_path)
    directory_path = os.path.dirname(xlsx_file_path)
    csv_file_path = os.path.join(
        directory_path, os.path.splitext(os.path.basename(xlsx_file_path))[0] + ".csv"
    )
    # Convert to CSV
    df.to_csv(csv_file_path, index=False)


def get_best_match(name, choices, threshold=90):
    best_match = process.extractOne(name, choices, score_cutoff=threshold)
    return best_match[0] if best_match else None


def create_sample_orbis_csv():
    # Read the CSV files
    df_1 = pd.read_csv("collection/data/CbCRs_sample.csv")

    companies_1 = df_1["Company"].unique()
    uploaded_csv_path = "collection/data/orbis_d4g.csv"
    orbis_df = pd.read_csv(uploaded_csv_path)

    # Normalize the names in both the DataFrame and the list for better matching
    orbis_df["name_normalized"] = orbis_df["name"].str.lower()
    choices = orbis_df["name_normalized"].unique()
    companies_to_keep_normalized = [c.lower() for c in companies_to_keep]

    # Find best matches for each company in the list
    matches = {
        company: get_best_match(company, choices)
        for company in companies_to_keep_normalized
    }

    # Filter out None values from matches
    matches_filtered = {k: v for k, v in matches.items() if v is not None}

    # Use the matched names to filter the DataFrame
    filtered_df = orbis_df[orbis_df["name_normalized"].isin(matches_filtered.values())]

    filtered_df.to_csv("collection/data/orbis_d4g_sample.csv", index=False)


def sort_csv_file(input_file_path, output_file_path):
    with open(input_file_path, mode="r", newline="", encoding="utf-8") as infile:
        # Read the CSV file
        reader = csv.reader(infile)
        # Sort the rows by the first column (ignoring case)
        sorted_rows = sorted(reader, key=lambda row: row[0].lower())

    with open(output_file_path, mode="w", newline="", encoding="utf-8") as outfile:
        # Write the sorted data to a new CSV file
        writer = csv.writer(outfile)
        for row in sorted_rows:
            writer.writerow(row)


if __name__ == "__main__":
    # create_sample_orbis_csv()
    sort_csv_file(
        "collection/data/orbis_d4g_sample.csv",
        "collection/data/orbis_d4g_sample_sorted.csv",
    )
