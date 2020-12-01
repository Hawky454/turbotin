var config = {
    type: 'line',
    data: {
        labels: {{plot_data.labels}},
        datasets: [{% for i in range(items|length) %}
            {
                label: '{{plot_data.datasets[i].store}}',
                fill: false,
                borderColor: '{{store_colors[plot_data.datasets[i].store]}}',
                data: {{plot_data.datasets[i].data}}
            }{% if i != items|length %},{% endif %}
            {% endfor %}]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Price history for: {{brand}} {{blend}}'
        },
        scales: {
            xAxes: [{
                type: 'time'
            }]
        },
        elements: {
            line: {
                tension: 0 // disables bezier curves
            }
        },
        showLines: false
    }
};

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};