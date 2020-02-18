import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import NavBar from './components/NavBar.js';
import Home from './components/Home'
import Archive from './components/Archive'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-dates/lib/css/_datepicker.css';
import 'react-dates/initialize';
//import Layout from './components/Layout.js';

class App extends Component {
  render(){
    return (
      <React.Fragment>
        <BrowserRouter>
          <NavBar />
          {/*<Layout>*/}
            <Switch>
              <Route exact path='/' component={Home} />
              <Route path='/archive' component={Archive} />
            </Switch>
          {/*</Layout>*/}
        </BrowserRouter>
      </React.Fragment>
    );
  }
}

export default App;
