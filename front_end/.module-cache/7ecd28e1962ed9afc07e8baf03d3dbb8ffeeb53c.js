var React = require('react')

var Cog = React.createClass({displayName: "Cog",

  getDefaultProps: function() {
    return {
      size: 200,
      data_points: {
            mention_percentage: 0,
            retweet_percentage: 0,
            link_percentage: 0,
            hash_percentage: 0,
            verbosity: 0,
      },
      fill: 'currentcolor'
    }
  },

  render: function() {

    var size = this.props.size
    var fill = this.props.fill
    var points = this.props.data_points
    //convert to cartesian
    var percentage_multiplier = 50*Math.sqrt(2)/100
    var a = {x: -points.mention_percentage*percentage_multiplier, 
             y: points.mention_percentage*percentage_multiplier}
    var b = {x: points.retweet_percentage*percentage_multiplier, 
             y: points.retweet_percentage*percentage_multiplier}
    var c = {x: points.link_percentage*percentage_multiplier, 
             y: -points.link_percentage*percentage_multiplier}
    var d = {x: -points.hash_percentage*percentage_multiplier, 
             y: -points.hash_percentage*percentage_multiplier}

    var viewBox = [0, 0, size, size].join(' ')

    var pathData = [
            'M', 0, 0,
            'L', 50, 0,
            'L', 50, 50,
            'L', 0, 50,
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
