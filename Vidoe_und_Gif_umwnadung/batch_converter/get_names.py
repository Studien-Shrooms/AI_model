import os

def list_all_files(folder_path, output_file="dateiliste.txt"):
    # Hol dir alle Dateinamen im Ordner
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files.sort()  # alphabetisch sortieren (optional)

    # In Datei schreiben
    with open(output_file, "w", encoding="utf-8") as out_file:
        for filename in files:
            out_file.write(filename + "\n")
            print(filename)

    print(f"\n✅ {len(files)} Dateien aus '{folder_path}' wurden in '{output_file}' gespeichert.")

# ==== HIER STARTEN ====
if __name__ == "__main__":
    folder_path = r"C:\Users\charl\AI_model\Vidoe_und_Gif_umwnadung\batch_converter\output_batch_collage"  # <<<<< DEIN ORDNER HIER
    output_file = r"C:\Users\charl\AI_model\Vidoe_und_Gif_umwnadung\batch_converter\dateiliste.txt"

    list_all_files(folder_path, output_file)
