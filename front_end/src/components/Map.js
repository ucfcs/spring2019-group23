import React, { Component } from 'react';
import L from 'leaflet';

// Field of Vision for a specific camera (degrees). Using iPhone 7.
const FOV = 58;
const CENTER = [28.4294, -81.309];

class Map extends Component {
  componentDidMount(){
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
    
    var imagePath = 'leaflet_cloud_image.png'; 
    var imageBounds = [[28.3, -81.2], [28.4, -81.4]];
    var overlay = L.imageOverlay(imagePath, imageBounds);
    overlay.addTo(this.map);       
  }
  render (){
    return (
      <div id="map" style={{display:"flex", height:"400px"}}></div>
    );
  }
}

export default Map;

