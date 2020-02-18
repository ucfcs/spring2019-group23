import React, { Component } from 'react';
import { Row, Col, Card } from 'react-bootstrap';
import Cloudmotion from './Cloudmotion';
import JsmpegPlayer from './JsmpegPlayer';
import Map from './Map';
import { subscribeToData, subscribeToCoverageData } from '../api';
import Moment from 'react-moment';

const videoOptions = {
  poster: 'https://i.imgur.com/FJtImIA.png'
};

const videoOverlayOptions = {};

class Home extends Component {
      constructor(props) {
      super(props);
    
      subscribeToData((err, data) => {
        this.setState(data);
        this.setState({ time: new Date() })
      });

      subscribeToCoverageData((err, data) => {
        this.setState(data);
      });
      
      this.state = {
        cloud_coverage: '',
        temperature: '',
        dew_point: '',
        barometric_pressure: '',
        cloud_base_height: '',
        time: ''
      }
    }

    componentDidMount() {
      fetch('/coverage')
      .then( res => res.json() )
      .then( (data) => {
        this.setState(data)
      }).catch(console.log)
      
      fetch('/weather')
      .then( res => res.json() )
      .then( (data) => {
        this.setState(data)
      }).catch(console.log)
    }

    render(){
        return (
          <Row noGutters='true'>
          <Col sm={4} style={{backgroundColor:"ghostwhite", width:"100%", height:"auto"}}>
            <Card border="light" style={{backgroundColor:"ghostwhite", display:"flex", color:"slategray"}}>
              <Card.Header>Real-time Data</Card.Header>
              <Card.Body>
                <Card.Text>LIVESTREAM</Card.Text>
                <div>
                <JsmpegPlayer
                    wrapperClassName="video-wrapper"
                    videoUrl="ws://cloudtrackingcloudserver.herokuapp.com/stream"
                    // videoUrl="ws://localhost:3001/stream"
                    options={videoOptions}
                    overlayOptions={videoOverlayOptions}
                />
                </div>
                <Card.Text style={{color:"slategray"}}>Location: Engineering II, UCF; Orlando, FL</Card.Text>
              </Card.Body>
            </Card>
            <hr />
            <Card border='light' style={{backgroundColor: 'ghostwhite', display: 'flex'}}>
            <Card.Body style={{ color: "slategray" }}>
              <Card.Text>CURRENT CONDITIONS</Card.Text>
              <Card.Text>Cloud Coverage: {this.state.cloud_coverage}%</Card.Text>
              <Card.Text>Temperature: {this.state.temperature} °F</Card.Text>
              <Card.Text>Dewpoint: {this.state.dew_point} °F</Card.Text>
              <Card.Text>Barometric Pressure: {this.state.barometric_pressure} mb</Card.Text>
              <Card.Text>Cloud Base Height (CBH): {this.state.cloud_base_height} ft</Card.Text>
              <Card.Text style={{ fontStyle: "italic", fontSize: "14px" }}>Last updated:  
                <Moment format="LLL">{this.state.time}</Moment>
              </Card.Text>
            </Card.Body>
            </Card>
          </Col>
          <Col sm={8}>
            <Card border="light">
              <Card.Body>
                
                <Card.Text style={{color:"slategray"}}>CLOUD MONITORING</Card.Text>
                
                <React.Fragment>
                  <Cloudmotion />
                </React.Fragment>

                <React.Fragment>
                  <Map />
                </React.Fragment>
                <div style={{whiteSpace:"pre-wrap"}}>{``}</div>
              </Card.Body>
            </Card>
          </Col>
          </Row>
            
        ); 
    }
}

export default Home;
