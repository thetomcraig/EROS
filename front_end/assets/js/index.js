var React = require('react')
var ReactDOM = require('react-dom')
var Snap = require('snapsvg')
var s = Snap(800, 800);

var size = 100;
var points = {
    mention_percentage: 10,
    retweet_percentage: 50,
    link_percentage: 100,
    hash_percentage: 90,
    verbosity: 0,
}
//convert to cartesian
var percentage_multiplier = 50*Math.sqrt(2)/100
var a = {x: -points.mention_percentage*percentage_multiplier, 
            y: points.mention_percentage*percentage_multiplier};
var b = {x: points.retweet_percentage*percentage_multiplier, 
            y: points.retweet_percentage*percentage_multiplier};
var c = {x: points.link_percentage*percentage_multiplier, 
            y: -points.link_percentage*percentage_multiplier};
var d = {x: -points.hash_percentage*percentage_multiplier, 
            y: -points.hash_percentage*percentage_multiplier};


var paper = Snap('svg');
var start_points = [a.x+100, (100 - a.y),
                    b.x+100, (100 - b.y),
                    c.x+100, (100 - c.y),
                    d.x+100, (100 - d.y),
                   ];
var end_points  = [0, 0,
                   100, 0,
                   100, 100,
                   0, 100,
                  ];
var polygon = paper.polygon(start_points);
polygon.attr({
    id:"tri",
    fill:"#555555"
});


var animating = true;
function animationIn() {
    if (animating) {
        polygon.animate({"points":start_points}, 1000, mina.linear, animationOut);
    };
}
function animationOut() {
    polygon.animate({"points":end_points}, 1000, mina.linear, animationIn);
}


polygon.hover(function() {animating=true; animationIn() }, function() { animating=false });




var Hello = React.createClass ({
    render: function() {
        return (
            <h1>
            </h1>
        )
    }
})

ReactDOM.render(<Hello />, document.getElementById('container'));
