import React from "react";
import D3WordCloud from 'react-d3-cloud';

export class WordCloud extends React.Component {

  render() {
	let data =  this.props.jsonData;
	  const fontSizeMapper = word => word.value * 15;
	  const rotate = word => [0,0,0,90][word.value % 4];
   return (
          <div className= {window.location.href.includes("apps-stock-document-mode")?"text-center":"text-center wordCloud"}>
          <h3>Top Entities</h3>
          <D3WordCloud
          data={data}
          fontSizeMapper={fontSizeMapper}
          rotate={rotate}
          width="900"
          font="Roboto Condensed"
          height="300"
          />
        	</div>
       );
  }
}
