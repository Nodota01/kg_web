"use strict"

// 获取用户POST请求
function get_user_post(page, query, on_success, on_error) {
    $.ajax({
        type: "post",
        url: "user",
        data: JSON.stringify({
            page: page,
            query_type: query.query_type,
            query_data: query.query_data
        }),
        contentType: "application/json",
        dataType: "json",
        success: function (response) {
            on_success(response)
        },
        error: function (xhr) {
            on_error(xhr)
        }
    })
}
const trans_user_dict = {
    phone: "电话",
    name: "姓名",
    age: "年龄",
    gender: "性别",
    address: "地址",
    role: "角色",
    created: "注册日期"
}
var trans_user_dict_vers = new Object()
for (let k in trans_user_dict) {
    trans_user_dict_vers[trans_user_dict[k]] = k
}
const search_type = ['id', '电话', '姓名']

$(function () {
    var current_page = 1
    var next_page = null
    var prev_page = null
    var query_type = null
    var query_data = null
    var users = new Array()

    //前往指定页数并更新页面
    function go_page(page) {
        get_user_post(page, { query_type: query_type, query_data: query_data }, function (response) {
            if (response.msg == 'fail') {
                alert('get_user 请求体数据错误')
            } else if (response.msg == 'empty') {
                alert(`无搜索结果`)
            } else if (response.msg == 'success') {
                var table_body = $("#table_body")
                table_body.children().remove()
                users = response.data.items
                response.data.items.forEach(user => {
                    var tr = $('<tr style="cursor:pointer"></tr>')
                    tr.append($(`<th scope="row">${user["id"]}</th>`))
                    tr.append($(`<td>${user["name"]}</td>`))
                    tr.append($(`<td>${user["phone"]}</td>`))
                    tr.append($(`<td>${user["gender"]}</td>`))
                    //点击显示用户详情
                    tr.click(function (e) {
                        var user_id = Number.parseInt(tr.find("th").text())
                        var cur_user = null
                        for (let u of users) {
                            if (u['id'] == user_id) {
                                cur_user = u
                                break
                            }
                        }
                        if (cur_user == null) return
                        $("#detail_title").text(user.name)
                        var detail_content = $("#detail_content")
                        detail_content.children().remove()
                        for (let k in cur_user) {
                            var kv = k
                            if (Object.hasOwnProperty.call(trans_user_dict, k)) {
                                kv = trans_user_dict[k]
                            }
                            detail_content.append(`<h5 class="text-dark bg-light p-2">${kv}</h5>`)
                            detail_content.append(`<p class="text-dark p-2">${cur_user[k]}</p>`)
                        }
                        $("#detail_modal").modal("show")
                    })
                    table_body.append(tr)
                })
                //更新分页导航栏
                $("#page_info").text(`${response.data.first} ~ ${response.data.last} in ${response.data.total}`)
                var pre_pb = $("#pre_page_button")
                var next_pb = $("#next_page_button")
                //往前翻页
                pre_pb.off()
                pre_pb.click(function (e) {
                    if (prev_page == null) return
                    current_page = prev_page
                    go_page(current_page)
                })
                //往后翻页
                next_pb.off()
                next_pb.click(function (e) {
                    if (next_page == null) return
                    current_page = next_page
                    go_page(current_page)
                })
                next_page = response.data.next_num
                prev_page = response.data.prev_num
                pre_pb.toggleClass("disabled", !response.data.has_prev)
                next_pb.toggleClass("disabled", !response.data.has_next)
                $(".page-num").remove()
                for (let p of response.data.iter_pages) {
                    if (p != null) {
                        if (p == current_page) {
                            next_pb.before($(`<li class="page-num page-item active"><a class="page-link" href="#">${p}</a></li>`))
                        } else {
                            var pb = $(`<li class="page-num page-item"><a class="page-link" href="#">${p}</a></li>`)
                            pb.click(function (e) {
                                current_page = p
                                go_page(p)
                            })
                            next_pb.before(pb)
                        }
                    } else {
                        next_pb.before($(`<li class="page-num page-item disabled"><a class="page-link" href="#">...</a></li>`))
                    }
                }

            }
        },
            function (xhr) {
                alert(`错误：${xhr.status} ${xhr.statusText}`)
            })
    }

    //设置搜索框
    $("#type_list").children().remove()
    for (let v of search_type) {
        var li = $(`<li><a class="dropdown-item type_option">${v}</a></li>`)
        li.click(function (e) {
            $("#type_text").text($(this).find("a").text())
        })
        $("#type_list").append(li)
    }
    go_page(current_page)
    //搜索动作
    function search_func () {
        var type_text = $("#type_text").text().trim()
        var data_text = $("#search_text").val().trim()
        if (type_text == "字段" || data_text.length == 0) return
        query_type = type_text
        query_data = data_text
        //翻译成数据库字段
        if (Object.hasOwnProperty.call(trans_user_dict_vers, type_text)) {
            query_type = trans_user_dict_vers[query_type]
        }
        current_page = 1
        go_page(current_page)
    }
    $("#search_button").click(search_func)
    $("#search_text").keydown(function (e) { 
        if(e.which == 13){
            search_func()
        }else return
    })
    //清空搜索
    $("#clear_search_button").click(function (e) { 
        query_type = null
        query_data = null
        current_page = 1
        $("#search_text").val("")
        $("#type_text").text("字段")
        go_page(current_page)
    })
})