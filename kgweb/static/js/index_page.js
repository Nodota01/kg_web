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
                text += '<p class="text-dark p-2">' + params.data.des[o] + '</p>'
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
    const fp = JSON.parse(read_file('static/data/type_prop.json'))

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

    
})