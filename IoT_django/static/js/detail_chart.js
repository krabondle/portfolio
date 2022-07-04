console.log(labels);
console.log(defaultData);
console.log(Isupdate);
var myChart;
if(defaultData==0) {
  document.getElementById("nodata").style.visibility = "visible";
}else{
  document.getElementById("nodata").style.visibility = "hidden";
  setChart();
}
function setChart() {
  var ctx2 = document.getElementById("myChart2");
  myChart = new Chart(ctx2, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: '# of Votes',
        data: defaultData,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
        ],
        borderColor: [
          'rgba(255,255,255,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 2,
        pointRadius: 0,
        fill: false
      
      }]
    },
    options: {
      responsive: true,
        title: {
          display: true,
        },
        tooltips: {
          mode: 'index',
          intersect: false,
        },
        hover: {
          mode: 'nearest',
          intersect: true
        },
      scales: {
        autoSkip:true,
        fontSize: 15,
        xAxes: [{
          gridLines: {
            display: true,
            zeroLineColor:'white'
          },
          /*scaleLabel: {
            display: true,
            labelString: "Time in Seconds",
            fontColor: "red"
          },*/
          ticks: {
            fontColor:'white',
            
          },
          
        }],
        yAxes: [{
          gridLines: {
            display: true,
            drawBorder: false,
            zeroLineColor:'white'
          },
          /*scaleLabel: {
            display: true,
            labelString: "Time in Seconds",
            fontColor: "red"
          },*/
          ticks: {
            beginAtZero: false,
            //callback: function(value, index, values){return value + "%";},
            fontColor:'white',
            fontSize: 15,
            autoSkip: false
          },
          
        }]
      }
    }
  });
}
function refresh() {
  $.get("/data_update/", { 'item': location.pathname.replace("/","").replace("/","").split("_")[1] }, function (data) {
    //console.log(data.sensor[0]);
    //console.log(data.sensor[1]);
    var Sensor_ID = location.pathname.replace("/","").replace("/","").split("_")[1];
    //Sensor_ID = Sensor_ID.replace("/","");
    
    //console.log(Sensor_ID);
    console.log(data);
    //console.log(data[Sensor_ID]);
    //console.log(data[Sensor_ID][0][1]);
    //console.log(myChart.data.labels[19]);
    if (myChart.data.labels[19] != data[Sensor_ID][1]) {
      myChart.data.datasets[0].data.shift();
      myChart.data.labels.shift();
      myChart.data.labels.push(data[Sensor_ID][1]);
      //myChart.data.defaultData.push(data.sensor[1]);
      myChart.data.datasets[0].data.push(data[Sensor_ID][0]);
      myChart.update();
    }
  })
}
console.log(Isupdate);
if(Isupdate==true)
{
  setInterval(refresh, 1000);
}
// var ctx = document.getElementById("myChart");