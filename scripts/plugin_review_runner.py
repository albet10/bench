#!/usr/bin/env python3
"""
Plugin Review Runner
Legge il file "plugin review.md" da Google Drive, analizza lo stato dei plugin
e genera un report settimanale in formato tabellare Markdown con suggerimenti.
"""

import os
import json
import sys
from datetime import datetime, date
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PLUGIN_REVIEW_FILE_ID = "1f7tMkDJqOatC5vaGP1UtbIev2CU2uWFx"
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")

PLUGIN_CATALOG = {
    "Operations": {
        "descrizione": "Ottimizza operazioni aziendali: gestione vendor, documentazione processi, compliance.",
        "skills": ["process-doc", "runbook", "vendor-review", "risk-assessment",
                   "compliance-tracking", "status-report", "capacity-plan",
                   "change-request", "process-optimization"],
        "categoria": "Core",
        "soglia_utilizzo_minimo": 3,
    },
    "Productivity": {
        "descrizione": "Gestisce task, pianifica la giornata, mantiene memoria del contesto di lavoro.",
        "skills": ["start", "task-management", "update", "memory-management"],
        "categoria": "Supporto",
        "soglia_utilizzo_minimo": 5,
    },
    "Enterprise Search": {
        "descrizione": "Cerca in tutti gli strumenti aziendali in un'unica query.",
        "skills": ["search", "digest", "source-management"],
        "categoria": "Ricerca",
        "soglia_utilizzo_minimo": 2,
    },
}


def get_drive_service():
    token_json = os.environ.get("GOOGLE_TOKEN_JSON")
    if not token_json:
        raise RuntimeError("Variabile d'ambiente GOOGLE_TOKEN_JSON non trovata.")
    token_data = json.loads(token_json)
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes", ["https://www.googleapis.com/auth/drive.readonly"]),
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build("drive", "v3", credentials=creds)


def read_plugin_review_from_drive():
    service = get_drive_service()
    request = service.files().get_media(fileId=PLUGIN_REVIEW_FILE_ID)
    content = request.execute()
    return content.decode("utf-8") if isinstance(content, bytes) else content


def parse_plugin_states(content: str) -> dict:
    """Estrae stato e utilizzi per ogni plugin dal file Markdown."""
    plugins = {}
    current_plugin = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("## "):
            parts = line.lstrip("#").strip().split(". ", 1)
            current_plugin = parts[-1].strip() if parts else None
            plugins[current_plugin] = {"stato": "Sconosciuto", "utilizzi": 0}
        elif current_plugin and "Installato" in line:
            if "✅" in line:
                plugins[current_plugin]["stato"] = "Installato"
            elif "❌" in line:
                plugins[current_plugin]["stato"] = "Non installato"
        elif current_plugin and "**Utilizzi**" in line:
            try:
                utilizzi = int(line.split("|")[-2].strip())
                plugins[current_plugin]["utilizzi"] = utilizzi
            except (ValueError, IndexError):
                pass
    return plugins


def genera_suggerimenti(plugin_states: dict) -> list:
    """Genera suggerimenti di installazione/disinstallazione per ogni plugin."""
    suggerimenti = []
    for nome, info in plugin_states.items():
        stato = info["stato"]
        utilizzi = info["utilizzi"]
        catalog = PLUGIN_CATALOG.get(nome, {})
        soglia = catalog.get("soglia_utilizzo_minimo", 3)

        if stato == "Non installato":
            suggerimenti.append({
                "plugin": nome,
                "azione": "⚠️ INSTALLA",
                "motivo": f"Plugin non installato — categoria '{catalog.get('categoria', '?')}' utile per le attività settimanali",
            })
        elif stato == "Installato" and utilizzi == 0:
            suggerimenti.append({
                "plugin": nome,
                "azione": "🔍 VALUTA RIMOZIONE",
                "motivo": f"Installato ma con 0 utilizzi questa settimana — considera la disinstallazione se non pianificato",
            })
        elif stato == "Installato" and utilizzi < soglia:
            suggerimenti.append({
                "plugin": nome,
                "azione": "✅ MANTIENI",
                "motivo": f"{utilizzi} utilizzi (soglia: {soglia}) — sottoutilizzato, monitora la prossima settimana",
            })
        else:
            suggerimenti.append({
                "plugin": nome,
                "azione": "✅ MANTIENI",
                "motivo": f"{utilizzi} utilizzi — utilizzo nella norma",
            })
    return suggerimenti


def genera_report(plugin_states: dict, suggerimenti: list, data_report: str) -> str:
    linee = [
        f"# Plugin Review Report — {data_report}",
        "",
        "> Report generato automaticamente ogni sabato alle 15:34.",
        "",
        "---",
        "",
        "## Stato Plugin",
        "",
        "| # | Plugin | Stato | Utilizzi settimana | Categoria | Skills |",
        "|---|--------|-------|--------------------|-----------|--------|",
    ]

    for i, (nome, info) in enumerate(plugin_states.items(), 1):
        catalog = PLUGIN_CATALOG.get(nome, {})
        stato_emoji = "✅ Installato" if info["stato"] == "Installato" else "❌ Non installato"
        skills = ", ".join(f"`{s}`" for s in catalog.get("skills", []))
        categoria = catalog.get("categoria", "—")
        linee.append(
            f"| {i} | **{nome}** | {stato_emoji} | {info['utilizzi']} | {categoria} | {skills} |"
        )

    linee += [
        "",
        "---",
        "",
        "## Suggerimenti Settimanali",
        "",
        "| Plugin | Azione Consigliata | Motivazione |",
        "|--------|--------------------|-------------|",
    ]

    for s in suggerimenti:
        linee.append(f"| **{s['plugin']}** | {s['azione']} | {s['motivo']} |")

    linee += [
        "",
        "---",
        "",
        "## Note",
        "",
        "- La soglia di utilizzo minimo è impostata per plugin in base alla categoria.",
        "- Un plugin installato con 0 utilizzi per 2+ settimane consecutive è candidato alla rimozione.",
        "- I plugin non installati nella categoria **Core** sono da installare con priorità alta.",
        "",
        f"*Generato automaticamente da Claude Code · {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ]

    return "\n".join(linee)


def main():
    data_oggi = date.today().strftime("%Y-%m-%d")
    output_path = os.path.join(REPORTS_DIR, f"plugin_review_{data_oggi}.md")

    print(f"[plugin-review] Lettura file da Google Drive (ID: {PLUGIN_REVIEW_FILE_ID})...")
    try:
        content = read_plugin_review_from_drive()
    except Exception as e:
        print(f"[plugin-review] ERRORE lettura Drive: {e}", file=sys.stderr)
        sys.exit(1)

    plugin_states = parse_plugin_states(content)
    print(f"[plugin-review] Plugin rilevati: {list(plugin_states.keys())}")

    suggerimenti = genera_suggerimenti(plugin_states)
    report = genera_report(plugin_states, suggerimenti, data_oggi)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[plugin-review] Report salvato: {output_path}")
    print("\n" + "=" * 60)
    print(report)


if __name__ == "__main__":
    main()
