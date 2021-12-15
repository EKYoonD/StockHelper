// // $(document).ready(function() {
// //     chart(data)
// // })

function chart(data_set, stock_name) {
    data_set = data_set.split(',')
    var data = []
    var buffer = []
    for(i = 0; i < data_set.length; i++) {
        if(buffer.length == 5) {
            data.push(buffer)
            buffer = []
        }

        buffer.push(Number(data_set[i]))
    }
    // alert(data)

    // create the chart
    chart = new Highcharts.stockChart('container', {

        rangeSelector: {
            selected: 1
        },

        title: {
            text: '2020-01-01 이후 ' + stock_name + ' 주식 그래프'
        },

        rangeSelector: {
            selected: 1
        },

        plotOptions: {
            candlestick: {
                downColor: 'blue',
                upColor: 'red'
            }
        },

        series: [{
            type: 'candlestick',
            name: stock_name,
            data: data,
            tooltip: {
            valueDecimals: 8
            }
        }]
    });
}

// Highcharts.getJSON('https://demo-live-data.highcharts.com/aapl-ohlc.json', function (data) {
//     alert(data)
//     // create the chart
//     Highcharts.stockChart('container', {


//         rangeSelector: {
//             selected: 1
//         },

//         title: {
//             text: 'AAPL Stock Price'
//         },

//         series: [{
//             type: 'candlestick',
//             name: 'AAPL Stock Price',
//             data: data,
//             dataGrouping: {
//                 units: [
//                     [
//                         'week', // unit name
//                         [1] // allowed multiples
//                     ], [
//                         'month',
//                         [1, 2, 3, 4, 6]
//                     ]
//                 ]
//             }
//         }]
//     });
// });
