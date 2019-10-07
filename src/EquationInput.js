import React from 'react';
import { calculateG } from "./Equation";

class EquationInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    alert('G(1.0) =  ' + this.state.value + " " + this.calcG());
    event.preventDefault();
  }

  calcG(){
    return calculateG();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <input type="submit" value="Sample Calculation 1" />
      </form>
    );
  }
  }

  export default EquationInput;