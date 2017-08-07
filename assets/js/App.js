import React from 'react';
import ScrapeButton from './ScrapeButton';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import Polygon from './shapes/Polygon';


export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
    <div>
        <MuiThemeProvider>
            <Polygon data={document.getElementById('user-data')}/>
        </MuiThemeProvider>
     </div>
    );
  }
}
