// ---- GLOBAL VARIABLES -----------------------
var width = 6;
var height = 6;
var n = 85;
story = "";

// ------------------ Play and reset Buttons --------------
$("#play-button").on("click", () => {
    var button = $("#play-button");
    if (button.text() == "Play") {
        button.text("Pause");
        interval = setInterval(step, 1000);
    } else {
        button.text("Play");
        clearInterval(interval);
    }
});

$("reset-button").on("click", () => {
    pos = 0;
});


// -------------------- Make the grid-----------------


function gridData(day) {
    var array = new Array();

    // iterate for rows
    for (var row = 1; row <= day.length; row++) {
        array.push(new Array());

        // iterate for cells/columns inside rows
        for (var column = 1; column <= day[row - 1].length; column++) {
            array[row - 1].push({
                x: row * width,
                y: column * height,
                width: width,
                height: height,
                color: day[column - 1][row - 1]
            })
        }
    }
    return array;
}

function color(color){
    console.log(color);
    var string = "#ffffff";
    if(color == 30){ string = "#faacf9"; }
    else if(color == 60){ string = "#9cf7e2"; }
    else if(color == 90){ string = "##f79cca"; }
    else if(color == 120){ string = "#9cf7b1"; }
    else if(color == 150){ string = "#f7f19c"; }
    else if(color == 180){ string = "#ba9cf7"; }
    else if(color == 210){ string = "#f79c9c"; }
    return string;
}

var grid = d3.select("#grid")
    .append("svg")
    .attr("width", (width * n) + "px")
    .attr("height", (height * n) + "1000px");



// ---- Change the grid depending on the story ----------------

$("#story-select").on("change", () => {
    var select = $("#story-select").val();
    story = "data/".concat(select).concat(".json");
    console.log(story)
    d3.json(story).then((data) => {
        var days = data.map((d) => {
            return d;
        });

        days.forEach(day => {
            var gridInfo = gridData(day);
            console.log("vuelta");
            var row = grid.selectAll(".row")
                .data(gridInfo)
                .enter().append("g")
                .attr("class", "row")

            var column = row.selectAll(".square")
                .data(function (d) {
                    return d;
                })
                .enter().append("rect")
                .attr("class", "square")
                .attr("x", function (d) {
                    return d.x;
                })
                .attr("y", function (d) {
                    return d.y;
                })
                .attr("width", function (d) {
                    return d.width;
                })
                .attr("height", function (d) {
                    return d.height;
                })
                .style("fill", (d) => {
                    return color(d.color);
                })
                .style("stroke", "#ffff")
        });
        
    }).catch((error) => {
        console.log(error);
    });
});

