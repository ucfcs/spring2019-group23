import React, { Component } from 'react';
import { CsvToHtmlTable } from 'react-csv-to-table';
import { DateRangePicker } from 'react-dates';
import { CSVLink } from "react-csv";
import { Container, Form, Row, Col, ToggleButton, ToggleButtonGroup, ButtonToolbar} from 'react-bootstrap';

class Archive extends Component {
    constructor(props) {
    super(props);
    this.state = {
      startDate: null,
      endDate: null,
      focusedInput: null,
      data: '',
      report: 1,
    };
  }

  fetchData = () => {
    const encodedFromDate = encodeURIComponent(new Date(this.state.startDate));
    const encodedToDate = encodeURIComponent(new Date(this.state.endDate));
    var url = ''

    switch(this.state.report) {
      default:
      case 1:
        url = `/weather/range?from_date=${encodedFromDate}&to_date=${encodedToDate}`
        break;
      case 2:
        url = `/coverage/range?from_date=${encodedFromDate}&to_date=${encodedToDate}`
        break;
      case 3:
        url = `/motion/range?from_date=${encodedFromDate}&to_date=${encodedToDate}`
        break;
    }
    fetch(url)
    .then(response => response.text())
    .then(data => this.setState({ data }) );
  }
  
  render(){
        return(
          <Container>
            <h2>Archive</h2>
            <p className="text-muted">Select a date range and type to generate a report:</p>
            
            <Row>
              <Col>
              <Form>
                <Form.Group>
                  <ButtonToolbar>
                    <ToggleButtonGroup type="radio" name="option" defaultValue={this.state.report} onChange={report => this.setState({ report })}>
                      <ToggleButton value={1}>Weather Data</ToggleButton>
                      <ToggleButton value={2}>Cloud Coverage</ToggleButton>
                      <ToggleButton value={3}>Cloud Motion</ToggleButton>
                    </ToggleButtonGroup>
                  </ButtonToolbar>
                </Form.Group>
              <Form.Group>
                <DateRangePicker
                  startDateId="startDate"
                  endDateId="endDate"
                  startDate={this.state.startDate}
                  endDate={this.state.endDate}
                  onDatesChange={({ startDate, endDate }) => { this.setState({ startDate, endDate })}}
                  focusedInput={this.state.focusedInput}
                  onFocusChange={(focusedInput) => { this.setState({ focusedInput })}}
                  isOutsideRange= {() => false}
                />
              </Form.Group>
              </Form>
            </Col>
          </Row>

          <div style={{float: "right", margin: "auto"}}>
            <button 
              onClick={this.fetchData}
              style={{margin: 10}}
              disabled={!this.state.startDate || !this.state.endDate}
              className="btn btn-primary">
                Generate
            </button>
            {
              this.state.data === '' ? null :
              <CSVLink
                data={this.state.data}
                filename={"data.csv"}
                className="btn btn-primary"
                style={{margin: 10}}
                target="_blank">
                Download CSV
              </CSVLink>
            }
          </div>
        <Row className="container-fluid row">
        {
          this.state.data === '' ? 
          <small>
            No data to display
          </small> :
            <CsvToHtmlTable
              data={this.state.data}
              csvDelimiter=","
              tableClassName="table table-striped table-hover table-responsive table-body"
            />
          }
        </Row>
        </Container>
        );
  }
}

export default Archive;