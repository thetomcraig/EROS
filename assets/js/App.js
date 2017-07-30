import React from 'react';
import ScrapeButton from './ScrapeButton';

import {showPolygon} from './shapes/polygon.js'

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    showPolygon(.5);
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
