"use strict"

var cur_url = window.location.protocol + "//"
    + window.location.hostname + ":" + window.location.port + "/"

function search() {
    //Echarts绘图
    var mychart = echarts.init(document.getElementById("chart"), null, { renderer: 'svg' })
    window.onresize = function () { mychart.resize() }
    var search_text = $("#search_text")
    if (search_text.val().length == 0) {
        return
    }
    var obj = {
        key_word: search_text.val()
    }
    $.ajax({
        type: "post",
        url: cur_url + "q",
        data: JSON.stringify(obj),
        contentType: "application/json",
        dataType: "json",
        success: function (response) {
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
                    show: true,
                    trigger: 'item',
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
                            repulsion: 1500,
                            edgeLength: [100, 150]
                        },
                        draggable: true,//是否可以拖拽
                        label: {        //节点标签
                            show: true,
                            color: '#000',
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
            };
            mychart.setOption(options)
        }
    });
}

$(document).ready(function () {
    //搜索请求
    $("#search_text").keydown(function (e) {
        if (e.which == 13) {
            search()
        }
    });
    $("#search_button").click(function (e) {
        search()
    });

    //选定搜索类型更改文本
    $(".type_option").click(function (e) { 
        var type = $(this).text()
        $(".type_text").text(type);
    });


    // //SVG画图（需要d3）
    // var width = 300;
    // var height = 300;
    // var svg = d3.select("body")     //选择文档中的body元素
    //     .append("svg")          //添加一个svg元素
    //     .attr("width", width)
    //     .attr("height", height);

    // var dataset = [ 2.5 , 2.1 , 1.7 , 1.3 , 0.9 ]
    // var linear = d3.scaleLinear() //创建线性比例尺
    // .domain([0, d3.max(dataset)])
    // .range([0, 250]);
    // var rectheight = 25
    // svg.selectAll("rect")
    //     .data(dataset)
    //     .enter()
    //     .append("rect")
    //     .attr("x", 20)
    //     .attr("y", function (d, i) { return i * rectheight })
    //     .attr("width", function (d) { return linear(d) })
    //     .attr("height", rectheight - 2)
    //     .attr("fill", "steelblue")
    // //创建坐标轴
    // var axis = d3.axisBottom().scale(linear).ticks(7)
    // svg.append("g").call(axis)
});