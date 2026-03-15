const ctx = document.getElementById('documentStatusChart');
const chartData = JSON.parse(
  document.getElementById("status-data").textContent
);
const labels = Object.keys(chartData);
const values = Object.values(chartData);

const colorMap = {
  [labels[0]]: "#4A90E2",
  [labels[1]]: "#7ED321",
  [labels[2]]: "#F8E71C"
};

const backgroundColors = labels.map(label => colorMap[label] || "gray");

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Nombre de documents',
            data: values,
            backgroundColor: backgroundColors,
            borderWidth: 1
        }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });