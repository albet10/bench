#!/usr/bin/env python3
"""
Genera file .dsd per stampa batch A1 PDF dei layout AutoCAD.
Eseguire nella stessa cartella dei file .dwg, oppure impostare DWG_FOLDER.
"""

import os
import sys

# ─── CONFIGURAZIONE ──────────────────────────────────────────────────────────
DWG_FOLDER = os.path.dirname(os.path.abspath(__file__))  # stessa cartella dello script

# Plotter PDF installato in AutoCAD (verificare in Plot > Plotter manager)
PDF_PLOTTER = "DWG To PDF.pc3"

# Formato carta A1 – verificare il nome esatto in AutoCAD:
# Plot dialog > Paper size. Usare uno di questi:
PAPER_SIZE = "ISO_expand_A1_(841.00_x_594.00_MM)"
# PAPER_SIZE = "ISO_A1_(841.00_x_594.00_MM)"          # alternativa

# Stile di stampa
PLOT_STYLE = "monochrome.ctb"   # usa "acad.ctb" per colori

# Modalità output PDF:  5 = un PDF per foglio,  6 = un PDF multi-pagina
OUTPUT_TYPE = 5

# Area di stampa: "Extents" cattura tutto, anche fuori dai bordi layout
PLOT_AREA = "Extents"           # oppure "Layout" se vuoi usare i bordi pagina
# ─────────────────────────────────────────────────────────────────────────────

# Mappa file → nome layout (rilevato dai file DWG)
LAYOUT_MAP = {
    "ESASUP_XX_BQ0270.dwg": "Layout2",
    "ESASUP_XX_BQ0271.dwg": "Layout2",
    "ESASUP_XX_BQ0272.dwg": "Layout2",
    "ESASUP_XX_BQ0273.dwg": "Layout",
    "ESASUP_XX_BQ0274.dwg": "Layout2",
}

def make_dsd_single(dwg_path, layout_name, out_dir):
    """Genera un .dsd per singolo DWG → singolo PDF."""
    base = os.path.splitext(os.path.basename(dwg_path))[0]
    dsd_path = os.path.join(out_dir, base + ".dsd")
    pdf_path = os.path.join(out_dir, base + ".pdf")

    with open(dsd_path, "w", encoding="utf-8") as f:
        f.write("[DSD_File_Header]\n")
        f.write("Current DSD version=4\n\n")

        f.write("[DSD Component]\n")
        f.write(f"DWG={dwg_path}\n")
        f.write(f"Layout={layout_name}\n")
        f.write(f"Setup=\n")
        f.write(f"OriginalSheetPath={dwg_path}\n")
        f.write(f"HasPlotSettings=0\n")
        f.write(f"SheetName={base}\n\n")

        f.write("[Plot Device]\n")
        f.write(f"PlotToFile=1\n")
        f.write(f"PC3File={PDF_PLOTTER}\n")
        f.write(f"PaperSize={PAPER_SIZE}\n")
        f.write(f"PlotStyle={PLOT_STYLE}\n")
        f.write(f"UseLastPlotSettings=0\n\n")

        f.write("[DSD Data]\n")
        f.write(f"SheetCount=1\n")
        f.write(f"PromptForDWFName=0\n")
        f.write(f"IncludeLayer=0\n")
        f.write(f"LineMerge=0\n")
        f.write(f"OutputType={OUTPUT_TYPE}\n")
        f.write(f"OUT={pdf_path}\n")
        f.write("PWD=\n")

    return dsd_path


def make_dsd_combined(dwg_entries, out_dir):
    """Genera un unico .dsd con tutti i DWG → un PDF multi-pagina."""
    dsd_path = os.path.join(out_dir, "ESASUP_XX_BATCH.dsd")
    pdf_path = os.path.join(out_dir, "ESASUP_XX_BATCH.pdf")

    with open(dsd_path, "w", encoding="utf-8") as f:
        f.write("[DSD_File_Header]\n")
        f.write("Current DSD version=4\n\n")

        for dwg_path, layout_name in dwg_entries:
            base = os.path.splitext(os.path.basename(dwg_path))[0]
            f.write("[DSD Component]\n")
            f.write(f"DWG={dwg_path}\n")
            f.write(f"Layout={layout_name}\n")
            f.write(f"Setup=\n")
            f.write(f"OriginalSheetPath={dwg_path}\n")
            f.write(f"HasPlotSettings=0\n")
            f.write(f"SheetName={base}\n\n")

        f.write("[Plot Device]\n")
        f.write(f"PlotToFile=1\n")
        f.write(f"PC3File={PDF_PLOTTER}\n")
        f.write(f"PaperSize={PAPER_SIZE}\n")
        f.write(f"PlotStyle={PLOT_STYLE}\n")
        f.write(f"UseLastPlotSettings=0\n\n")

        f.write("[DSD Data]\n")
        f.write(f"SheetCount={len(dwg_entries)}\n")
        f.write(f"PromptForDWFName=0\n")
        f.write(f"IncludeLayer=0\n")
        f.write(f"LineMerge=0\n")
        f.write(f"OutputType=6\n")  # 6 = PDF multi-pagina
        f.write(f"OUT={pdf_path}\n")
        f.write("PWD=\n")

    return dsd_path


if __name__ == "__main__":
    print(f"Cartella DWG: {DWG_FOLDER}")
    print(f"Plotter: {PDF_PLOTTER}")
    print(f"Formato: {PAPER_SIZE}")
    print()

    found = []
    missing = []
    for dwg_name, layout in LAYOUT_MAP.items():
        full = os.path.join(DWG_FOLDER, dwg_name)
        if os.path.isfile(full):
            found.append((full, layout))
        else:
            missing.append(dwg_name)

    if missing:
        print(f"ATTENZIONE: file non trovati in {DWG_FOLDER}:")
        for m in missing:
            print(f"  - {m}")
        print()

    if not found:
        print("Nessun file DWG trovato. Verifica DWG_FOLDER.")
        sys.exit(1)

    out_dir = DWG_FOLDER  # i .dsd vengono creati nella stessa cartella

    # 1. DSD singoli (un PDF per disegno)
    print("Generazione DSD singoli:")
    for dwg_path, layout in found:
        p = make_dsd_single(dwg_path, layout, out_dir)
        print(f"  OK  {os.path.basename(p)}")

    # 2. DSD combinato (un PDF multi-pagina)
    p = make_dsd_combined(found, out_dir)
    print(f"\nGenerazione DSD combinato:")
    print(f"  OK  {os.path.basename(p)}")

    print("\n─────────────────────────────────────────────────────")
    print("COME USARE I FILE DSD IN AUTOCAD:")
    print("  1. Apri AutoCAD")
    print("  2. Digita PUBLISH (o usa File > Pubblica)")
    print("  3. Clicca sul menu a discesa > Carica foglio...")
    print("     e seleziona il file .dsd")
    print("  4. IMPORTANTE per il contenuto fuori layout:")
    print("     Nella finestra PUBLISH, clicca 'Impostazioni pagina'")
    print("     e imposta Area di stampa = Estesi (Extents)")
    print("  5. Clicca Pubblica")
    print()
    print("NOTA: se AutoCAD non trova il plotter 'DWG To PDF.pc3',")
    print("  aprire un DWG, andare in Plot > Plotter > Add-a-Plotter")
    print("  e aggiungere 'DWG to PDF.pc3'.")
