let chart;

const money = (value) => Number(value).toFixed(2);
const rows = document.getElementById("rows");
const message = document.getElementById("msg");

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

function sortByDate(data) {
    return data.sort((first, second) => {
        const [day1, month1, year1] = first.date.split("/").map(Number);
        const [day2, month2, year2] = second.date.split("/").map(Number);
        return new Date(2000 + year1, month1 - 1, day1) - new Date(2000 + year2, month2 - 1, day2);
    });
}

function draw(data) {
    data = sortByDate(data);
    rows.innerHTML = data.map((item) => `
        <tr><td>${item.date}</td><td>${money(item.ms)}</td><td>${money(item.hsd)}</td><td>${money(item.total)}</td></tr>
    `).join("");

    if (chart) chart.destroy();
    chart = new Chart(document.getElementById("chart"), {
        type: "line",
        data: {
            labels: data.map((item) => item.date),
            datasets: [
                { label: "MS Sales", data: data.map((item) => item.ms), tension: 0.3 },
                { label: "HSD Sales", data: data.map((item) => item.hsd), tension: 0.3 },
                { label: "Total Sales", data: data.map((item) => item.total), tension: 0.3 },
            ],
        },
        options: {
            responsive: true,
            interaction: { mode: "index", intersect: false },
            scales: { y: { beginAtZero: true } },
        },
    });
}

document.getElementById("add-report").addEventListener("click", addReport);
document.getElementById("clear-data").addEventListener("click", clearData);
getData().then(draw);
