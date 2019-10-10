import React, { Component } from 'react';
import { Row, Col, Card, Alert} from 'react-bootstrap';
//import Livefeed from './Livefeed';
//import Cloudmotion from './Cloudmotion';

class Home extends Component {  
    render(){
        return (
          <Row noGutters='true'>
          <Col sm={4} style={{backgroundColor:"ghostwhite", width:"100%", height:"auto"}}>
            <Card border="light" style={{backgroundColor:"ghostwhite", display:"flex", color:"slategray"}}>
              <Card.Header>Real-time Data</Card.Header>
              <Card.Body>
                <Card.Text>LIVESTREAM</Card.Text>
                <Card.Img src="https://raw.githubusercontent.com/ucfcs/spring2019-group23/master/test_images/event20190929151615001.jpg" rounded="true" />
                <Card.Text style={{color:"slategray"}}>Location: Stanton; Orlando, FL</Card.Text>
              </Card.Body>
            </Card>
            <hr />
            <Card border='light' style={{backgroundColor: 'ghostwhite', display: 'flex'}}>
              <Card.Body style={{color:"slategray"}}>
                <Card.Text>CURRENT CONDITIONS</Card.Text>
                <Card.Text>Cloud Coverage</Card.Text>
                <Card.Text>Temperature</Card.Text>
                <Card.Text>Dewpoint</Card.Text>
                <Card.Text>Cloud base height(CBH)</Card.Text>
              </Card.Body>
            </Card>
          </Col>
          <Col sm={8}>
            <Card border="light">
              <Card.Body>
                <Card.Text style={{color:"slategray"}}>CLOUD MOTION MONITORING</Card.Text>
                <Alert variant="danger">An alert that appears when clouds are approaching the sun.</Alert>
                <Card.Img src="https://raw.githubusercontent.com/ucfcs/spring2019-group23/master/opticalFlow/sample%20output/opticalhsv(Clouds1-out).png" 
                    rounded="true" style={{display:"flex", height:"250px", width:"500px"}} />
                <div style={{whiteSpace:"pre-wrap"}}>{`
                `}</div>
                <Card.Text style={{color:"slategray"}}>POWER OUTPUT (Sample graph)</Card.Text>
                <Card.Img src="https://firstgreenconsulting.files.wordpress.com/2013/05/conductor.jpg"
                    style={{display:"flex", height:"200px", width:"500px"}} />
              </Card.Body>
            </Card>
          </Col>
          </Row>
            
        ); 
    }
}

export default Home;