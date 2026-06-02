"""Email composer and sender via Gmail API."""

import base64
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from .auth import get_credentials
from .recipes import CATEGORIES, Recipe

DAYS_IT = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
MONTHS_IT = [
    "", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]


def send_weekly_email(
    plan: dict[date, Recipe],
    shopping: dict[str, list[tuple[str, str]]],
    schedule: dict[date, bool],
    recipient: str,
) -> None:
    """Build and send the weekly dinner plan email via Gmail API."""
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    dates = sorted(plan.keys())
    week_label = f"{dates[0].day} {MONTHS_IT[dates[0].month]} – {dates[-1].day} {MONTHS_IT[dates[-1].month]} {dates[-1].year}"

    subject = f"Piano cene settimanale 🌿 {week_label}"
    html = _build_html(plan, shopping, schedule, week_label)
    plain = _build_plain(plan, shopping, schedule, week_label)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = "me"
    msg["To"] = recipient
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()


def _day_label(d: date, has_appointment: bool) -> str:
    label = f"{DAYS_IT[d.weekday()]} {d.day} {MONTHS_IT[d.month]}"
    if has_appointment:
        label += " 📅"
    return label


def _build_html(
    plan: dict[date, Recipe],
    shopping: dict[str, list[tuple[str, str]]],
    schedule: dict[date, bool],
    week_label: str,
) -> str:
    dates = sorted(plan.keys())

    rows = ""
    for d in dates:
        recipe = plan[d]
        has_appt = schedule.get(d, False)
        bg = "#fff9f0" if has_appt else "#ffffff"
        tag = ""
        if has_appt:
            tag = '<span style="font-size:11px;background:#ff6b35;color:white;padding:2px 6px;border-radius:10px;margin-left:6px">⚡ ≤15 min</span>'
        veg_badge = "" if recipe.is_vegetarian else '<span style="font-size:11px;background:#4a90d9;color:white;padding:2px 6px;border-radius:10px;margin-left:4px">🐟</span>'
        rows += f"""
        <tr style="background:{bg}">
          <td style="padding:10px 16px;font-weight:600;white-space:nowrap">{_day_label(d, has_appt)}{tag}</td>
          <td style="padding:10px 16px">{recipe.name}{veg_badge}
            <span style="color:#888;font-size:12px;margin-left:8px">({recipe.prep_time_min} min)</span>
          </td>
        </tr>"""

    recipe_cards = ""
    for d in dates:
        recipe = plan[d]
        ingredients_html = "".join(
            f"<li><strong>{ing.name}</strong>: {ing.quantity}</li>"
            for ing in recipe.ingredients
        )
        steps_html = "".join(
            f"<li>{step}</li>" for step in recipe.instructions
        )
        recipe_cards += f"""
        <div style="margin-bottom:24px;padding:20px;border:1px solid #e0e0e0;border-radius:8px;background:#fafafa">
          <h3 style="margin:0 0 4px;color:#2c5f2e">{recipe.name}</h3>
          <p style="margin:0 0 12px;color:#666;font-size:13px">
            {'🌿 Vegetariana' if recipe.is_vegetarian else '🐟 Non vegetariana'} &nbsp;·&nbsp;
            ⏱ {recipe.prep_time_min} minuti &nbsp;·&nbsp; 👥 2 persone
          </p>
          <h4 style="margin:0 0 6px;color:#555">Ingredienti</h4>
          <ul style="margin:0 0 12px;padding-left:20px">{ingredients_html}</ul>
          <h4 style="margin:0 0 6px;color:#555">Preparazione</h4>
          <ol style="margin:0;padding-left:20px">{steps_html}</ol>
        </div>"""

    shopping_html = ""
    for cat_key, items in shopping.items():
        cat_name = CATEGORIES.get(cat_key, cat_key)
        items_html = "".join(f"<li><strong>{name}</strong>: {qty}</li>" for name, qty in items)
        shopping_html += f"""
        <div style="margin-bottom:16px">
          <h4 style="margin:0 0 6px;color:#2c5f2e;border-bottom:1px solid #c8e6c9;padding-bottom:4px">{cat_name}</h4>
          <ul style="margin:0;padding-left:20px">{items_html}</ul>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;padding:20px;color:#333">

  <div style="background:linear-gradient(135deg,#2c5f2e,#4a8f4c);padding:24px 28px;border-radius:12px;margin-bottom:28px">
    <h1 style="margin:0;color:white;font-size:22px">🌿 Piano Cene Settimanale</h1>
    <p style="margin:6px 0 0;color:#c8e6c9;font-size:15px">{week_label} &nbsp;·&nbsp; 2 persone</p>
  </div>

  <p style="color:#555;font-size:13px">📅 = giorno con appuntamento → ricetta rapida (≤ 15 min) &nbsp;|&nbsp; 🐟 = piatto non vegetariano</p>

  <h2 style="color:#2c5f2e">Piano della settimana</h2>
  <table style="width:100%;border-collapse:collapse;margin-bottom:32px">
    <thead>
      <tr style="background:#2c5f2e;color:white">
        <th style="padding:10px 16px;text-align:left">Giorno</th>
        <th style="padding:10px 16px;text-align:left">Cena</th>
      </tr>
    </thead>
    <tbody>{rows}
    </tbody>
  </table>

  <h2 style="color:#2c5f2e">Lista della spesa</h2>
  {shopping_html}

  <h2 style="color:#2c5f2e">Ricette complete</h2>
  {recipe_cards}

  <hr style="border:none;border-top:1px solid #e0e0e0;margin:32px 0">
  <p style="color:#aaa;font-size:12px;text-align:center">
    Piano generato automaticamente ogni sabato pomeriggio 🤖
  </p>
</body></html>"""


def _build_plain(
    plan: dict[date, Recipe],
    shopping: dict[str, list[tuple[str, str]]],
    schedule: dict[date, bool],
    week_label: str,
) -> str:
    lines = [f"PIANO CENE SETTIMANALE — {week_label}", "=" * 50, ""]

    lines.append("PIANO DELLA SETTIMANA")
    lines.append("-" * 30)
    for d in sorted(plan.keys()):
        recipe = plan[d]
        tag = " [appuntamento - ricetta rapida]" if schedule.get(d) else ""
        veg = "" if recipe.is_vegetarian else " [non vegetariano]"
        lines.append(f"{_day_label(d, False)}{tag}: {recipe.name}{veg} ({recipe.prep_time_min} min)")

    lines += ["", "LISTA DELLA SPESA", "-" * 30]
    for cat_key, items in shopping.items():
        cat_name = CATEGORIES.get(cat_key, cat_key)
        lines.append(f"\n{cat_name.upper()}")
        for name, qty in items:
            lines.append(f"  - {name}: {qty}")

    lines += ["", "RICETTE COMPLETE", "-" * 30]
    for d in sorted(plan.keys()):
        recipe = plan[d]
        lines += [f"\n{recipe.name.upper()}", f"Tempo: {recipe.prep_time_min} min | 2 persone"]
        lines.append("Ingredienti:")
        for ing in recipe.ingredients:
            lines.append(f"  - {ing.name}: {ing.quantity}")
        lines.append("Preparazione:")
        for i, step in enumerate(recipe.instructions, 1):
            lines.append(f"  {i}. {step}")

    return "\n".join(lines)
