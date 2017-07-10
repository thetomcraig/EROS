var React = require('react')

var Cog = React.createClass({displayName: "Cog",

  getDefaultProps: function() {
    return {
      size: 10,
      points: {
                a: {x: 0, y: 0},
                b: {x: 0, y: 0},
                c: {x: 0, y: 0},
                d: {x: 0, y: 0},
      },
      fill: 'currentcolor'
    }
  },

  render: function() {

    var size = this.props.size
    var fill = this.props.fill
    var points = this.props.points
    var a = points.a
    var b = points.b
    var c = points.c
    var d = points.d

    var viewBox = [0, 0, size, size].join(' ')

    var pathData = [
            'M', a.x+size, Math.abs(a.y - size),
            'L', b.x+size, Math.abs(b.y - size),
            'L', c.x+size, Math.abs(c.y - size),
            'L', d.x+size, Math.abs(d.y - size),
            'L', a.x+size, Math.abs(a.y - size),
        ].join(' ')

    return (
        React.createElement("svg", {xmlns: "http://www.w3.org/svg/2000", 
        viewBox: viewBox, 
        width: size, 
        height: size, 
        fill: fill}, 
        React.createElement("path", {d: pathData})
        )
      )
  }
});

module.exports = Cog
