"use strict"


$(function () {
    //登录
    $("#login_button").click(function (e) {
        toggle_invalid("input", false)
        var error_message = ''
        var phone = $("#phone").val()
        var password = $("#password").val()
        //正则匹配
        if (phone.trim().length == 0) {
            error_message += "电话号码不能为空 "
            toggle_invalid("#phone", true)
        } else if (/^\d+$/.test(phone) == false) {
            error_message += "电话号码格式错误 "
            toggle_invalid("#phone", true)
        }
        if (password.trim().length == 0) {
            error_message += "密码不能为空 "
            toggle_invalid("#password", true)
        }
        if (error_message.length != 0) {
            alert(error_message, "danger")
        } else {
            $.ajax({
                type: "post",
                url: "login",
                data: JSON.stringify({
                    phone: phone,
                    password: password
                }),
                contentType: "application/json",
                dataType: "json",
                success: function (response) {
                    if (response.msg == 'success') {
                        alert(`登录成功，欢迎您${response.data.name}`, "success")
                        window.location.replace("/")
                    } else {
                        alert(`登陆失败:${response.data.error}`, 'danger')
                    }
                },
                error: function (xhr) {
                    alert(`错误：${xhr.status} ${xhr.statusText}`, "danger");
                }
            })
        }
    })
})