// 종목 검색 확인
function check_input() {
    if ($('#search_input').val().trim() == "" || $('#search_input').val().trim().length < 2) {
        $('#search_result').css('display', 'none')  // 검색 결과
        
        if ($('.chkIdErrorNum').length < 4) {  // 화면에 경고창이 4개 있으면 신규 경고 표시 중지 
            $('#chkIdError_list').prepend('<li class="alert alert-danger alert-dismissable chkIdErrorNum"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-diamond-fill mr-2" viewBox="0 0 16 16"><path d="M9.05.435c-.58-.58-1.52-.58-2.1 0L.436 6.95c-.58.58-.58 1.519 0 2.098l6.516 6.516c.58.58 1.519.58 2.098 0l6.516-6.516c.58-.58.58-1.519 0-2.098L9.05.435zM8 4c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995A.905.905 0 0 1 8 4zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>2글자 이상 입력해주세요.<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button></li>')
        }
        return false;
    }
    return true;
}

// 검색 결과 반환
function search_table() {
    $('#res_cnt').css('display', 'none')  // 검색 결과 개수
    $('#search_result').css('display', 'block')  // 결과 표시칸 생성
    $('.chkIdErrorNum').css('display', 'none')  // 모든 경고창 삭제
    
    // index 페이지에 검색 결과 보여줌
    var res = $("#res_table");   // res 결과가 들어갈 html element
    res.load("../static/data/stockList_CSV.csv", function (data) {
        var lines = data.split("\n");
        var table = "";
        var res_cnt = 0;
        
        for (i = 1; i < lines.length; i++) {
            var line = lines[i];
            var elements = line.split(",");
            if (String(elements[1]).includes($('#search_input').val())) {
                table += "<tr>";
                table += "<td class='pl-3 ellipsis'>" + elements[1] + "</td>";
                table += "<td class='text-center'>" + elements[2] + "</td>";
                table += '<td class="pr-3 text-right"><button type="button" name="analysisKeyword_btn" class="btn btn-outline-secondary btn-sm" value="' + elements  + '">선택</button></td>';
                table += "</tr>";
                res_cnt += 1;
            }
        }
        res.html(table);   // res 결과를 html에 보여줌

        // 검색 개수
        res.prepend('<tr class="border-bottom" id="res_cnt"><td class="pl-3 py-1" colspan="3">검색결과: <strong>' + res_cnt + '</strong>건</td></tr>')
        
        // table의 선택 버튼 눌러서 분석 페이지로 이동
        $("button[name='analysisKeyword_btn']").on("click", function () {
            stock = $(this).val().split(',');

            location.href = "analysis?stock=" + stock[2] + "&name=" + stock[1];
        });
    });
}

$(document).ready(function() {
    // 검색어 입력창에서 엔터
    $('#search_input').keydown(function(key) {
        if (key.keyCode == 13) {
            if (check_input() == true) search_table()
        }
    });
    // 검색버튼 클릭
    $('#search_btn').click(function() {
        if (check_input() == true) search_table()
    });
    // 첫 시작 화면에서 안 보이게 하기
    $('#search_result').css('display', 'none')  // 검색 결과
});