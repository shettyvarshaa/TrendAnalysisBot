# Sales Report Analyzer Bot

A bot that turns simple forwarded sales reports into useful sales insights.

Instead of manually entering sales data into a spreadsheet or creating charts, simply forward the daily sales report to the bot in a predefined format.

### Example Input

```text
SalesReport;
09/09/26
MS;1879.97
HSD;3514.01
Total sales;1880+3514=5393.98
```

The bot reads the report, records the sales figures, and uses the accumulated data to generate:

* 📈 **MS, HSD, and Total sales trend visualization**
* 📊 **Sales performance summary**
* 🔎 **Key changes and fluctuations in sales**
* 📅 **Comparison of sales across different dates**

As more daily reports are forwarded, the bot can build up a sales history and provide a broader view of how sales are performing over time.

## Goal

The goal is to make sales tracking as simple as **forwarding a daily report**.

No manual data entry, spreadsheet updates, or separate analysis is required. The bot converts the reports into an easy-to-understand view of sales performance.

## Workflow

**Forward Sales Report → Bot processes the report → Sales data is recorded → Trend is updated → Performance summary is generated**

## Example

A series of daily reports can be used to generate a visualization like:

**MS ↗️ | HSD ↗️ | Total Sales ↗️**

along with a short summary explaining the overall sales trend and notable changes.

## Intended Use

Designed for businesses that receive regular sales reports and want a simple way to continuously track and understand their sales performance.

### Vercel deployment 

The dashboard saves each user's graph data in that browser's local storage, so refreshing
the page preserves the result. The Vercel filesystem is read-only except for `/tmp`, so
the server also uses `/tmp/sales_data.json` during a serverless instance's lifetime.
Browser data is private to that browser and is cleared if its site data is removed. (Still working on it, will fix this week :D)
