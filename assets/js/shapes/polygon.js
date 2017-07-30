export const showPolygon = (n) => {
    var Snap = require('snapsvg')
    var svg_el = "#svg";
    var paper = Snap(svg_el);

    var colors = ['#f0adcc', '#e794b1', '#d68080', '#e36363', '#e32e2e'];

    var translation = 100;
    var buffer = 50;
    var percentage_multiplier = 50*Math.sqrt(2);
    var scalar = .80;

    paper.attr({
        height: percentage_multiplier*2+buffer,
        width: percentage_multiplier*2+buffer
    });

    var center = {x: translation, y: translation};
    var top_left = {x: -percentage_multiplier+translation, y: (translation - percentage_multiplier)};
    var top_right = {x: percentage_multiplier+translation, y: (translation - percentage_multiplier)};
    var bottom_right  = {x: percentage_multiplier+translation, y: (translation + percentage_multiplier)};
    var bottom_left = {x: -percentage_multiplier+translation, y: (translation + percentage_multiplier)}

    var points = {
        mention_percentage: n,
        retweet_percentage: .10,
        link_percentage: .80,
        hash_percentage: .50,
        verbosity: 0,
    }
    //convert to cartesian
    var a = {x: -points.mention_percentage*percentage_multiplier, 
                y: points.mention_percentage*percentage_multiplier};
    var b = {x: points.retweet_percentage*percentage_multiplier, 
                y: points.retweet_percentage*percentage_multiplier};
    var c = {x: points.link_percentage*percentage_multiplier, 
                y: -points.link_percentage*percentage_multiplier};
    var d = {x: -points.hash_percentage*percentage_multiplier, 
                y: -points.hash_percentage*percentage_multiplier};

    var start_points = [a.x+translation, (translation - a.y),
                        b.x+translation, (translation - b.y),
                        c.x+translation, (translation - c.y),
                        d.x+translation, (translation - d.y),
                    ];
    var end_points = [a.x*scalar+translation, (translation - a.y*scalar),
                        b.x*scalar+translation, (translation - b.y*scalar),
                        c.x*scalar+translation, (translation - c.y*scalar),
                        d.x*scalar+translation, (translation - d.y*scalar),
                    ];

    //debugging
    // var circle = paper.circle(center.x, center.y, 5);
    var triangle0_start_points = [start_points[0], start_points[1], 
                                start_points[2], start_points[3], 
                                center.x, center.y];
    var triangle0_end_points = [end_points[0], end_points[1], 
                                end_points[2], end_points[3], 
                                center.x, center.y];
    var triangle0 = paper.polygon(triangle0_start_points);
    triangle0.attr({
        fill: colors[0]
    });
    var triangle1_start_points = [start_points[2], start_points[3], 
                                start_points[4], start_points[5], 
                                center.x, center.y];
    var triangle1_end_points = [end_points[2], end_points[3], 
                                end_points[4], end_points[5], 
                                center.x, center.y];
    var triangle1 = paper.polygon(triangle1_start_points);
    triangle1.attr({
        fill: colors[1]
    });
    var triangle2_start_points = [start_points[4], start_points[5], 
                                start_points[6], start_points[7], 
                                center.x, center.y];
    var triangle2_end_points = [end_points[4], end_points[5], 
                                end_points[6], end_points[7], 
                                center.x, center.y];
    var triangle2 = paper.polygon(triangle2_start_points);
    triangle2.attr({
        fill: colors[0]
    });
    var triangle3_start_points = [start_points[6], start_points[7], 
                                start_points[0], start_points[1], 
                                center.x, center.y];
    var triangle3_end_points = [end_points[6], end_points[7], 
                                end_points[0], end_points[1], 
                                center.x, center.y];
    var triangle3 = paper.polygon(triangle3_start_points);
    triangle3.attr({
        fill: colors[0]
    });

    function animationIn() {
        triangle0.stop().animate({"points":triangle0_start_points}, 1000, mina.elastic, animationOut);
        triangle1.stop().animate({"points":triangle1_start_points}, 1000, mina.elastic, animationOut);
        triangle2.stop().animate({"points":triangle2_start_points}, 1000, mina.elastic, animationOut);
        triangle3.stop().animate({"points":triangle3_start_points}, 1000, mina.elastic, animationOut);
    }
    function animationOut() {
        triangle0.stop().animate({"points":triangle0_end_points}, 1000, mina.linear, animationIn);
        triangle1.stop().animate({"points":triangle1_end_points}, 1000, mina.linear, animationIn);
        triangle2.stop().animate({"points":triangle2_end_points}, 1000, mina.linear, animationIn);
        triangle3.stop().animate({"points":triangle3_end_points}, 1000, mina.linear, animationIn);
    }

    animationIn();
}
