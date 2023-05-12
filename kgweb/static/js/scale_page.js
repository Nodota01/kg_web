"use strict"

$(function () {
    $("#submit_button").click(function (e) {
        var scores = Array()
        var trs =  $("tbody").find("tr")
        for (var i = 0; i < trs.length; i++){ 
            var radio = $(trs[i]).find("input[type=radio]:checked");
            //如果存在这样的元素
            if (radio.length = 1) {
                var value = radio.val()
                scores.push(value)
            } else {
                alert("未完成量表")
                return
            }
        }
        console.log(scores)
        $.ajax({
            type: "post",
            url: "/scale",
            data: JSON.stringify({
                scale_name: scale_name,
                scores: scores,
            }),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                if (response.msg == "fail"){
                    alert("请求体错误")
                }else if(response.msg == "success"){
                    alert(`您的体质为${response.data.items}`)
                }else{
                    alert("未知错误")
                }
            },
            error: function (xhr) {
                alert(xhr)
            }
        })
    })
})