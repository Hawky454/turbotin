var config = {
    type: 'line',
    data: {
        labels: {{plot_data.labels}},
        datasets: [{% for i in range(plot_data.datasets|length) %}
            {
                label: '{{plot_data.datasets[i].store}}',
                fill: false,
                borderColor: '{{store_colors[plot_data.datasets[i].store]}}',
                pointBackgroundColor: '{{store_colors[plot_data.datasets[i].store]}}',
                data: {{plot_data.datasets[i].data}}
            }{% if i != plot_data.datasets|length %}, {% endif %}
            {% endfor %}]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Price When in Stock'
        },
        scales: {
            xAxes: [{
                type: 'time'
            }],
            yAxes: [{
                ticks: {
                    callback: function (label, index, labels) {
                        return "$" + label;
                    }
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Price'
                }
            }]
        },
        elements: {
            line: {
                tension: 0 // disables bezier curves
            }
        },
        showLines: false,
        maintainAspectRatio: false,
        tooltips: {
            callbacks: {
                label: function (tooltipItem, data) {
                    var label = data.datasets[tooltipItem.datasetIndex].label || '';

                    if (label) {
                        label += ': $';
                    }
                    label += tooltipItem.yLabel.toFixed(2);
                    return label;
                }
            }
        }
    }
};

window.onload = function () {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};