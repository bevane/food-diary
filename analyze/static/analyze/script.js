document.addEventListener('DOMContentLoaded', function() {
    const symData = JSON.parse(document.getElementById('sym-data').textContent);
    const foodData = JSON.parse(document.getElementById('food-data').textContent);
    const ctxSymptoms = document.getElementById('symptomsChart');
    const ctxFoods = document.getElementById('foodsChart')

    // prepare dataset for the stacked bar chart for Food History
    var foodDataset = []
    for (let [key, value] of Object.entries(foodData[1])) {
      foodDataset.push(
        {
          label: key,
          data: value
        })
    }

    // instantiation and configuration of charts displayed on analyze app, using ChartJs
    new Chart(ctxSymptoms, {
      type: 'line',
      data: {
        datasets: [{
            label: 'All Symptoms',
            data: symData[1],
        }],
        labels: symData[0]
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

      new Chart(ctxFoods, {
        type: 'bar',
        data: {
          labels: foodData[0],
          datasets: foodDataset,
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: 'Food history over time'
            }
          },
          scales: {
            y: {
              stacked: true,
              title: {
                display: true,
                text: '# of Food'
              },
              suggestedMin: 0,
              ticks: {
                stepSize: 1
              }
            },
            x: {
              stacked: true,
              title: {
                display: true,
                text: 'Date'
              }
            }
          }
        }
        })
});
