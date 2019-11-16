import React, { Component } from 'react';
import L from 'leaflet';
import { subscribeToCoverage, subscribeToFlow, subscribeToData } from '../api';
import { getCloudHeight } from './cloud-height.js'
var SunCalc = require('suncalc');
// Calib is an array of the dimensions of whatever was used to calibrate the camera.
// In our case, we used a square sheet of paper that's 210mmx210mm and was held at
// 75mm away from the lens
const CALIB  = [0.6883333, 0.6883333, 1/6];

// lat/long coordinates of the center of the image. i.e. wherever the camera is placed
const CENTER = [28.4294, -81.309];

class Map extends Component {
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
    })
  }
 

  state = {
    coverage_img: 'leaflet_cloud_image.png',
    flow_img: '',
    cloud_base_height: 2500
  };

  componentDidMount() {
    this.map = L.map('map', {
      center: CENTER,
      zoom: 14,
      layers: [
        L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
      })]
    });

    // Returns a {azimuth, altitude} object. We're only interested in altitude
    // sun altitude above the horizon in radians, e.g. 0 at the horizon and PI/2 at the zenith (straight over your head)
    var sun = SunCalc.getPosition(new Date(), CENTER[0], CENTER[1]);

    // ===================================================================================
    // To avoid inflating this code with comments, check the final project design document
    // for a more detailed description that explains the logic behind this.
    var cloudHeight = this.state.cloud_base_height;
    var calibrationAngle = Math.atan(CALIB[0] / CALIB[1]);

    var smallHypo  = Math.sqrt(Math.pow(CALIB[0]/2, 2) + Math.pow(CALIB[1]/2, 2));
    var largeHypo  = smallHypo * cloudHeight / CALIB[2];
    var NSdistance = Math.sin(calibrationAngle) * largeHypo;
    var EWdistance = Math.cos(calibrationAngle) * largeHypo;

    console.log(upperLeftCorner);
    var upperLeftCorner = this.addDistanceToCoordinate(CENTER, -NSdistance, EWdistance, sun.altitude, cloudHeight);
    console.log(upperLeftCorner);

    var bottomRightCorner = this.addDistanceToCoordinate(CENTER, NSdistance, -EWdistance, sun.altitude, cloudHeight);
    // ===================================================================================

    // To be passed to Leaflet to be displayed onto the map
    var imageBounds = [upperLeftCorner, bottomRightCorner];

    // TODO: Create second overlay and swap them as new data arrives
    // see also: https://plnkr.co/edit/nIdNwTpDjZNhyiCzGJPC?p=info
    var overlay = L.imageOverlay(this.state.coverage_img, imageBounds);
    overlay.addTo(this.map);
  };

  render (){
    return (
      <div id="map" style={{display:"flex", height:"400px"}}></div>
    );
  };

  // Input: Starting lat/long coordinate, North/South distance travlled, East/West distance.
  // Return: Final latitude value after travelling the input distance
  // Forumals: https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
  addDistanceToCoordinate(startCoordinate, x_distance, y_distance, sun_altitude, cbh) {
    var finalCoordinate = [1e9, 1e9];
    finalCoordinate[0] = startCoordinate[0] + (y_distance / 362775.6);
    finalCoordinate[1] = startCoordinate[1] + ((x_distance + Math.tan(sun_altitude) * cbh) /
                         365223.1) * Math.cos(startCoordinate[0] * Math.PI / 180);
    return finalCoordinate;
  }
}

export default Map;