var userName = "jayaprakash";

function getParametersByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(document).ready(function () {
    userName = getParametersByName("username");
    var url = "piechartdata/" + userName;
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
            //use the data and populate pie chart
            console.log(data);
            var piechartdata = data.result;
            var id = "#piechart";
            if (id == '#piechart') {
                $(id).empty();
            }
            var wid = 400;
            var hei = 400;
            var radius = Math.min(wid, hei) / 2;

            var colours = ["#00ffff", "#00ff00", "#ffff00", "#ff3300", "#3333cc", "#009933",
                "#0066cc", "#ff00ff", "#9900ff", "#6699ff", "#4d4dff", "#660066",
                "#663300", "#999966", "#9933ff", "#ffffff"];
            /*var topics = {};
            $.each(data.result, function(key, t){
                topics[t.Name]=0;
            } );
            console.log(topics);*/
            var colors = d3.scale.linear()
                .domain(d3.keys(piechartdata))
                .range(colours);

            /*var colors = d3.scale.ordinal()
                .domain(d3.keys(piechartdata));*/

            var svg = d3.select(id)
                .append('svg')
                .attr('width', wid)
                .attr('height', hei)
                .append('g')
                .attr('transform', 'translate(' + (wid / 2) + ',' + (hei / 2) + ')');

            var arc = d3.svg.arc().outerRadius(radius);
            var pie = d3.layout.pie()
                .value(function (d) { return d.Duration; })
                .sort(null);
            var path = svg.selectAll('path')
                .data(pie(piechartdata))
                .enter()
                .append('path')
                .attr('d', arc)
                .attr('fill', function (d, i) {
                    
                    return colors(i);//
                });

            var tooltip = d3.select(id)            // NEW 
                .append('div')                             // NEW
                .attr('class', 'tooltipPiechart');                 // NEW

            tooltip.append('div')                        // NEW
                .attr('class', 'label');                   // NEW

            tooltip.append('div')                        // NEW
                .attr('class', 'count');                   // NEW

            tooltip.append('div')                        // NEW
                .attr('class', 'percent');                 // NEW

            path.on('mouseover', function (d) {
                var total = d3.sum(piechartdata.map(function (d) {
                    return d.Duration;
                }));
                var percent = Math.round(1000 * d.data.Duration / total) / 10;
                tooltip.select('.label').html(d.data.Name);
                tooltip.select('.count').html(d.data.Duration);
                tooltip.select('.percent').html(percent + '%');
                tooltip.style('display', 'block');
            });
           /* 
            var legendRectSize = 18;
            var legendSpacing = 4;
            
            var legend = svg.selectAll('.legend')
                .data(colors.domain())
                .enter()
                .append('g')
                .attr('class', 'legend')
                .attr('transform', function (d, i) {
                    var height = legendRectSize + legendSpacing;
                    var offset = height * colors.domain().length / 2;
                    var horz = -2 * legendRectSize;
                    var vert = i * height - offset;
                    return 'translate(' + horz + ',' + vert + ')';
                });

            legend.append('rect')
                .attr('width', legendRectSize)
                .attr('height', legendRectSize)
                .style('fill', colors)
                .style('stroke', colors);


            legend.append('text')
                .attr('x', legendRectSize + legendSpacing)
                .attr('y', legendRectSize - legendSpacing)
                .text(function (d) { return d; });


                */
            path.on('mouseout', function () {
                tooltip.style('display', 'none');
            });

            path.on('mousemove', function (d) {
                tooltip.style('top', (d3.event.layerY + 10) + 'px')
                    .style('left', (d3.event.layerX + 10) + 'px');
            });


        })
        .fail(function () {
            console.log("Error");
        });
});


