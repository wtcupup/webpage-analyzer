import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import ScrollArea from 'react-scrollbar';
//var ScrollArea=require('react-scrollbar');


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
        <label>
          Search Term:
          <input type="text" value={this.state.value}
            onChange={this.handleChange} />
        </label>
        <input type="submit" value= "Submit" />
      </form>
    );
  }
}

function Results(props) {
  const listOfPages= (
    <ol>
      {props.pages.map((page) =>
        <li key={page.id}>
          {page.title}
          {' Count: '+page.frequency}
        </li>
      )}
    </ol>
  );
  return (
  <ScrollArea
    speed={0.8}
    vertical={true}
    horizontal={true}>
  <div>
    {listOfPages}
  </div>
  </ScrollArea>
  );
}


class Main extends React.Component {

  render() {
    const pages =[ //pages will be determined in some other way. We will receive
      //a ranked list of URLs (ranked by frequency of that term in the URL)
      //along with the frequency for each of those URLs.
      {id:1, title: 'title1 REALLY LONG NAME still is not scrolling ksjflkadsjfldkasjgkljdkfjkdjfaldsfkjsaflksdjfklsajfl;ksajfksdjaf;asfjas;dkfjdsl;fkjdsf;kladjfl;kasdfjdl;ksfjdl;kafjadslk;fjasdlkjfdslakfjdslkfjdslkfjasl;kfjas;kfjdsaklfjdaslkfjadlkfjdslkfjsdlkjadslkfjlakdsfjdlaksfjd;lfks', frequency: '145'},
      {id:2, title: 'title2', frequency: '246'},
      {id:3, title: 'title3', frequency: '367'},
      {id:4, title: 'title4', frequency: '426'}
    ];
    return (
      <div className="display">
        <div className="search-box">
          <SearchBox />
        </div>
        <div className="results-list">
          <Results pages= {pages}/>
        </div>
      </div>
    );
  }
}

ReactDOM.render(
  <Main />,
  document.getElementById('root')
);
