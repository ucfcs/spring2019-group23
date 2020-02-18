import React, { Component } from 'react';

class Livefeed extends Component {
    render (){
        return (
            <div className="col s5">
                <div className="card grey lighten-5 z-depth-1">
                    <div className="card-content">
                        <span className="card-title">Live feed</span>
                            <div className="card-image">
                                <img className="responsive-img" 
                                src="https://raw.githubusercontent.com/ucfcs/spring2019-group23/master/test_images/event20190929151615001.jpg" 
                                alt=" "></img>
                            </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Livefeed;

