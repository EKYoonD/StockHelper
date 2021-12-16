// 기업정보에 들어가는 chart
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

    // create the chart
    chart = new Highcharts.stockChart('companyChart', {

        rangeSelector: {
            selected: 1
        },

        title: {
            text: stock_name + ' 주식 그래프'
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

$(document).ready(function() {
});