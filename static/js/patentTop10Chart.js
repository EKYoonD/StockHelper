$(document).ready(function() {
    // 특허 키워드 순위 top50 보여줌
    $.ajax({
        url : '../static/data/count_patent_desc.csv',
        dataType : 'text',
        success: function(data) {
            items = parseData(data)
            graphTop10(items);
        }
    });
});

function parseData(data) {
    var kw = [];
    var num = [];

    var lines = data.split('\n');
    for (i = 1; i <= 10; i++) {
        var element = lines[i].split(',');
        kw.push(element[1]);
        num.push(Number(element[2]));
    }

    return {'kw': kw, 'num': num};
}

function graphTop10(items) {
    // 출처: https://carriedata.tistory.com/entry/Chartjs로-그래프-만들기 [캐리의 데이터 세상]
   
    var ctx = document.getElementById('patentTop10Chart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create 
        type: 'bar', // The data for our dataset 
        data: {
            labels: items['kw'],
            datasets: [{
                label: '빈도수',
                backgroundColor: '#33333370',
                borderColor: '#0D2C3F',
                data: items['num']
            }]
        },
        // Configuration options go here 
        options: {
            // title: {
            //     display: true,
            //     text: '- Top10 기술별 언급 빈도수 -',
            //     fontSize: 15,
            //     fontColor: 'gray'
            // },
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
                        fontSize: '15',
                        fontStyle: 'bold'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontColor: 'black',
                        fontSize: '15',
                    }
                }]
            }
        }
    });
}