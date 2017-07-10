var fs = require('fs')
var React = require('react')
var Cog = require('./Cog')
var ReactDOMServer = require('react-dom/server')


var build = function(name, props) {

  props.size = props.size || 64
  var size = props.size
  var viewBox = [0, 0, size, size].join(' ')
  var svg = [
    '<svg xmlns="http://www.w3.org/2000/svg" ',
      'viewBox="', viewBox, '" ',
      'width="', size, '" ',
      'height="', size, '" ',
        '>',
    ReactDOMServer.renderToStaticMarkup(React.createElement(Cog, props)),
    '</svg>'
  ].join('')
  
  fs.writeFileSync('icons/' + name + '.svg', svg)

}
build('cog-icon', {'teeth': 5})
