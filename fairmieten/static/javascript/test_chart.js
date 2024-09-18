

fetch('data/vorfaelle_pro_jahr/')
.then(response => response.json())
.then(data => {
    // Get the canvas context
    const ctx = document.getElementById('testChart').getContext('2d');
    
    // Create a bar chart using Chart.js
    console.log(data);
    new Chart(ctx, {
        type: 'bar',  // Bar chart type
        data: {
            labels: data.labels,  // Years on the x-axis
            datasets: [{
                label: 'Vorfälle pro Jahr',  // Legend label
                data: data.datasets[0].data,  // Incident count on y-axis
                backgroundColor: 'rgba(255, 99, 132, 0.2)',  // Bar color
                borderColor: 'rgba(255, 99, 132, 1)',  // Border color
                borderWidth: 1  // Bar border width
            }]
        },
        options: {
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'Anzahl Vorfälle'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Jahr'
                    }
                }
            }
        }
    });
})
.catch(error => console.error('Error fetching data:', error));