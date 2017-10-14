import React, { Component } from 'react';
var Snap = require('snapsvg');

export default class Polygon extends Component {
    constructor(props) {
        super(props);
        this.state = {
            mention_percentage: props.data.getAttribute('mention_percentage'),
            retweet_percentage: props.data.getAttribute('retweet_percentage'),
            link_percentage: props.data.getAttribute('link_percentage'),
            hash_percentage: props.data.getAttribute('hash_percentage'),
            verbosity: 0
        };
    }
    setTriangles() {
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

        var a = {x: -this.state.mention_percentage*percentage_multiplier, 
                    y: this.state.mention_percentage*percentage_multiplier};
        var b = {x: this.state.retweet_percentage*percentage_multiplier, 
                    y: this.state.retweet_percentage*percentage_multiplier};
        var c = {x: this.state.link_percentage*percentage_multiplier, 
                    y: -this.state.link_percentage*percentage_multiplier};
        var d = {x: -this.state.hash_percentage*percentage_multiplier, 
                    y: -this.state.hash_percentage*percentage_multiplier};

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
        this.state.triangle0_start_points = [start_points[0], start_points[1], 
                                    start_points[2], start_points[3], 
                                    center.x, center.y];
        this.state.triangle0_end_points = [end_points[0], end_points[1], 
                                    end_points[2], end_points[3], 
                                    center.x, center.y];
        this.state.triangle0 = paper.polygon(this.state.triangle0_start_points);
        this.state.triangle0.attr({
            fill: colors[0]
        });
        this.state.triangle1_start_points = [start_points[2], start_points[3], 
                                    start_points[4], start_points[5], 
                                    center.x, center.y];
        this.state.triangle1_end_points = [end_points[2], end_points[3], 
                                    end_points[4], end_points[5], 
                                    center.x, center.y];
        this.state.triangle1 = paper.polygon(this.state.triangle1_start_points);
        this.state.triangle1.attr({
            fill: colors[1]
        });
        this.state.triangle2_start_points = [start_points[4], start_points[5], 
                                    start_points[6], start_points[7], 
                                    center.x, center.y];
        this.state.triangle2_end_points = [end_points[4], end_points[5], 
                                    end_points[6], end_points[7], 
                                    center.x, center.y];
        this.state.triangle2 = paper.polygon(this.state.triangle2_start_points);
        this.state.triangle2.attr({
            fill: colors[0]
        });
        this.state.triangle3_start_points = [start_points[6], start_points[7], 
                                    start_points[0], start_points[1], 
                                    center.x, center.y];
        this.state.triangle3_end_points = [end_points[6], end_points[7], 
                                    end_points[0], end_points[1], 
                                    center.x, center.y];
        this.state.triangle3 = paper.polygon(this.state.triangle3_start_points);
        this.state.triangle3.attr({
            fill: colors[0]
        });
    }
    grow () {
        this.state.triangle0.animate({"points":this.state.triangle0_end_points}, 1000, mina.linear);
        this.state.triangle1.animate({"points":this.state.triangle1_end_points}, 1000, mina.linear);
        this.state.triangle2.animate({"points":this.state.triangle2_end_points}, 1000, mina.linear);
        this.state.triangle3.animate({"points":this.state.triangle3_end_points}, 1000, mina.linear);
    }
    componentDidMount() {
    }

    render() {
        return (
            <div>
                {this.setTriangles()}
                {this.grow()}
            </div>
        )
    }
}
