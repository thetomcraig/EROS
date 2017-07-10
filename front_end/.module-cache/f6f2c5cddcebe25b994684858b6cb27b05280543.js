var React = require('react')

var Cog = React.createClass({displayName: "Cog",

  getDefaultProps: function() {
    return {
      size: 64,
		d1: 1,
		d2: .6875,
		d3: .375,
		teeth: 8,
		splay: 0.375,
      fill: 'currentcolor'
    }
  },

  render: function() {

    var size = this.props.size
    var fill = this.props.fill
 // Center
  var c = size / 2

  // Radii
  var r1 = this.props.d1 * size / 2
  var r2 = this.props.d2 * size / 2
  var r3 = this.props.d3 * size / 2

  // Angle
  var angle = 360 / this.props.teeth
  var offset = 90

  var viewBox = [0, 0, size, size].join(' ')


    var pathData = [
      ''
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
