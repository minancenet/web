function createChart(chartType, timeFrame, assetName) {
  var dates = []
  var o = []
  var h = []
  var l = []
  var c = []

  fetch("http://localhost:5000/api/v1/asset/" + assetName + "/ohlc/" + timeFrame + ".json")
  .then(res => res.json())
  .then((out) => {    
    for (var i = 0; i < out[chartType].length; i++) {
      dates.push(out[chartType][i][0]*1000)
      o.push(out[chartType][i][1])
      h.push(out[chartType][i][2])
      l.push(out[chartType][i][3])
      c.push(out[chartType][i][4])
    }

    var trace1 = {
  
      x: dates, 
              
      open: o,
      high: h,        
      low: l,
      close: c, 
    
      increasing: {line: {color: '#05FFA1'}}, 
      decreasing: {line: {color: '#333333'}},

      line: {color: 'rgba(31,119,180,1)'}, 
  
      type: 'candlestick', 
      xaxis: 'x', 
      yaxis: 'y'
    };
  
    var data = [trace1];
  
    var layout = {
      dragmode: 'zoom', 
      margin: {
        r: 10, 
        t: 25, 
        b: 40, 
        l: 60
      }, 
      showlegend: false, 
      xaxis: {
        autorange: true, 
        rangeslider: {}, 
        type: 'date'
      }, 
      yaxis: {
        autorange: true, 
        type: 'linear'
      },
      plot_bgcolor: "rgb(0,0,0)",
      paper_bgcolor: "rgb(0,0,0)"
    };
  
    var config = {
      responsive: true
    }
  
    Plotly.newPlot(chartType + "Chart", data, layout, config);  
  })
}

function createBuySellChart(assetName) {
  fetch("http://localhost:5000/api/v1/asset/" + assetName + "/price")
  .then(res => res.json())
  .then((out) => {
    var dates = []
    var sell = []
    var buy = []
    
    for (var i = 0; i < out["sell"].length; i++) {
      dates.push(out["sell"][i][0]*1000)
      sell.push(out["sell"][i][1])
    }

    for (var i = 0; i < out["buy"].length; i++) {
      dates.push(out["buy"][i][0]*1000)
      buy.push(out["buy"][i][1])
    }
    
    var trace1 = {
  
      x: dates, 
      y: sell,
      name: "Sell Price",
    
      line: {color: '#05DB89'}, 
      fill: 'tozeroy',

      type: 'scatter', 
      xaxis: 'x', 
      yaxis: 'y'
    };

    var trace2 = {
      x: dates,
      y: buy,
      name: "Buy Price",

      line: {color: '#7F7F7F'},
      fill: 'tonexty',
        
      type: 'scatter', 
      xaxis: 'x', 
      yaxis: 'y'
    }

    var data = [trace1, trace2];

    var layout = {
      dragmode: 'zoom', 
      margin: {
        r: 10, 
        t: 25, 
        b: 40, 
        l: 60
      }, 
      showlegend: false, 
      xaxis: {
        autorange: true, 
        rangeslider: {}, 
        type: 'date'
      }, 
      yaxis: {
        autorange: true, 
        type: 'linear'
      },
      plot_bgcolor: "rgb(0,0,0)",
      paper_bgcolor: "rgb(0,0,0)"
    };

    var config = {
      responsive: true
    }
  
    Plotly.newPlot('lineChart', data, layout, config);
  })
}