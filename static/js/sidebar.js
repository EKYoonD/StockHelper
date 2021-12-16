$(document).ready(function() {
    // 파라미터 가져오기
    var rank = $('#param_rank').val();

    // aside 태그에 특허 키워드 보여줄 순위 산출
    var start = 1
    var end = 10

    if (rank) {  // 파라미터에 값이 있으면 실행
        var tmp = Math.floor(rank / 10);  // 순위의 일의 자리가 1 ~ 9인 키워드를 눌렀을 때
        start = 10 * tmp + 1;
        end = 10 * (tmp + 1);
        if (rank / 10 == tmp) {  // 순위의 일의 자리가 0인 키워드를 눌렀을 때
            start = rank - 9;
            end = rank;
        }
    }
    
    // aside 태그에 특허 키워드 순위 보여줌
    var res = $('#patent_kw');   // res 결과가 들어갈 자리
    res.load('../static/data/count_patent_desc.csv', function (data) {
        var lines = data.split('\n');
        var list = '';
        
        for (i = start; i <= end; i++) {
            var element = lines[i].split(',');
            list += '<li><a href="/StockWeb/patent?rank=' + element[0] + '&kw=' + element[1] + '">'
                        + '<span class="rank text-warning mr-1">' + element[0] + '</span>'
                        + '<span class="kw mr-1">' + String(element[1]) + '</span>'
                        + '<span class="cnt text-warning">' + element[2] + '</span>'
                        + '</a></li>'
        }
        res.html(list);   // res 결과를 html에 보여줌
    });
});