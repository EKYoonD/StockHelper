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
        kw.push(element[1])
        num.push(element[2])
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
            labels: [items['kw']],
            datasets: [{
                label: '빈도수',
                // backgroundColor: ['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)', 'rgba(75, 192, 192, 0.5)', 'rgba(153, 102, 255, 0.5)', 'rgba(255, 159, 64, 0.5)'],
                // borderColor: ['rgb(255, 99, 132,1.5)', 'rgba(54, 162, 235, 1.5)', 'rgba(255, 206, 86, 1.5)', 'rgba(75, 192, 192, 1.5)', 'rgba(153, 102, 255, 1.5)', 'rgba(255, 159, 64, 1.5)'],
                data: [items['num']]
            }]
        },
        // Configuration options go here 
        options: {
            title: {
                display: true,
                text: 'Top10 기술별 언급 빈도수',
                fontSize: 18,
                fontColor: 'rgba(46, 49, 49, 1)'
            },
            legend: {
                labels: {
                    fontColor: 'rgba(83, 51, 237, 1)',
                    fontSize: 15
                }
            },
            scales: {
                xAxes: [{
                    ticks: {
                        fontColor: 'rgba(27, 163, 156, 1)',
                        fontSize: '15'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        fontColor: 'rgba(246, 36, 89, 1)',
                        fontSize: '15'
                    }
                }]
            }
        }
    });
}