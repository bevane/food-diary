document.addEventListener('DOMContentLoaded', function() {
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);
    const ctxSymptoms = document.getElementById('symptomsChart');
    const ctxFoods = document.getElementById('foodsChart')

    // instantiation and configuration of charts displayed on analyze app, using ChartJs
    new Chart(ctxSymptoms, {
      type: 'line',
      data: {
        datasets: [{
            label: 'All Symptoms',
            data: chartData[1],
        }],
        labels: chartData[0]
      },
      options: {
        plugins: {
          title: {
            display: true,
            text: 'Occurrences of Symptoms over time'
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: '# of times symptoms occurred'
            },
            suggestedMin: 0,
            ticks: {
              stepSize: 1
            }
          },
          x: {
            title: {
              display: true,
              text: 'Date'
            }
          }
        }
      }
      })
});
