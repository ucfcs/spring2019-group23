import React, { Component } from 'react';

class Cloudmotion extends Component{
    render(){
        return(
            <div className="col s7">
                <div className="card horizontal grey lighten-5 z-depth-1">
                        <div className="card-image">
                            <img className="responsive-img" 
                                src="https://raw.githubusercontent.com/ucfcs/spring2019-group23/master/test_images/event20190929151615001.jpg" 
                                alt=" "></img>
                                </div>
                            <div className="card-content">
                                <div className="card grey lighten-2 z-depth-1">
                                    <div className="card-content">
                                        <span className="card-title">ALERT</span>
                                        <p>Clouds are coming.</p>
                                    </div>
                                </div>
                            </div>
                        
                    </div>
                </div>
        
        );
    }
}

export default Cloudmotion;