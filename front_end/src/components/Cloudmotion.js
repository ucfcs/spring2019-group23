import React, { Component } from 'react';
// import { Alert } from 'react-bootstrap';
import { Bar } from 'react-chartjs-2';
import { subscribeToPredictions } from '../api'

class Cloudmotion extends Component{
    constructor(props) {
        super(props);

        subscribeToPredictions((err, data) => {
            var labels = [], values = []
            for (const [key, value] of Object.entries(data)) {
                labels.push(key)
                values.push(value)
            }

            const oldDataSet = this.state.data.datasets[0];
            const newDataSet = { ...oldDataSet };
            newDataSet.data = values
      
            const newChartData = {
              ...this.state.data,
              datasets: [newDataSet],
              labels: labels
            };
            
            this.setState({ data: newChartData });
        });

        this.state = {
            data: {
                labels: [],
                datasets: [{
                        label: 'Cloud Motion',
                        backgroundColor: 'rgba(255,99,132,0.2)',
                        borderColor: 'rgba(255,99,132,1)',
                        borderWidth: 1,
                        barPercentage: 1.25,
                        hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                        hoverBorderColor: 'rgba(255,99,132,1)',
                        data: []
                }]
            }
        };
        
        this.options = {
            maintainAspectRatio: false,
            responsive: true,
            legend: {
                display: false
            },
            title: {
                display: true,
                text: 'Cloud Motion Prediction'
            },
            scales: {
                xAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: 'Time until Sun Occlusion'
                            },
                        ticks: {
                            beginAtZero:true,
                            userCallback: function(item) {
                                return item + " min"
                            }
                        }
                    }
                ],
                yAxes: [
                    {
                        scaleLabel: {
                            display: true,
                            labelString: '# of Cloud Segments'
                          },
                        ticks: {
                            beginAtZero:true
                        }
                    }
                ]
            }
        }
    }

    render(){
        return(
            <div>
            {/* <Alert variant="info">An alert that appears when clouds are approaching the sun.</Alert> */}
            <div>
                <Bar
                    width={ 150 }
                    height={ 200 }
                    data={this.state.data}
                    options ={this.options}
                />
            </div>
            </div>
        );
    }
}

export default Cloudmotion;