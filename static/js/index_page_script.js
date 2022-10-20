"use strict"

var cur_url = window.location.protocol + "//"
    + window.location.hostname + ":" + window.location.port + "/"

$(document).ready(function () {
    $("#search_button").click(function (e) {
        var obj = {
            key_word : $("#search_text").val()
        }
        $.ajax({
            type: "post",
            url: cur_url  + "q",
            data: JSON.stringify(obj),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                $("#search_result").text(JSON.stringify(response));
            }
        });
    });
});