"use strict"

const cur_url = window.location.protocol + "//"
    + window.location.hostname + ":" + window.location.port + "/"

//读type_prop.json
function read_file(name) { // name为文件所在位置
    let xhr = new XMLHttpRequest(),
        okStatus = document.location.protocol === "file:" ? 0 : 200
    xhr.open('GET', name, false)
    xhr.overrideMimeType("text/html;charset=utf-8")//默认为utf-8
    xhr.send(null)
    return xhr.status === okStatus ? xhr.responseText : null
}
const fp = JSON.parse(read_file('static/data/type_prop.json'))
const quesn_data = JSON.parse(read_file("static/data/form_data.json"))
const judge_standard = JSON.parse(read_file("static/data/judge_standard.json"))

//搜索方法
function search() {
    //Echarts绘图
    var mychart = echarts.init(document.getElementById("chart"), null, { renderer: 'svg' })
    //点击结点事件
    mychart.off('click')
    mychart.on('click', function (params) {
        if (params.dataType == 'node') {
            console.log(params);
            //显示节点详情模态框
            $("#node_detail_modal").modal("show")
            $("#node_detail_title").text(params.name)
            var text = ''
            for (let o in params.data.des) {
                text += '<h5 class="text-dark bg-light p-2">' + o + '</h5>'
                text += '<p class="text-dark">' + params.data.des[o] + '</p>'
            }
            $("#node_detail_content").children().remove()
            $("#node_detail_content").text('')
            $("#node_detail_content").append(text)
        }
    })
    window.onresize = function () { mychart.resize() }
    var search_text = $("#search_text")
    //检查关键字
    if (search_text.val().length == 0) {
        $("#search_result").text('请输入关键字')
        return
    } else if ($("#type_text").text().trim() == '类型' || $("#prop_text").text().trim() == '属性') {
        $("#search_result").text('请选择类型和属性')
        return
    } else {
        $("#search_result").text('Loading.....')
        $("#search_loadding").toggleClass('invisible')
    }
    var obj = {
        type: $("#type_text").text(),
        prop: $("#prop_text").text(),
        key_word: search_text.val()
    }
    $.ajax({
        type: "post",
        url: cur_url + "q",
        data: JSON.stringify(obj),
        contentType: "application/json",
        dataType: "json",
        success: function (response) {
            $("#search_loadding").toggleClass('invisible')
            if (response.msg == 'fail') {
                $("#search_result").text('错误')
                return
            } else if (response.msg == 'empty') {
                $("#search_result").text('无结果')
                return
            }
            $("#search_result").text('共找到' + response.data.nodes.length + '个节点')
            //类别集合
            //var categories = [{ name: "ca" }, { name: "cb" }, { name: "cd" }];
            /** @type EChartsOption */
            const options = {
                // title: {
                //     text: 'Basic Graph'
                // },
                //提示框
                tooltip: {
                    show: false,
                    trigger: 'item',
                    confine: true,
                    textStyle: {
                        width: 30,
                        overflow: 'truncate'
                    },
                    formatter: function (x) {
                        return x.data.des;
                    }
                },
                //工具箱
                toolbox: {
                    // 显示工具箱
                    show: true,
                    feature: {
                        // 还原
                        restore: {
                            show: true
                        },
                        // 保存为图片
                        saveAsImage: {
                            show: true
                        }
                    }
                },
                //设置图例
                legend: [{
                    show: true,
                    // selectedMode: 'single',
                    data: response.data.categories.map(function (a) {
                        return a.name;
                    })
                }],
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series: [
                    {
                        type: 'graph',
                        layout: 'force',
                        symbolSize: 60,  //节点大小
                        roam: true,     //是否可以缩放
                        force: {        //节点之间的斥力
                            repulsion: 800,
                            edgeLength: [180, 200, 230]
                        },
                        draggable: true,//是否可以拖拽
                        label: {        //节点标签
                            show: true,
                            color: '#000',
                            formatter: function (x) {
                                return x.data.name;
                            }
                        },
                        edgeSymbol: ['none', 'arrow'], //边两端的形状
                        edgeSymbolSize: [4, 10],        //边两端标记的大小
                        edgeLabel: {
                            fontSize: 12,
                            show: true,
                            color: '#000',
                            borderWidth: 1,
                            formatter: function (x) {
                                return x.data.des;
                            }
                        },
                        categories: response.data.categories,
                        //节点集
                        nodes: response.data.nodes,
                        //边集
                        edges: response.data.edges,
                        lineStyle: {
                            opacity: 0.9,
                            width: 2,
                            curveness: 0.1
                        }
                    }
                ],
            }
            mychart.setOption(options)
        }
    })
}

$(document).ready(function () {
    //搜索请求
    $("#search_text").keydown(function (e) {
        if (e.which == 13) {
            search()
        } else {
            return
        }
    })
    $("#search_button").click(function (e) {
        search()
    })

    // //选定搜索类型更改文本
    // $(".type_option").click(function (e) { 
    //     var type = $(this).text()
    //     $(".type_text").text(type);
    // });

    //修改下拉菜单选项
    $("#type_list").children().remove()
    $("#prop_list").children().remove()
    for (let k in fp) {
        $("#type_list").append("<li><a class=\"dropdown-item type_option\">" + k + "</a></li>")
    }
    $(".type_option").click(function (e) { //点选类型后更改属性
        $("#type_text").text($(this).text())
        $("#prop_list").children().remove()
        $("#prop_text").text('属性')
        for (let p of fp[$(this).text()]) {
            $("#prop_list").append("<li><a class=\"dropdown-item prop_option\">" + p + "</a></li>")
        }
        $(".prop_option").click(function (e) {
            $("#prop_text").text($(this).text())
        })
    })

    //显示问卷模态框，并排版问卷
    const pick_answer = ["没有", "很少", "有时", "经常", "总是"]
    const toggle_answer = ["无", "有"]
    const tb = $("#questionnaire_body")
    const row_template = $("#row_template").clone()
    const radio_template = $(".form-check").first().clone()
    $("#questionnaire_button").click(function (e) {
        tb.children().remove()
        quesn_data.forEach(ques => {
            var row = row_template.clone()
            row.attr("id", "row_" + ques["position"])
            row.find("th").text(ques["position"])
            row.find("td").eq(0).text(ques["question"])
            var radio_group = row.find("td").eq(1)
            radio_group.children().remove()
            var ans_set
            if (ques["type"] == "pick") {
                ans_set = pick_answer
            } else if (ques["type"] == "toggle") {
                ans_set = toggle_answer
            }
            ans_set.forEach(function (ans, index){
                var radio = radio_template.clone()
                var p = index + 1
                radio.find("input").attr({
                    name: "row_" + ques["position"],
                    id: "row_" + ques["position"] + "_" + p,
                    value: index
                })
                if(index == 0){
                    radio.find("input").prop("checked", true)
                }
                radio.find("label").attr("for", "row_" + ques["position"] + "_" + p)
                radio.find("label").text(ans)
                radio_group.append(radio)
            })
            tb.append(row)
        })
        $("#questionnaire_modal").modal("show")
    })
    //问卷提交事件
    $("#questionnaire_submit_button").click(function (e) { 
        //获取分数
        var score = new Array()
        for(let i = 1; i < quesn_data.length + 1; i++){
            score[i - 1] = $(`input[name='row_${i}']:checked`).val()
        }
        //评分
        var symps = new Array()
        judge_standard.forEach(jstan => {
            var sum = 0
            jstan["clause_position"].forEach(function(pos, i){
                sum += score[pos - 1] * jstan["weight"][i]
            })
            if(sum >= jstan["threshold"]){
                symps.push(jstan["name"])
            }
        })
        $("#search_result").text(String(symps))
    })
})