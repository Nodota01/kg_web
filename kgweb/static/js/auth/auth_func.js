"use strict"
// 弹出警告框
function alert(message, type) { 
    var holder = $("#live_alert_placeholder")
    holder.children().remove()
    holder.html(`<div class="alert mt-3 alert-${type}" role="alert">${message}</div>`)
}

// 显示或关闭输入框错误
function toggle_invalid(selector, swich) {
    $(selector).toggleClass("is-invalid", swich);
}