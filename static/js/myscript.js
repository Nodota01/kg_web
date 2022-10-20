"use strict"
var click_count = 0

$(function () {
    console.log("jq is ready")
    // $("table tr:even").style.backgroundColor = "grey"
    $("#jq_click").click(function () {
        console.log("jq click event")
        $("#title").slideToggle();
    })
    $("#jq_animation").click(function (e) {
        $("#main_text").animate({ height: '300px', opacity: '0.4' }, "slow")
            .animate({ width: '300px', opacity: '0.8' }, "slow")
            .animate({ height: '100px', opacity: '0.4' }, "slow")
            .animate({ width: '100px', opacity: '0.8' }, "slow")
    });
    $("#jq_change_text").click(function (e) {
        $("#main_text").text("I am changed by jq");
    })
        .attr("href", "javascript:void(0)")
        .attr({
            "target": "_self",
            "type": "text/plain"
        })
    $("#main_text").append($("<p></p>").text(" to here"))
    $("#jq_class").click(function (e) {
        $(this).toggleClass("button")
    });
    $("#jq_css").click(function (e) {
        $(this).css({
            "background_color": "grey",
            "font-size": "30px"
        })
    });

    $("#jq_ajax").click(function (e) { 
        $.get("http://192.168.1.2:8888/user/1", "",
            function (data, textStatus, jqXHR) {
                alert(JSON.stringify(data))
            },
            "json"
        );
    })

    $("#login_button").click(function (e) { 
        var obj = {
            username : $("#username_text").val(),
            password : $("#password_text").val()
        }
        $.ajax({
            type: "post",
            url: "http://192.168.1.2:8888/user/verify",
            data: JSON.stringify(obj),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                console.log(response.msg)
                if(response.data == -1){
                    alert("Login Failure")
                }else{
                    alert("Login Success")
                }
            }
        })
    })
})

function create_alert() {
    var person = { name: "Tom", age: 11 }
    alert("Hello" + person.name
        + JSON.stringify(person))
    console.log(person.name + person.age)
}

function change_title() {
    var t = document.getElementById("title")
    t.style.backgroundColor = "Aqua"
    t.innerHTML = "Hello World!!!!"
    click_count += 1
    document.getElementById("main_text").innerHTML += click_count + " "
}

function check_input(obj) {
    alert(/^\d+@\w+\.\w+$/.test(obj.value))
    if (obj.checkValidity() == false) {
        alert(obj.validationMessage)
    }
}

//三秒后执行函数
setTimeout(function () {
    console.log("三秒过去了")
}, 3000)

new Promise(function (resolve, reject) {
    console.log("Run");
});
