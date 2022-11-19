"use strict"


$(function () {
    $("#register_button").click(function (e) {
        var error_message = ''
        toggle_invalid("input", false)
        toggle_invalid("select", false)
        var phone = $("#phone").val()
        var password = $("#password").val()
        var name = $("#name").val()
        var age = $("#age").val()
        var gender = $("#gender").find("option:selected").val()
        var email = $("#email").val()
        var address = $("#address").val()
        if(phone.trim().length == 0){
            error_message += "电话号码不能为空 "
            toggle_invalid("#phone", true)
        }else if(/^\d+$/.test(phone) == false){
            error_message += "电话号码格式错误 "
            toggle_invalid("#phone", true)
        }
        if(password.trim().length == 0){
            error_message += "密码不能为空 "
            toggle_invalid("#password", true)
        }else if(!/^(\w){6,20}$/.test(password)){
            error_message += "密码格式错误 "
            toggle_invalid("#password", true)
        }
        if(name.trim().length == 0){
            error_message += "姓名不能为空 "
            toggle_invalid("#name", true)
        }
        if(age.trim().length == 0){
            error_message += "年龄不能为空 "
            toggle_invalid("#age", true)
        }else if(/^\d+$/.test(age) == false){
            error_message += "年龄格式错误 "
            toggle_invalid("#age", true)
        }else{
            age = Number.parseInt(age)
            if(age <= 0 || age >= 110){
                error_message += "年龄范围错误 "
                toggle_invalid("#age", true)
            }
        }
        if(gender != "男" && gender != "女"){
            error_message += "性别格式错误 "
            toggle_invalid("#gender", true)
        }
        if(email.trim().length != 0 && !/^\w +[@]\w +[.][\w.] +$/.test(email)){
            error_message += "邮箱格式错误 "
            toggle_invalid("#email", true)
        }
        if(error_message.length != 0){
            alert(error_message, "danger")
        }else{
            //发送请求
            $.ajax({
                type: "post",
                url: "register",
                data: JSON.stringify({
                    phone:phone,
                    password:password,
                    name:name,
                    age:age,
                    gender:gender,
                    email:email,
                    address:address
                }),
                contentType: "application/json",
                dataType: "json",
                success: function (response) {
                    if(response.msg == 'success'){
                        alert("注册成功", "success")
                        window.location.replace("/login")
                    }else{
                        alert(`注册失败:${response.data.error}`, 'danger')
                    }
                },
                error:function(xhr){
                    alert(`错误：${xhr.status} ${xhr.statusText}`, "danger");
                }
            })
        }
    })
})