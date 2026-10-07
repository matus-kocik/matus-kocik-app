document.addEventListener("DOMContentLoaded", () => {
    // =====================================================
    // ELEMENTS
    // =====================================================

    const growthCanvas = document.getElementById(
        "investment-growth-chart"
    );

    const riskReturnCanvas = document.getElementById(
        "risk-return-chart"
    );

    const finalInvestmentCanvas = document.getElementById(
        "final-investment-chart"
    );

    const drawdownCanvas = document.getElementById(
        "drawdown-chart"
    );

    const returnVolatilityCanvas = document.getElementById(
        "return-volatility-chart"
    );

    const annualReturnsCanvas = document.getElementById(
        "annual-returns-chart"
    );

    const drawdownTimeCanvas = document.getElementById(
        "drawdown-time-chart"
    );

    const datesElement = document.getElementById(
        "investment-growth-dates"
    );

    const seriesElement = document.getElementById(
        "investment-growth-series"
    );

    const summaryElement = document.getElementById(
        "investment-summary-data"
    );

    const annualReturnYearsElement = document.getElementById(
        "annual-return-years"
    );

    const annualReturnSeriesElement = document.getElementById(
        "annual-return-series"
    );

    const drawdownDatesElement = document.getElementById(
        "drawdown-dates"
    );

    const drawdownSeriesElement = document.getElementById(
        "drawdown-series"
    );


    // =====================================================
    // FORMATTERS
    // =====================================================

    const currencyFormatter = new Intl.NumberFormat("sk-SK", {
        style: "currency",
        currency: "EUR",
        maximumFractionDigits: 0,
    });

    const percentFormatter = new Intl.NumberFormat("sk-SK", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });


    // =====================================================
    // COMMON DATA
    // =====================================================

    const assetNames = {
        usa_stocks: "USA – akcie",
        usa_bonds: "USA – dlhopisy",
        europe_stocks: "Európa – akcie",
        europe_bonds: "Európa – dlhopisy",
        germany_stocks: "Nemecko – akcie",
        germany_bonds: "Nemecko – dlhopisy",
    };

    const assetColors = {
        usa_stocks: "#4E8BC9",
        usa_bonds: "#66B7C2",
        europe_stocks: "#F2A15F",
        europe_bonds: "#D88CB5",
        germany_stocks: "#F27C73",
        germany_bonds: "#776B60",
    };


    // =====================================================
    // INVESTMENT GROWTH
    // =====================================================

    if (
        growthCanvas &&
        datesElement &&
        seriesElement
    ) {
        const dates = JSON.parse(
            datesElement.textContent
        );

        const series = JSON.parse(
            seriesElement.textContent
        );

        new Chart(growthCanvas, {
            type: "line",

            data: {
                labels: dates,

                datasets: [
                    {
                        label: assetNames.usa_stocks,
                        data: series.usa_stocks,
                        borderColor: assetColors.usa_stocks,
                        backgroundColor: assetColors.usa_stocks,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                    {
                        label: assetNames.usa_bonds,
                        data: series.usa_bonds,
                        borderColor: assetColors.usa_bonds,
                        backgroundColor: assetColors.usa_bonds,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                    {
                        label: assetNames.europe_stocks,
                        data: series.europe_stocks,
                        borderColor: assetColors.europe_stocks,
                        backgroundColor: assetColors.europe_stocks,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                    {
                        label: assetNames.europe_bonds,
                        data: series.europe_bonds,
                        borderColor: assetColors.europe_bonds,
                        backgroundColor: assetColors.europe_bonds,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                    {
                        label: assetNames.germany_stocks,
                        data: series.germany_stocks,
                        borderColor: assetColors.germany_stocks,
                        backgroundColor: assetColors.germany_stocks,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                    {
                        label: assetNames.germany_bonds,
                        data: series.germany_bonds,
                        borderColor: assetColors.germany_bonds,
                        backgroundColor: assetColors.germany_bonds,
                        borderWidth: 2.5,
                        pointRadius: 0,
                        pointHoverRadius: 5,
                        tension: 0.1,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false,
                },

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            boxWidth: 10,
                            boxHeight: 10,
                            padding: 24,
                            color: "#252525",
                        },
                    },

                    tooltip: {
                        callbacks: {
                            title(items) {
                                if (!items.length) {
                                    return "";
                                }

                                return new Date(
                                    items[0].label
                                ).toLocaleDateString("sk-SK");
                            },

                            label(context) {
                                if (context.parsed.y === null) {
                                    return "";
                                }

                                return (
                                    `${context.dataset.label}: ` +
                                    `${currencyFormatter.format(
                                        context.parsed.y
                                    )}`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                            maxTicksLimit: 10,

                            callback(value) {
                                const label =
                                    this.getLabelForValue(value);

                                return new Date(
                                    label
                                ).getFullYear();
                            },
                        },
                    },

                    y: {
                        beginAtZero: true,
                        min: 0,

                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",
                            stepSize: 10000,

                            callback(value) {
                                return currencyFormatter.format(
                                    value
                                );
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // SUMMARY DATA
    // =====================================================

    let summary = [];

    if (summaryElement) {
        summary = JSON.parse(
            summaryElement.textContent
        );
    }

    const labels = summary.map(
        (row) => assetNames[row.series] ?? row.series
    );

    const colors = summary.map(
        (row) => assetColors[row.series] ?? "#4E8BC9"
    );


    // =====================================================
    // RISK VS RETURN
    // =====================================================

    if (riskReturnCanvas && summary.length) {
        const datasets = summary.map((row) => ({
            label: assetNames[row.series] ?? row.series,

            data: [
                {
                    x: row.volatility_pct,
                    y: row.cagr_pct,
                },
            ],

            backgroundColor:
                assetColors[row.series] ?? "#4E8BC9",

            borderColor:
                assetColors[row.series] ?? "#4E8BC9",

            pointRadius: 8,
            pointHoverRadius: 11,
        }));

        new Chart(riskReturnCanvas, {
            type: "scatter",

            data: {
                datasets,
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 20,
                            color: "#252525",
                        },
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                const volatility =
                                    percentFormatter.format(
                                        context.parsed.x
                                    );

                                const returnValue =
                                    percentFormatter.format(
                                        context.parsed.y
                                    );

                                return (
                                    `${context.dataset.label}: ` +
                                    `výnos ${returnValue} %, ` +
                                    `volatilita ${volatility} %`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "Volatilita (%)",
                            color: "#776B60",
                        },

                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },

                    y: {
                        beginAtZero: true,

                        title: {
                            display: true,
                            text: "CAGR (%)",
                            color: "#776B60",
                        },

                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // FINAL INVESTMENT
    // =====================================================

    if (finalInvestmentCanvas && summary.length) {
        new Chart(finalInvestmentCanvas, {
            type: "bar",

            data: {
                labels,

                datasets: [
                    {
                        label: "Hodnota investície",
                        data: summary.map(
                            (row) => row.final_investment
                        ),
                        backgroundColor: colors,
                        borderColor: colors,
                        borderWidth: 1,
                        borderRadius: 8,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false,
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                return currencyFormatter.format(
                                    context.parsed.y
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                        },
                    },

                    y: {
                        beginAtZero: true,

                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return currencyFormatter.format(
                                    value
                                );
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // MAX DRAWDOWN
    // =====================================================

    if (drawdownCanvas && summary.length) {
        new Chart(drawdownCanvas, {
            type: "bar",

            data: {
                labels,

                datasets: [
                    {
                        label: "Maximálny pokles",
                        data: summary.map(
                            (row) => row.max_drawdown_pct
                        ),
                        backgroundColor: colors,
                        borderColor: colors,
                        borderWidth: 1,
                        borderRadius: 8,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: false,
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                return (
                                    `${percentFormatter.format(
                                        context.parsed.y
                                    )} %`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                        },
                    },

                    y: {
                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // RETURN VS VOLATILITY
    // =====================================================

    if (returnVolatilityCanvas && summary.length) {
        new Chart(returnVolatilityCanvas, {
            type: "bar",

            data: {
                labels,

                datasets: [
                    {
                        label: "CAGR",
                        data: summary.map(
                            (row) => row.cagr_pct
                        ),
                        backgroundColor: "#4E8BC9",
                        borderColor: "#4E8BC9",
                        borderWidth: 1,
                        borderRadius: 6,
                    },
                    {
                        label: "Volatilita",
                        data: summary.map(
                            (row) => row.volatility_pct
                        ),
                        backgroundColor: "#F2A15F",
                        borderColor: "#F2A15F",
                        borderWidth: 1,
                        borderRadius: 6,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 24,
                            color: "#252525",
                        },
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                return (
                                    `${context.dataset.label}: ` +
                                    `${percentFormatter.format(
                                        context.parsed.y
                                    )} %`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                        },
                    },

                    y: {
                        beginAtZero: true,

                        grid: {
                            color: "#E7F0F8",
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // ANNUAL RETURNS
    // =====================================================

    if (
        annualReturnsCanvas &&
        annualReturnYearsElement &&
        annualReturnSeriesElement
    ) {
        const years = JSON.parse(
            annualReturnYearsElement.textContent
        );

        const annualSeries = JSON.parse(
            annualReturnSeriesElement.textContent
        );

        new Chart(annualReturnsCanvas, {
            type: "bar",

            data: {
                labels: years,

                datasets: [
                    {
                        label: assetNames.usa_stocks,
                        data: annualSeries.usa_stocks,
                        backgroundColor: assetColors.usa_stocks,
                    },
                    {
                        label: assetNames.usa_bonds,
                        data: annualSeries.usa_bonds,
                        backgroundColor: assetColors.usa_bonds,
                    },
                    {
                        label: assetNames.europe_stocks,
                        data: annualSeries.europe_stocks,
                        backgroundColor: assetColors.europe_stocks,
                    },
                    {
                        label: assetNames.europe_bonds,
                        data: annualSeries.europe_bonds,
                        backgroundColor: assetColors.europe_bonds,
                    },
                    {
                        label: assetNames.germany_stocks,
                        data: annualSeries.germany_stocks,
                        backgroundColor: assetColors.germany_stocks,
                    },
                    {
                        label: assetNames.germany_bonds,
                        data: annualSeries.germany_bonds,
                        backgroundColor: assetColors.germany_bonds,
                    },
                ],
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false,
                },

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            padding: 24,
                            color: "#252525",
                        },
                    },

                    tooltip: {
                        callbacks: {
                            title(items) {
                                if (!items.length) {
                                    return "";
                                }

                                return `Rok ${items[0].label}`;
                            },

                            label(context) {
                                if (context.parsed.y === null) {
                                    return "";
                                }

                                return (
                                    `${context.dataset.label}: ` +
                                    `${percentFormatter.format(
                                        context.parsed.y
                                    )} %`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                        },
                    },

                    y: {
                        grid: {
                            color(context) {
                                if (context.tick.value === 0) {
                                    return "#776B60";
                                }

                                return "#E7F0F8";
                            },

                            lineWidth(context) {
                                if (context.tick.value === 0) {
                                    return 1.5;
                                }

                                return 1;
                            },
                        },

                        ticks: {
                            color: "#776B60",

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },
                },
            },
        });
    }


    // =====================================================
    // DRAWDOWN OVER TIME
    // =====================================================

    if (
        drawdownTimeCanvas &&
        drawdownDatesElement &&
        drawdownSeriesElement
    ) {
        const drawdownDates = JSON.parse(
            drawdownDatesElement.textContent
        );

        const drawdownSeries = JSON.parse(
            drawdownSeriesElement.textContent
        );

        new Chart(drawdownTimeCanvas, {
            type: "line",

            data: {
                labels: drawdownDates,

                datasets: [
                    {
                        label: assetNames.usa_stocks,
                        data: drawdownSeries.usa_stocks,
                        borderColor: assetColors.usa_stocks,
                        backgroundColor: assetColors.usa_stocks,
                    },
                    {
                        label: assetNames.usa_bonds,
                        data: drawdownSeries.usa_bonds,
                        borderColor: assetColors.usa_bonds,
                        backgroundColor: assetColors.usa_bonds,
                    },
                    {
                        label: assetNames.europe_stocks,
                        data: drawdownSeries.europe_stocks,
                        borderColor: assetColors.europe_stocks,
                        backgroundColor: assetColors.europe_stocks,
                    },
                    {
                        label: assetNames.europe_bonds,
                        data: drawdownSeries.europe_bonds,
                        borderColor: assetColors.europe_bonds,
                        backgroundColor: assetColors.europe_bonds,
                    },
                    {
                        label: assetNames.germany_stocks,
                        data: drawdownSeries.germany_stocks,
                        borderColor: assetColors.germany_stocks,
                        backgroundColor: assetColors.germany_stocks,
                    },
                    {
                        label: assetNames.germany_bonds,
                        data: drawdownSeries.germany_bonds,
                        borderColor: assetColors.germany_bonds,
                        backgroundColor: assetColors.germany_bonds,
                    },
                ].map((dataset) => ({
                    ...dataset,
                    borderWidth: 2.5,
                    pointRadius: 0,
                    pointHoverRadius: 5,
                    tension: 0.1,
                    spanGaps: true,
                })),
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    mode: "index",
                    intersect: false,
                },

                plugins: {
                    legend: {
                        position: "bottom",

                        labels: {
                            usePointStyle: true,
                            pointStyle: "circle",
                            boxWidth: 10,
                            boxHeight: 10,
                            padding: 24,
                            color: "#252525",

                            font: {
                                size: 13,
                            },
                        },
                    },

                    tooltip: {
                        callbacks: {
                            title(items) {
                                if (!items.length) {
                                    return "";
                                }

                                const date = new Date(
                                    items[0].label
                                );

                                return date.toLocaleDateString(
                                    "sk-SK"
                                );
                            },

                            label(context) {
                                if (context.parsed.y === null) {
                                    return "";
                                }

                                return (
                                    `${context.dataset.label}: ` +
                                    `${percentFormatter.format(
                                        context.parsed.y
                                    )} %`
                                );
                            },
                        },
                    },
                },

                scales: {
                    x: {
                        grid: {
                            display: false,
                        },

                        border: {
                            color: "#D7E5F1",
                        },

                        ticks: {
                            color: "#776B60",
                            maxTicksLimit: 10,
                            padding: 10,

                            font: {
                                size: 12,
                            },

                            callback(value) {
                                const label =
                                    this.getLabelForValue(value);

                                const date =
                                    new Date(label);

                                return date.getFullYear();
                            },
                        },
                    },

                    y: {
                        max: 0,

                        grid: {
                            color: "#E7F0F8",
                            lineWidth: 1,
                        },

                        border: {
                            display: false,
                        },

                        ticks: {
                            color: "#776B60",
                            padding: 12,

                            font: {
                                size: 12,
                            },

                            callback(value) {
                                return `${value} %`;
                            },
                        },
                    },
                },
            },
        });
    }
});