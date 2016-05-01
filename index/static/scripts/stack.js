"use strict"
var userName = '2526083';
var allactivies = {
    "Questions": 0,
    "Answers": 0,
    "Question Comments": 0,
    "Answer Comments": 0
};
var n = 4;
$(document).ready(function () {
    var url = "stackchartdata/" + userName;
    $.ajax(
        {
            url: url,
            beforeSend: function (xhr) {

            },
            error: function (xhr) {


            },
            method: "GET"
        }
    )
        .done(function (data) {
            //console.log(data);
            var newdataset = data.result;
            //draw the chart
            populate(newdataset);
        })
        .fail(function () {

        });
});

function populate(newdataset) {
    var stack = d3.layout.stack();
    stack(newdataset);

    var margin = { top: 20, right: 20, bottom: 100, left: 20 },
        width = 790 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    $("#chart-svg").empty();

    var svg = d3.select("#chart-svg").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    var yGroupMax = d3.max(newdataset, function (layer) {
        return d3.max(layer, function (d) { return d.y; });
    });

    //console.log(yGroupMax);

    var yStackMax = d3.max(newdataset, function (d) {
        return d3.max(d, function (d) {
            return d.y0 + d.y;
        });
    });

    //console.log(yStackMax);


    var xScale = d3.scale.ordinal()
        .domain(newdataset[0].map(function (d) { return d.x; }))
        .rangeRoundBands([25, width], .08);

    var y = d3.scale.linear()
        .domain([0, yStackMax])
        .range([height, 0]);

    var color = d3.scale.ordinal()
        .domain(d3.keys(allactivies))
        .range(["#E01933", "#A0EB1E", "#4397F0", "#F09C43"]);
    //.range(["#98ABC5", "#8a89a6", "#7b6888", "#6b486b"]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .tickSize(0)
        .tickPadding(6)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format(".2s"));

    var layer = svg.selectAll(".layer")
        .data(newdataset)
        .enter().append("g")
        .attr("class", "layer")
        .style("fill", function (d, i) { return color(i); });

    var rect = layer.selectAll("rect")
        .data(function (d) { return d; })
        .enter().append("rect")
        .attr("x", function (d) { return xScale(d.x); })
        .attr("y", height)
        .attr("width", xScale.rangeBand())
        .attr("height", 0);


    rect.transition()
        .delay(function (d, i) { return i * 10; })
        .attr("y", function (d) { return y(d.y0 + d.y); })
        .attr("height", function (d) { return y(d.y0) - y(d.y0 + d.y); });

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text").style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", ".15em")
        .attr("transform", function (d) {
            return "rotate(-45)"
        });


    svg.append("g")
        .attr("class", "y axis")
        .attr("id", "yaxis")
        .attr("transform", "translate(20,0)")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr({ "x": -150, "y": -70 })
        .attr("dy", ".75em")
        .style("text-anchor", "end")
        .text("Operations");

    var legend = svg.selectAll(".legend")
        .data(d3.keys(allactivies))
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) { return "translate(-20," + i * 20 + ")"; });

    legend.append("rect")
        .attr("x", width - 176)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 180)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function (d) { return d; });


    d3.selectAll("input[name=\"chartype\"]").on("change", change);


    var timeout = setTimeout(function () {
        d3.select("input[value=\"grouped\"]").property("checked", true).each(change);
    }, 2000);

    function change() {
        clearTimeout(timeout);
        if (this.value === "grouped") transitionGrouped();
        else transitionStacked();
    }

    function transitionGrouped() {

        y.domain([0, yGroupMax]);

        svg.selectAll("#yaxis")
            .call(yAxis);


        rect.transition()
            .duration(500)
            .delay(function (d, i) { return i * 10; })
            .attr("x", function (d, i, j) { return xScale(d.x) + xScale.rangeBand() / n * j; })
            .attr("width", xScale.rangeBand() / n)
            .transition()
            .attr("y", function (d) { return y(d.y); })
            .attr("height", function (d) { return height - y(d.y); });

        rect.on("mouseover", function () { tooltip.style("display", null); })
            .on("mouseout", function () { tooltip.style("display", "none"); })
            .on("mousemove", function (d) {
                var xPosition = d3.mouse(this)[0] - 15;
                var yPosition = d3.mouse(this)[1] - 25;
                tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
                tooltip.select("text").text(d.y);
            });
    }




    function transitionStacked() {
        y.domain([0, yStackMax]);
        svg.selectAll("#yaxis")
            .call(yAxis);

        rect.transition()
            .duration(500)
            .delay(function (d, i) { return i * 10; })
            .attr("y", function (d) { return y(d.y0 + d.y); })
            .attr("height", function (d) { return y(d.y0) - y(d.y0 + d.y); })
            .transition()
            .attr("x", function (d) { return xScale(d.x); })
            .attr("width", xScale.rangeBand());


        rect.on("mouseover", function () { tooltip.style("display", null); })
            .on("mouseout", function () { tooltip.style("display", "none"); })
            .on("mousemove", function (d) {
                var xPosition = d3.mouse(this)[0] - 15;
                var yPosition = d3.mouse(this)[1] - 25;
                //console.log(xPosition);
                tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
                tooltip.select("text").text(d.y);
            });

    }


    var tooltip = svg.append("g")
        .attr("class", "tooltip");

    tooltip.append("rect")
        .attr("width", 30)
        .attr("height", 20)
        .attr("fill", "red")
        .style("opacity", 0.5);

    tooltip.append("text")
        .attr("x", 15)
        .attr("dy", "1.2em")
        .style("text-anchor", "middle")
        .attr("font-size", "12px")
        .attr("font-weight", "bold");
}