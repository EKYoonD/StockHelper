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
                stock_close_date_list,

            datasets: [{ //데이터
                    label: '종가', //차트 제목
                    fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
                    data: 
                        stock_close_price_list //x축 label에 대응되는 데이터 값
                        ,
                    backgroundColor: 
                        //색상

                        '#f0ad4e'
                    ,
                    borderWidth: 1 //경계선 굵기
                }
            ]
        },
        options: {
            title:{
                display:true,
                text:'최근 20일간의 종가 + 예측 종가'
            },
            legend: {
                labels: {
                    fontColor: 'black',
                    fontSize: 16,
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontColor: 'black',
                        fontSize: '10',
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontColor: 'black',
                        fontSize: '10',
                    }
                }]
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
    
                            if (label) {
                                label += ': ';
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}

$(document).ready(function(){
    // 종가 상하강 여부에 따른 글자색 변화
    var upDown = $('#up_down').text();
    if (upDown == '상승') {
        $('.stock_upDown').css({"color": "#d9534f", "font-weight": "bold"}) // 빨강(danger)
    } else if (upDown == '하강') {
        $('.stock_upDown').css({"color": "#0275d8", "font-weight": "bold"}) // 파랑(primary)
    } else {
        $('.stock_upDown').css({"color": "#5cb85c", "font-weight": "bold"}) // 초록(success)
    }
});