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
    if (buffer.length > 0) {
        data.push(buffer)
    }
 
    Highcharts.setOptions({
        time: {
            getTimezoneOffset: function (timestamp) {
                var zone = 'Asia/Seoul',
                    timezoneOffset = -moment.tz(timestamp, zone).utcOffset();
    
                return timezoneOffset;
            }
        }
    });
 
    // create the chart
    Highcharts.stockChart('companyChart', {

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

        global: {
                    useUTC: false
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