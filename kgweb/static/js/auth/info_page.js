"use strict"

$(function () {
    $.ajax({
        type: "post",
        url: "info",
        data: "",
        dataType: "json",
        success: function (response) {
            for(let i in response.data){
                $(`#${i}`).val(response.data[i])
            }
        },
        error: function (xhr) {
            $("#content").text(`错误：${xhr.status} ${xhr.statusText}`, "danger")
        }
    })
})