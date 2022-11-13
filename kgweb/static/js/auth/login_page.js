"use strict"

// 弹出警告框
function alert(message, type) { 
    var holder = $("#live_alert_placeholder")
    holder.children().remove()
    holder.html(`<div class="alert mt-3 alert-${type}" role="alert">${message}</div>`)
}

$(function () {
    //登录
    $("#login_button").click(function (e) { 
        var error_message = ''
        var phone = $("#phone").val()
        var password = $("#password").val()
        //正则匹配
        if(phone.trim().length == 0){
            error_message += "电话号码不能为空 "
        }else if(/^\d+$/.test(phone) == false){
            error_message += "电话号码格式错误 "
        }
        if(password.trim().length == 0){
            error_message += "密码不能为空 "
        }
        if(error_message.length != 0){
            alert(error_message, "danger")
        }else{
            $.ajax({
                type: "post",
                url: "login",
                data: JSON.stringify({
                    phone:phone,
                    password:password
                }),
                contentType: "application/json",
                dataType: "json",
                success: function (response) {
                    if(response.msg == 'success'){
                        alert("登录成功", "success")
                        window.location.replace("/")
                    }else{
                        alert(`登陆失败:${response.data}`, 'danger')
                    }
                },
                error:function(xhr){
                    alert(`错误：${xhr.status} ${xhr.statusText}`, "danger");
                }
            });
        }
    })

    //测试登录
    $("#test_login_button").click(function (e) { 
        $.ajax({
            type: "post",
                url: "isLogin",
                data: "",
                dataType: "json",
                success: function (response) {
                    if(response.msg == 'success'){
                        if(response.data.isLogin){
                            alert("已登录", 'success')
                        }else{
                            alert("未登录", 'danger')
                        }
                    }else{
                        alert(`请求失败`, 'danger')
                    }
                },
                error:function(xhr){
                    alert(`错误：${xhr.status} ${xhr.statusText}`, "danger");
                }
        });
    })
})