import React from 'react';
import ScrapeButton from './ScrapeButton';

exports.shapes = require('./shapes/polygon.js');

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
    <div>
        <MuiThemeProvider>
            <ScrapeButton />
        </MuiThemeProvider>
     </div>
    );
  }
}

