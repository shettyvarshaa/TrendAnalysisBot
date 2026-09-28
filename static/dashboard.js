let chart;

const money = (value) => Number(value).toFixed(2);
const rows = document.getElementById("rows");
const message = document.getElementById("msg");
const theme = getComputedStyle(document.documentElement);
const cssValue = (name) => theme.getPropertyValue(name).trim();
const cssNumber = (name) => Number(cssValue(name));

const chartTheme = {
    axis: cssValue("--color-axis"),
    grid: cssValue("--color-grid"),
    muted: cssValue("--color-muted"),
    point: cssValue("--color-point"),
    ms: cssValue("--color-ms"),
    hsd: cssValue("--color-hsd"),
    total: cssValue("--color-total"),
    lineWidth: cssNumber("--chart-line-width"),
    totalLineWidth: cssNumber("--chart-total-line-width"),
    pointRadius: cssNumber("--chart-point-radius"),
    pointHoverRadius: cssNumber("--chart-point-hover-radius"),
    tension: cssNumber("--chart-line-tension"),
};

async function getData() {
    return (await fetch("/api")).json();
}

async function addReport() {
    const input = document.getElementById("input");
    const text = input.value;

    if (!text.trim()) {
        message.textContent = "Please enter a report.";
        return;
    }

    const response = await fetch("/api", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });
    const data = await response.json();

    if (response.ok) {
        message.textContent = "Saved!";
        input.value = "";
        draw(data);
    } else {
        message.textContent = data.error;
    }
}

async function clearData() {
    await fetch("/api", { method: "DELETE" });
    draw([]);
    message.textContent = "Data cleared.";
}
async function generateSummary() {
    const summaryCard = document.getElementById("summary-card");
    const summaryText = document.getElementById("summary-text");

    summaryText.textContent = "Generating summary...";
    summaryCard.hidden = false;

    const response = await fetch("/api/summary");
    const data = await response.json();

    if (!response.ok) {
        summaryText.textContent = data.error;
        return;
    }

    summaryText.textContent = data.summary;
}

document
    .getElementById("performance-summary")
    .addEventListener("click", generateSummary);

function sortByDate(data) {
    return data.sort((first, second) => {
        const [day1, month1, year1] = first.date.split("/").map(Number);
        const [day2, month2, year2] = second.date.split("/").map(Number);
        return new Date(2000 + year1, month1 - 1, day1) - new Date(2000 + year2, month2 - 1, day2);
    });
}

function formatDate(date) {
    const [day, month, year] = date.split("/").map(Number);
    return new Intl.DateTimeFormat("en-GB", {
        day: "numeric",
        month: "short",
    }).format(new Date(2000 + year, month - 1, day));
}

function salesDataset(label, key, color, width) {
    return {
        label,
        data: currentData.map((item) => item[key]),
        borderColor: color,
        backgroundColor: color,
        borderWidth: width,
        pointRadius: chartTheme.pointRadius,
        pointHoverRadius: chartTheme.pointHoverRadius,
        pointBorderWidth: 2,
        pointBackgroundColor: chartTheme.point,
        pointHoverBackgroundColor: color,
        pointHoverBorderColor: chartTheme.point,
        tension: chartTheme.tension,
        fill: false,
    };
}

let currentData = [];

function draw(data) {
    data = sortByDate(data);
    currentData = data;
    rows.innerHTML = data.map((item) => `
        <tr><td>${item.date}</td><td>${money(item.ms)}</td><td>${money(item.hsd)}</td><td>${money(item.total)}</td></tr>
    `).join("");

    if (chart) chart.destroy();
    chart = new Chart(document.getElementById("chart"), {
        type: "line",
        data: {
            labels: data.map((item) => formatDate(item.date)),
            datasets: [
                salesDataset("MS Sales", "ms", chartTheme.ms, chartTheme.lineWidth),
                salesDataset("HSD Sales", "hsd", chartTheme.hsd, chartTheme.lineWidth),
                salesDataset("Total Sales", "total", chartTheme.total, chartTheme.totalLineWidth),
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: {
                    position: "top",
                    align: "start",
                    labels: {
                        usePointStyle: true,
                        pointStyle: "circle",
                        boxWidth: 8,
                        padding: 20,
                        color: chartTheme.axis,
                        font: { size: 13 },
                    },
                },
                tooltip: {
                    mode: "index",
                    intersect: false,
                    displayColors: true,
                    callbacks: {
                        title: (items) => items[0]?.label || "",
                        label: (context) => `${context.dataset.label}: ${Number(context.raw).toLocaleString("en-US")} L`,
                    },
                },
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: chartTheme.muted, maxRotation: 0, autoSkip: true },
                    border: { display: false },
                },
                y: {
                    beginAtZero: true,
                    grace: "5%",
                    title: {
                        display: true,
                        text: "Sales (Litres)",
                        color: chartTheme.axis,
                        font: { size: 12, weight: "600" },
                    },
                    grid: { color: chartTheme.grid, drawTicks: false },
                    ticks: {
                        color: chartTheme.muted,
                        padding: 10,
                        callback: (value) => Number(value).toLocaleString("en-US"),
                    },
                    border: { display: false },
                },
            },
        },
    });
}

document.getElementById("add-report").addEventListener("click", addReport);
document.getElementById("clear-data").addEventListener("click", clearData);
getData().then(draw);
