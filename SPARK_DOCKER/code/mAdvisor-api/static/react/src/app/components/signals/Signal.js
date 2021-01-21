import React from "react";
import {connect} from "react-redux";
import {Redirect} from "react-router";
import {getSignalAnalysis} from "../../actions/signalActions";
import {MasterSummary} from "./MasterSummary";
import {isEmpty,getUserDetailsOrRestart} from "../../helpers/helper";
import {STATIC_URL} from "../../helpers/env.js";
import {notify} from 'react-notify-toast';

@connect((store) => {
  return {
          signal: store.signals.signalAnalysis,
      };
})

export class Signal extends React.Component {
  constructor() {
    super();
  }
  componentWillMount() {
  if(isEmpty(this.props.signal)){
	  this.props.dispatch(getSignalAnalysis(getUserDetailsOrRestart.get().userToken, this.props.match.params.slug));
	  }
  }
  render() {
    if(isEmpty(this.props.signal)){
     return(
        <div className="side-body">
            <img id = "loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
        </div>
      );
    }else if(!$.isPlainObject(this.props.signal)){
      let myColor = { background: '#00998c', text: "#FFFFFF" };
      notify.show("You are not authorized to view the signal.", "custom", 2000,myColor);
              return (<Redirect to="/signals"/>);
    }
    else
    return (<MasterSummary signalId={this.props.match.params.slug} />);

}
}
