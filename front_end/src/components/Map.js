import React, { Component } from 'react';
import L from 'leaflet';

class Map extends Component {
  componentDidMount(){
    this.map = L.map('map', {
      center: [28.4294, -81.309],
      zoom: 14,
      layers: [
        L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
      })]
    });
  }
  render (){
    return (
      <div id="map" style={{display:"flex", height:"400px"}}></div>
    );
  }
}

export default Map;

