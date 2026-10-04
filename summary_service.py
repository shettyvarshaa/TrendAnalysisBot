from datetime import datetime


def _parse_date(value):
    return datetime.strptime(value, "%d/%m/%y")


def _format_amount(value):
    return f"{value:,.2f}"


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
    return (
        f"Across {len(records)} days, total sales were {_format_amount(total_sales)} litres, "
        f"averaging {_format_amount(average_sales)} litres per day. "
        f"Total sales {trend} from {_format_amount(first_total)} litres on "
        f"{records[0]['date']} to {_format_amount(latest_total)} litres on "
        f"{records[-1]['date']}. The best day was {best_day['date']} with "
        f"{_format_amount(float(best_day['total']))} litres."
    )
