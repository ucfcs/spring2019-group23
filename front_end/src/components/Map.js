import React, { Component } from 'react';
import L from 'leaflet';
import { subscribeToCoverage, subscribeToFlow } from '../api';

// Field of Vision for a specific camera (degrees). Using iPhone 7.
const FOV = 58;
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
  }

  state = {
    coverage_img: 'leaflet_cloud_image.png',
    flow_img: ''
  }

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

    // Creating Image overlay
    var imageBounds = [[28.3, -81.2], [28.4, -81.4]];

    /// TODO: Create second overlay and swap them as new data arrives
    ///// seealso: https://plnkr.co/edit/nIdNwTpDjZNhyiCzGJPC?p=info
    var overlay = L.imageOverlay(this.state.coverage_img, imageBounds);
    overlay.addTo(this.map);       
  }
  render (){
    return (
      <div id="map" style={{display:"flex", height:"400px"}}></div>
    );
  }
}

export default Map;

