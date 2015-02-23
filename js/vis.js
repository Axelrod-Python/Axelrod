(function() {

    // the visualisation
    var svg;
    var container;

    // get the size of the visualisation element
    var width = document.getElementById('vis').clientWidth;
    var height = document.getElementById('vis').clientHeight;

    // some padding around the visualisation
    var padding = {'bottom': 170, 'left': 90, 'right': 40, 'top': 40};

    // scale from median values to height
    var y_scale = d3.scale.linear()
        .range([height-padding.bottom, padding.top]);

    // scale from player name to width
    var x_scale = d3.scale.ordinal()
        .rangeRoundBands([padding.left, width-padding.right], 0.5, 0.4);

    // scale from median value to colour
    var colour_scale = d3.scale.quantile()
        .range(colorbrewer.Blues[9]);
    var cheater_scale = d3.scale.quantile()
        .range(colorbrewer.Greens[9]);

    // axes
    var x_axis = d3.svg.axis()
        .scale(x_scale)
        .orient('bottom');

    var y_axis = d3.svg.axis()
        .scale(y_scale)
        .orient('left');

    // axes
    var x_axis = d3.svg.axis()
        .scale(x_scale)
        .orient('bottom');

    var y_axis = d3.svg.axis()
        .scale(y_scale)
        .orient('left');

    // how long transitions will last
    var transition_duration = 1000;

    // function for handling zoom event
    var zoom_handler = function() {
        
        svg.select('.y.axis')
            .transition()
            .call(y_axis);

        svg.select('.x.axis')
            .transition()
            .attr('transform', 'translate(' + d3.event.translate[0] + ',' +(height-padding.bottom)+ ')')
            .call(x_axis.scale(x_scale.rangeRoundBands([padding.left * d3.event.scale, (width-padding.right) * d3.event.scale],.5 * d3.event.scale, .4 * d3.event.scale)));

        svg.select('.x.axis')
            .selectAll('text')
            .style('text-anchor', 'end');

        container.attr('transform', 'translate(' + d3.event.translate + ')scale(' + d3.event.scale + ')');
    }


    // find the indexes of the whisker reach values
    function whisker_reach(d, k) {
        var q1 = d3.quantile(d, 0.25);  // first quartile
        var q3 = d3.quantile(d, 0.75);  // third quartile
        var reach = (q3 - q1) * k;      // reach
        var i = -1;                     // start at the beginning
        while (d[++i] < (q1 - reach));    // find the first non-outlier
        var j = d.length;               // start at the end
        while (d[--j] > (q3 + reach));    // find the first non-outlier
        return [i, j];                  // return the indexes
    }

    var zoom = d3.behavior.zoom()
        .scaleExtent([0, 10])
        .on("zoom", zoom_handler)
        .y(y_scale);

    // data
    var results;
    // player names
    var players;
    var cheaters;

    // initialise the visualisation
    var init_plot = function() {
        
        // read the cheaters names from the results file
        d3.csv('cheating_results.csv', function(error, data) {
            // extract the list of cheating players
            cheaters = data.map(function(d) {
                return d.player;
            });
        });

        // create the svg element to hold 
        // all the visualisation elements
        svg = d3.select('#vis')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .call(zoom);

        container = svg.append('g')
            .attr('class', 'container')
            .call(zoom);

        svg.append('rect')
            .attr('x', padding.left)
            .attr('y', height - padding.bottom)
            .attr('width', width - padding.right)
            .attr('height', padding.bottom)
            .attr('fill', 'white')
            .attr('stroke', 'none');

        svg.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', padding.left)
            .attr('height', height)
            .attr('fill', 'white')
            .attr('stroke', 'none');

        // add an x-axis element
        svg.append('g')
          .attr('class', 'x axis')
          .attr('transform', 'translate(0,' + (height-padding.bottom) + ')');

        // rotate the x-axis labels
        svg.selectAll('.x.axis text')
            .style('text-anchor', 'end')
            .attr('transform', 'translate(-15,10)rotate(-90)');

        // add a y-axis and label
        svg.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + (padding.left) + ", " + "0)")
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 20 - padding.left)
          .attr("x", 0 - (height/2))
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text("Mean score per game over 200 rounds repeated 50 times");

    }

    // function to draw a circle for an outlying data value
    var draw_outlier = function(element, x, y) {
        var circle = element.append('circle')
            .attr('cx', x)
            .attr('cy', y)
            .attr('r', 2)
            .attr('stroke', '#aaa')
            .attr('stroke-width', 0.5)
            .attr('fill', 'none')
            .attr('class', 'outlier')
            .style('opacity', 0);            
    }

    var reset = function() {
        svg.remove();
        var sel = document.getElementById('result_select');
        var selected = sel.options[sel.selectedIndex].value;

        // reset y_scale scale from median values to height
        y_scale = d3.scale.linear()
            .range([height-padding.bottom, padding.top]);

        // reset x_scale from player name to width
        x_scale = d3.scale.ordinal()
            .rangeRoundBands([padding.left, width-padding.right], 0.5, 0.4);
        
        // reset x_axis
        x_axis = d3.svg.axis()
            .scale(x_scale)
            .orient('bottom');

        // reset y_axis
        y_axis = d3.svg.axis()
            .scale(y_scale)
            .orient('left');
        
        // reinitialise plot
        init_plot();

        // load the currently selected results set
        load_results(selected);        
    }

    // load results from the specified file
    var load_results = function(results) {
        
        d3.csv(results + '.csv', function(error, data) {

            // extract the list of players
            players = data.map(function(d) {
                return d.player;
            });

            // coerce data into a proper format - array of numerical scores
            data.forEach(function(d){
                var temp = d.scores.replace('[', '')
                temp = temp.replace(']', '')
                scores = temp.split(',')
                d.scores = scores.map(function(s) { return +s/(200 * (players.length-1)); });
                d.scores = d.scores.sort();
            });

            results = data;

            // calculate max and min values across all scores
            var max = d3.max(results, function(d){ return d3.max(d.scores); });
            var min = d3.min(results, function(d){ return d3.min(d.scores); });

            // calculate median score for each player
            var medians = data.map(function(d) {
                return d3.median(d.scores);
            });

            // set the scale domain values 
            colour_scale.domain(medians);
            cheater_scale.domain(medians);
            y_scale.domain([min, max]);
            x_scale.domain(players);

            zoom.y(y_scale);

            // draw the visualisation
            draw_plot(results);
        });
    }

    // function to draw a box_plot of the results
    var draw_plot = function(result_set) {
    
        // remove any existing box-and-whisker plots
        container.selectAll('.box')
            .style("opacity", 0)
            .remove();

        // select all box-and-whisker plots
        // (there aren't any) and bind data
        // to them
        var boxes = container.selectAll('.box')
            .data(result_set);

        // add a box for each of the results
        var box = boxes
            .enter()
            .append('g')
            .attr('class', function(d){ return "box " + d.player; });

        // draw a rectangle for the inter-quartile range for each player
        box
            .append('rect')
            .attr('class', 'quartiles')
            .attr('x', function(d) {
                return x_scale(d.player)
            })
            .attr('width', x_scale.rangeBand())
            .attr('y', function(d){
                var upper_quartile = d3.quantile(d.scores, 0.75);
                return y_scale(upper_quartile);
            })
            .attr('height', function(d) {
                var lower_quartile = d3.quantile(d.scores, 0.25);
                var upper_quartile = d3.quantile(d.scores, 0.75);
                return y_scale(lower_quartile)-y_scale(upper_quartile);
            })
            .attr("fill", function(d) {
                if(cheaters.indexOf(d.player) == -1) {
                    return colour_scale(d3.median(d.scores));    
                } else {
                    return cheater_scale(d3.median(d.scores));    
                }
                
            })
            .attr("stroke", function(d) {
                if(cheaters.indexOf(d.player) == -1) {
                    return "blue";
                } else {
                    return "green";
                }
            })
            .style('opacity', 0);
        
        // draw a line for the median for each player
        box
            .append('path')
            .attr('class', 'median')
            .attr('d', function(d) {
                var median = d3.median(d.scores);
                var band_width = x_scale.rangeBand();
                var x_start = x_scale(d.player);
                var y = y_scale(median);
                var path = "M " + x_start + " " + y + " L " + " " + (x_start+band_width) + " " + y;
                return path;
            })
            .attr('stroke', 'red')
            .attr('stroke-width', '2')
            .style('opacity', 0);

        // draw the upper whisker (and any outliers)
        box
            .append('path')
            .attr('class', 'upper-whisker')
            .attr('d', function(d) {
                var lower_quartile = d3.quantile(d.scores, 0.25);
                var upper_quartile = d3.quantile(d.scores, 0.75);
                var i = whisker_reach(d.scores, 1.5);
                var reach = d.scores[i[1]];
                var band_width = x_scale.rangeBand();
                var x_start = x_scale(d.player);
                var midpoint = x_start + (band_width/2);

                if(i[1] < d.scores.length-1) {
                    for(var j = i[1]+1; j < d.scores.length; j++) {
                        draw_outlier(box, midpoint, y_scale(d.scores[j]));
                    }
                }

                var path = "M " + midpoint + " " + y_scale(upper_quartile) + " L " + midpoint + " " + y_scale(reach) + " " + (x_start + band_width) + " " + y_scale(reach) + " " + x_start + " " +  y_scale(reach);
                return path;
            })
            .attr('stroke', 'black')
            .attr('fill', 'none')
            .style('opacity', 0);

        // draw the lower whisker (and any outliers)
        box
            .append('path')
            .attr('class', 'lower-whisker')
            .attr('stroke', 'black')
            .attr('fill', 'none')
            .attr('d', function(d) {
                var lower_quartile = d3.quantile(d.scores, 0.25);
                var upper_quartile = d3.quantile(d.scores, 0.75);
                var i = whisker_reach(d.scores, 1.5);
                var reach = d.scores[i[0]];
                var band_width = x_scale.rangeBand();
                var x_start = x_scale(d.player);
                var midpoint = x_start + (band_width/2);
                if(i[0] > 0) {
                    for(var j = 0; j < i[0]; j++) {
                        draw_outlier(box, midpoint, y_scale(d.scores[j]));
                    }
                }

                var path = "M " + midpoint + " " + y_scale(lower_quartile) + " L " + midpoint + " " + y_scale(reach) + " " + (x_start + band_width) + " " + y_scale(reach) + " " + x_start + " " +  y_scale(reach);
                return path;
            })
            .style('opacity', 0);

        // once all the elements are drawn, fade them in
        boxes.selectAll('.median')
            .transition()
            .duration(transition_duration)
            .style('opacity', 1);

        boxes.selectAll('.quartiles')
            .transition()
            .duration(transition_duration)
            .style('opacity', 1);

        boxes.selectAll('.upper-whisker')
            .transition()
            .duration(transition_duration)
            .style('opacity', 1);

        boxes.selectAll('.lower-whisker')
            .transition()
            .duration(transition_duration)                
            .style('opacity', 1);

        boxes.selectAll('.outlier')
            .transition()
            .duration(transition_duration)                
            .style('opacity', 1);

        // fade out and remove any boxes 
        // that don't have data
        // (there shouldn't be any)
        boxes
            .exit()
            .transition()
            .duration(transition_duration)
            .style('opacity', 0)
            .remove();
          
        // update the axes
        svg.select('.x.axis')
            .transition()
            .duration(transition_duration)
            .call(x_axis);

        svg.select('.x.axis')
            .selectAll('text')
            .attr('transform', 'translate(-15, 15)rotate(-90)')
            .style('text-anchor', 'end');

        svg.select('.y.axis')
            .transition()
            .duration(transition_duration)
            .call(y_axis);
    }


    // register a listener on the <select> form element
    d3.select('#result_select').on('change', function() {
        var selected = this.options[this.selectedIndex].value;
        load_results(selected);
    });

    d3.select('#reset').on('click', reset);

    // initialise the plot and draw some results
    init_plot();
    load_results('all_results');

})();