// 검색 결과 반환
function search_keyword_company(kw, stock_code) {
    // patent 페이지에 키워드 보유 기업 리스트 보여줌
    var res = $("#res_table");   // res 결과가 들어갈 html element
    res.load("../static/data/Keyword_Company.csv", function (data) {
        var lines = data.split("\n");
        var table = "";
        var res_cnt = 0;
        
        for (i = 1; i < lines.length; i++) {
            var line = lines[i];
            var elements = line.split(",");
            if (String(elements[1]).includes(kw)) {
                if (elements[2] == 'N') break;  // 키워드에 해당하는 종목이 없는 데이터
                table += "<tr>";
                table += "<td class='pl-3 ellipsis'>" + elements[2] + "</td>";
                table += "<td class='text-center'>" + elements[3] + "</td>";
                table += '<td class="pr-3 text-right"><button type="button" name="analysisKeyword_btn" class="btn btn-outline-secondary btn-sm" value="' + elements  + '">선택</button></td>';
                table += "</tr>";
                res_cnt += 1;
            }
        }
        res.html(table);   // res 결과를 html에 보여줌

        // 검색 개수
        res.prepend('<tr class="border-bottom" id="res_cnt"><td class="pl-3 py-1" colspan="3">검색결과: <strong class="text-warning">' + res_cnt + '</strong>건</td></tr>')
        
        // table의 선택 버튼 눌러서 분석 페이지로 이동
        $("button[name='analysisKeyword_btn']").on("click", function () {
            stock = $(this).val().split(',');

            location.href = "analysis?stock=" + stock[3] + "&name=" + stock[2];
        });
    });
}

$(document).ready(function() {
    // 클릭한 키워드
    keyword = $('#patent > h6 > span').html()
    
    // 클릭한 키워드에 대한 주식정보
    search_keyword_company(keyword)    
});