import React, { Component } from 'react';
import { Row, Col, Card, Alert} from 'react-bootstrap';
import JsmpegPlayer from './JsmpegPlayer';
import Map from './Map';
import { subscribeToData, subscribeToCoverage, subscribeToFlow } from '../api';
//import Livefeed from './Livefeed';
//import Cloudmotion from './Cloudmotion';

const videoOptions = {
  poster: 'https://i.imgur.com/FJtImIA.png'
};

const videoOverlayOptions = {};

class Home extends Component {
      constructor(props) {
      super(props);
      subscribeToCoverage((err, coverage_img) => {
        this.setState({ coverage_img })
      });
  
      subscribeToFlow((err, flow_img) => {
        this.setState({ flow_img })
      })
    
      subscribeToData((err, data) => {
        /// TODO: If no data was sent for some points will this be duplicated?
        this.setState(data);
      });
    }

    state = {
      coverage_img: videoOptions.poster,
      flow_img: videoOptions.poster
    };
  
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
                    options={videoOptions}
                    overlayOptions={videoOverlayOptions}
                />
                </div>
                <Card.Text style={{color:"slategray"}}>Location: Stanton; Orlando, FL</Card.Text>
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
              <Card.Text>Cloud base height (CBH): {this.state.cloud_base_height} ft</Card.Text>
            </Card.Body>
            </Card>
          </Col>
          <Col sm={8}>
            <Card border="light">
              <Card.Body>
                <Card.Text style={{color:"slategray"}}>CLOUD MOTION MONITORING</Card.Text>
                <Alert variant="danger">An alert that appears when clouds are approaching the sun.</Alert>
                <React.Fragment>
                  <Map />
                </React.Fragment>
                <div style={{whiteSpace:"pre-wrap"}}>{`
                `}</div>
                <Card.Text style={{color:"slategray"}}>POWER OUTPUT (Sample graph)</Card.Text>
                <Card.Img src={this.state.coverage_img}
                    style={{display:"flex"}} />
                <Card.Img src={this.state.flow_img}
                  style={{display:"flex"}} />
              </Card.Body>
            </Card>
          </Col>
          </Row>
            
        ); 
    }
}

export default Home;
