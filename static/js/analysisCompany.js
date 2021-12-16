function chart(data_set, stock_name, stock_close_date_list, stock_close_price_list) {
    all_chart(data_set, stock_name)
    close_chart(stock_close_date_list, stock_close_price_list)

}

// 기업정보에 들어가는 chart
function all_chart(data_set, stock_name) {
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

// 종가 그래프 그리기
function close_chart(stock_close_date_list, stock_close_price_list) {
    stock_close_date_list = stock_close_date_list.split(',')
    stock_close_price_list = stock_close_price_list.split(',')

    var context = document
        .getElementById('closeChart')
        .getContext('2d');
    var closeChart = new Chart(context, {
        type: 'line', // 차트의 형태
        data: { // 차트에 들어갈 데이터
            labels:
                //x 축 (리스트) 
                stock_close_date_list
                // [1,2,3,4,5,6]
                // ['1','2','3','4','5','6']

                ,
            datasets: [{ //데이터
                    label: '최근 20일간의 종가 + 예측 종가', //차트 제목
                    fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
                    data: 
                        stock_close_price_list //x축 label에 대응되는 데이터 값 (list)
                        // [5,6,7,8,9,10]
                        ,
                    backgroundColor: [
                        //색상
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        //경계선 색상
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1 //경계선 굵기
                }
            ]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}