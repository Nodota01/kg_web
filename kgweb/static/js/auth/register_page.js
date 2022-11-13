"use strict"

// 弹出警告框
function alert(message, type) { 
    var holder = $("#live_alert_placeholder")
    holder.children().remove()
    holder.html(`<div class="alert mt-3 alert-${type}" role="alert">${message}</div>`)
}

$(function () {
    
})