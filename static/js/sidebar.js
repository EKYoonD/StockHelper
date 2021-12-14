function getToday(){
    var date = new Date();
    var year = date.getFullYear();
    var month = ("0" + (1 + date.getMonth())).slice(-2);
    var day = ("0" + date.getDate()).slice(-2);

    return year + month + day;
}

$(document).ready(function() {
    // + 아이콘 클릭시 페이지 이동 
    $('#more_btn').click(function(){
        location.href = '/StockWeb/patentKeyword';
    });

    // aside 태그에 특허 키워드 순위 보여줌
    var res = $('#patent_kw');   // res 결과가 들어갈 자리
    var today = '20211208'
    // var today = getToday()
    res.load('../static/data/count_patent_' + today + '.csv', function (data) {
        var lines = data.split('\n');
        var list = '';
        
        for (i = 1; i <= 10; i++) {
            var element = lines[i].split(',');
            list += '<li><a href="/StockWeb/patent">'
                        + '<span class="rank text-warning mr-1">' + i + '</span>'
                        + '<span class="kw mr-1">' + element[0] + '</span>'
                        + '<span class="cnt text-warning">' + element[1] + '</span>'
                        + '</a></li>'
        }
        res.html(list);   // res 결과를 html에 보여줌
    });
});