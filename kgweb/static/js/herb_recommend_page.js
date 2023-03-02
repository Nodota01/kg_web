$(function () {
    //生成功能
    $("#generate_button").click(function (e) {
        if ($("input:checked").length == 0) {
            return
        }
        syps = $.map($("input:checked"), function (element, index) {
            return $(element).val()
        })
        $.ajax({
            type: "post",
            url: "get_herbs",
            data: JSON.stringify({
                symps: syps,
                k: Number.parseInt($("option:selected").val())
            }),
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                if (response.msg == 'success') {
                    col = $("#herbs_col")
                    col.empty()
                    //添加下拉按钮
                    for (let herb in response.data) {
                        item = $(`
                        <select class="d-inline mx-2 w-auto form-select my-1">
                            <option value="${herb}" selected>${herb}</option>
                        </select>`)
                        for (let simi_herb of response.data[herb]) {
                            item.append(`<option value="${simi_herb}">${simi_herb}</option>`)
                        }
                        col.append(item)
                    }
                    //为下拉列表添加事件

                } else {
                    alert(`获取药方失败:${response.data.error}`)
                }
            },
            error: function (xhr) {
                alert(`错误：${xhr.status} ${xhr.statusText}`)
            }
        })
    })

    //点选症状加入症状框中
    $("input").change(function (e) {
        if($(this).prop("checked")){
            d = $(`<div class="d-inline text-center border rounded p-2 m-1 h-auto" value="${$(this).val()}">${$(this).val()} </div>`)
            $("#symps_col").append(d)
        }else{
            $("#symps_col").children(`div[value="${$(this).val()}"]`).remove()
        }
    })
})