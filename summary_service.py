from datetime import datetime, timedelta


def _parse_date(value):
    return datetime.strptime(value, "%d/%m/%y")


def _format_amount(value):
    return f"{value:,.2f}"


def _weekly_average(records, start, end):
    weekly_totals = [
        float(record["total"])
        for record in records
        if start <= _parse_date(record["date"]) < end
    ]
    return sum(weekly_totals) / len(weekly_totals) if weekly_totals else None


def generate_summary(data):
    if not data:
        return "There is no sales data available to summarize."

    records = sorted(data, key=lambda item: _parse_date(item["date"]))
    total_sales = sum(float(item["total"]) for item in records)
    average_sales = total_sales / len(records)
    first_total = float(records[0]["total"])
    latest_total = float(records[-1]["total"])

    if first_total == 0 and latest_total == 0:
        trend = "started and ended at zero"
    elif first_total == 0:
        trend = "increased from zero"
    else:
        change = ((latest_total - first_total) / abs(first_total)) * 100
        direction = "increased" if change > 0 else "decreased" if change < 0 else "stayed flat"
        trend = f"{direction} by {abs(change):.1f}%"

    best_day = max(records, key=lambda item: float(item["total"]))
    current_week_start = _parse_date(records[-1]["date"]) - timedelta(
        days=_parse_date(records[-1]["date"]).weekday()
    )
    previous_week_start = current_week_start - timedelta(days=7)
    current_week_average = _weekly_average(
        records, current_week_start, current_week_start + timedelta(days=7)
    )
    previous_week_average = _weekly_average(
        records, previous_week_start, current_week_start
    )

    if previous_week_average is None:
        weekly_summary = (
            f"In the current week, sales averaged {_format_amount(current_week_average)} "
            "litres per day."
        )
    else:
        weekly_change = (
            (current_week_average - previous_week_average)
            / abs(previous_week_average)
            * 100
        )
        weekly_direction = "increase" if weekly_change >= 0 else "decrease"
        weekly_summary = (
            f"In the current week, sales averaged {_format_amount(current_week_average)} "
            f"litres per day, compared with {_format_amount(previous_week_average)} "
            f"litres per day in the previous week, a {abs(weekly_change):.1f}% "
            f"{weekly_direction}."
        )

    return (
        f"Across {len(records)} days, total sales were {_format_amount(total_sales)} litres, "
        f"averaging {_format_amount(average_sales)} litres per day. "
        f"Daily sales {trend} from {_format_amount(first_total)} litres on "
        f"{records[0]['date']} to {_format_amount(latest_total)} litres on "
        f"{records[-1]['date']}. The best day was {best_day['date']} with "
        f"{_format_amount(float(best_day['total']))} litres. {weekly_summary}"
    )
