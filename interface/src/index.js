import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
//import ScrollArea from 'react-scrollbar';
//import Helmet from 'react-helmet';

const Title = _ =>
  <header>
    Webpage Analyzer
  </header>


class SearchBox extends React.Component {
  constructor(props) {
    super(props);
    this.state= {
      value: ''
    };
    this.handleChange=this.handleChange.bind(this);
    this.handleSubmit=this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  //INTENTION for handleSubmit: The term will be processed and we will receive
  //a ranked list of URLs (ranked by frequency of that term in the URL)
  //along with the frequency for each of those URLs. We will display this
  //ranked list, with each URL in the form of a hyperlink, and with
  //the frequencies listed beside each URL.
  handleSubmit(event) {
    alert('A search term was submitted: ' + this.state.value);
    event.preventDefault();
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <br/>
        <label>
          Search Term:
          <input type="text" value={this.state.value}
            onChange={this.handleChange} />
        </label>
        <input type="submit" value= "Submit" />
        <br/>
        <br/>
      </form>
    );
  }
}

class Results extends React.Component {
  constructor() {
      super();
      this.state = {
      //this is currently fake data,
      //in reality we will do ajax call to fetch data
        data: [{
          id: 1,
          name: "Simon Bailey",
          frequency: "123"
        }, {
          id: 2,
          name: "Thomas Burleson",
          frequency: "123"
        }, {
          id: 3,
          name: "Will Button",
          frequency: "123"
        }]
      }
    }
    render() {
      let rows = this.state.data.map(row => {
        return <Row key = {
          row.id
        }
        data = {
          row
        }
        />
      })
      return <table >
        < thead> {
        <tr>
          <td>Rank </td>
          <td>Webpage</td>
          <td>Count</td>
        </tr>
        } </thead>
        < tbody > {
          rows
        } < /tbody> < /table>
    }
  }

  const Row = (props) => {
    return (
      <tr>
        <td>
          { props.data.id }
        </td>
        <td>
          { props.data.name }
        </td>
        <td>
         { props.data.frequency }
        </td>
      </tr>
    );
  }




class Main extends React.Component {
  render() {
    return (
      <div className="display">
        <div className="title">
          <Title/>
        </div>
        <div className="search-box">
          <SearchBox />
        </div>
        <div className="results-list">
          <Results/>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <Main />,
  document.getElementById('root')
);
