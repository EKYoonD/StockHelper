$(document).ready(function() {

    // 종목 검색
    $('#search_btn').click(function() {
        // 종목 검색
        if ($('#search_input').val().trim() == "" || $('#search_input').val().trim().length < 2) {
            alert("검색은 2글자 이상 입력해야 합니다.");
            return;
        }
        // res 결과가 들어갈 html element
        var res = $("#res_table");
        res.load("../static/data/stockList_CSV.csv", function (data) {
            var lines = data.split("\n");
            var table = "";
            
            for (i = 0; i < lines.length; i++) {    
                var line = lines[i];
                if ( line.includes($('#search_input').val()) ) {
                    var elements = line.split(",");                    
                    table += "<tr>";
                    table += "<td>" + elements[0] + "</td>";
                    table += "<td>" + elements[1] + "</td>";
                    table += '<td><button type="button" name="add" value="' + elements[0] + '">선택</button></td>' ;
                    table += "</tr>";
                }
            }
            res.html(table);

            $("button[name='add']").on("click", function () {
                stock_name = $(this).val();
                location.href = '/StockWeb/analysis'
                alert(stock_name)
        
            });
        })

        
    

    });


    

})