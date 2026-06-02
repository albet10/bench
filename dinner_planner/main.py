"""Entry point: orchestrates calendar reading, meal planning, and email sending."""

import argparse
import os
import sys
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "a.tummillo@gmail.com")


def _next_monday(today: date = None) -> date:
    today = today or date.today()
    days_ahead = (7 - today.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return today + timedelta(days=days_ahead)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Piano cene vegetariano settimanale")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Usa calendario simulato, stampa il piano senza inviare email.",
    )
    parser.add_argument(
        "--start-date",
        type=date.fromisoformat,
        default=None,
        help="Data inizio settimana (YYYY-MM-DD). Default: prossimo lunedì.",
    )
    parser.add_argument(
        "--recipient",
        default=RECIPIENT_EMAIL,
        help=f"Email destinatario. Default: {RECIPIENT_EMAIL}",
    )
    args = parser.parse_args(argv)

    start_date = args.start_date or _next_monday()
    dry_run: bool = args.dry_run

    print(f"Settimana: {start_date} → {start_date + timedelta(days=6)}")
    if dry_run:
        print("Modalità dry-run: calendario simulato, email NON inviata.\n")

    # 1. Calendario
    print("1/4 Lettura calendario...")
    from .calendar_client import get_week_schedule
    schedule = get_week_schedule(start_date, dry_run=dry_run)

    appointment_days = [d for d, busy in schedule.items() if busy]
    if appointment_days:
        print(f"   Appuntamenti trovati: {', '.join(str(d) for d in sorted(appointment_days))}")
    else:
        print("   Nessun appuntamento trovato.")

    # 2. Piano cene
    print("2/4 Generazione piano cene...")
    from .meal_planner import plan_week
    plan = plan_week(schedule)

    # 3. Lista della spesa
    print("3/4 Generazione lista della spesa...")
    from .shopping_list import build_shopping_list
    shopping = build_shopping_list(plan)

    # 4. Email / output
    if dry_run:
        print("4/4 Output dry-run:\n")
        _print_plan(plan, schedule)
        _print_shopping(shopping)
        return 0

    print(f"4/4 Invio email a {args.recipient}...")
    from .email_sender import send_weekly_email
    send_weekly_email(plan, shopping, schedule, args.recipient)
    print("   Email inviata con successo!")
    return 0


def _print_plan(plan, schedule):
    from .email_sender import DAYS_IT, MONTHS_IT

    print("═" * 60)
    print("PIANO CENE DELLA SETTIMANA")
    print("═" * 60)
    for d in sorted(plan.keys()):
        recipe = plan[d]
        appt = " [📅 appuntamento]" if schedule.get(d) else ""
        veg = "🌿" if recipe.is_vegetarian else "🐟"
        quick = " ⚡" if recipe.is_quick else ""
        day_str = f"{DAYS_IT[d.weekday()]} {d.day}/{d.month}"
        print(f"  {day_str:<22}{appt:<22} {veg} {recipe.name}{quick} ({recipe.prep_time_min} min)")
    print()


def _print_shopping(shopping):
    from .recipes import CATEGORIES

    print("═" * 60)
    print("LISTA DELLA SPESA")
    print("═" * 60)
    for cat_key, items in shopping.items():
        cat_name = CATEGORIES.get(cat_key, cat_key)
        print(f"\n  {cat_name.upper()}")
        for name, qty in items:
            print(f"    • {name}: {qty}")
    print()


if __name__ == "__main__":
    sys.exit(main())
