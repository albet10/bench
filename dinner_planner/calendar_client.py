"""Google Calendar API wrapper — reads all calendars for appointment detection."""

from datetime import date, datetime, timedelta, timezone

from googleapiclient.discovery import build

from .auth import get_credentials


def get_week_schedule(
    start_date: date,
    dry_run: bool = False,
) -> dict[date, bool]:
    """Return {date: has_appointment} for 7 days starting from start_date.

    In dry_run mode, returns simulated data (Mon, Wed, Fri have appointments).
    """
    if dry_run:
        return _simulated_schedule(start_date)

    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    time_min = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc).isoformat()
    time_max = datetime.combine(
        start_date + timedelta(days=7), datetime.min.time(), tzinfo=timezone.utc
    ).isoformat()

    calendar_ids = _get_all_calendar_ids(service)
    events_by_date: dict[date, bool] = {start_date + timedelta(days=i): False for i in range(7)}

    for cal_id in calendar_ids:
        try:
            result = (
                service.events()
                .list(
                    calendarId=cal_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
        except Exception:
            continue

        for event in result.get("items", []):
            event_start = event["start"].get("dateTime") or event["start"].get("date")
            try:
                if "T" in event_start:
                    event_date = datetime.fromisoformat(event_start.replace("Z", "+00:00")).date()
                else:
                    event_date = date.fromisoformat(event_start)
            except ValueError:
                continue

            if event_date in events_by_date:
                events_by_date[event_date] = True

    return events_by_date


def _get_all_calendar_ids(service) -> list[str]:
    """Return IDs of all accessible calendars."""
    result = service.calendarList().list().execute()
    return [cal["id"] for cal in result.get("items", [])]


def _simulated_schedule(start_date: date) -> dict[date, bool]:
    """Simulated week: Mon, Wed, Fri have appointments."""
    schedule = {}
    for i in range(7):
        day = start_date + timedelta(days=i)
        schedule[day] = day.weekday() in (0, 2, 4)  # Mon, Wed, Fri
    return schedule
