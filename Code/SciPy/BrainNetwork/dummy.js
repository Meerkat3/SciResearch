//change background color to black
backgroundColor = d3.rgb('#000000')
d3.select("body").style("background-color", backgroundColor)

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

//var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().distance(function(d) {
        return d.distance;
    }).strength(1))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));


(function() {
    graph = {
        "nodes": [{
            "id": "test1",
            "group": 1,
            "size": 10
        }, {
            "id": "test2",
            "group": 1,
            "size": 10
        }, {
            "id": "test3",
            "group": 1,
            "size": 10
        }],
        "links": [{
            "source": "test1",
            "target": "test2",
            "value": 1,
            "distance": 200
        }, {
            "source": "test3",
            "target": "test1",
            "value": 1,
            "distance": 300
        }]
    };
    var nodes = graph.nodes,
        nodeById = d3.map(nodes, function(d) {
            return d.id;
        }),
        links = graph.links,
        bilinks = [];


    //get graphics to make color scale us scaleOrdinal if every color chosen
    var color = d3.scaleOrdinal()
        .domain([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
        .range(["#af1f45", "#be4f5e", "#cd767c", "#dc9d9e", "#ecc9c8", "#fbdbe9", "#f7bbd5", "#f49ac1", "#f179ae", "#ef509c",
            "#e3d4e4", "#cdb1cf", "#9a5699", "#b990ba", "#a973a9", "#d6eaf3", "#b0daeb", "#8acce4", "#5ebfde", "#00a5db", "#6dbe46", "#e0efd4",
            "#c3e0ae", "#a7d48b", "#8cc866", "#fff2d1", "#ffe8a8", "#ffdf80", "#ffd751", "#fecf07", "#fee1c9", "#fcc79c", "#faae74", "#f69d58",
            "#f7964a", "#fde3d9", "#fcccbc", "#f58870", "#f9b4a0", "#f79e87"
        ]);


    links.forEach(function(link) {
        var s = link.source = nodeById.get(link.source),
            t = link.target = nodeById.get(link.target),
            i = {}, // intermediate node
            linkDist = link.distance;
        nodes.push(i);
        //console.log(linkDist);
        bilinks.push([s, i, t, linkDist]);
    });

    var link = svg.selectAll(".link")
        .data(bilinks)
        .enter().append("path")
        .style("stroke", "#6b7071") //gunmetal grey
        .attr("class", "link")
        .attr("fill", "none")



    var node = svg.selectAll(".node")
        .data(nodes.filter(function(d) {
            return d.id;
        }))
        .enter().append("circle")
        .attr("class", "node")
        //change circle size according to new function
        .attr("r", function(d) {
            return d.size
        })
        .attr("fill", function(d) {
            return color(d.group);
        })
        .style("stroke", "#000000")
        //.style("stroke", function(d) { return color(d.group); })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(function(d) {
            return d.id;
        });

    simulation
        .nodes(nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(links);

    function ticked() {
        link.attr("d", positionLink);
        node.attr("transform", positionNode);
    }
}());




function positionLink(d) {
    return "M" + d[0].x + "," + d[0].y + "S" + d[1].x + "," + d[1].y + " " + d[2].x + "," + d[2].y;
}

function positionNode(d) {
    return "translate(" + d.x + "," + d.y + ")";
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x, d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x, d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null, d.fy = null;
}
