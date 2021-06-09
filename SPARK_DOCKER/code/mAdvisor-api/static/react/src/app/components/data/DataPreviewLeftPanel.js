import React from "react";
import {connect} from "react-redux";
import {STATIC_URL} from "../../helpers/env.js";
import { Scrollbars } from 'react-custom-scrollbars';
import {getScoreSummaryInCSV,getAppDetails,fetchScoreSummaryCSVSuccess} from "../../actions/appActions";
import {Link} from "react-router-dom";
import {Button} from "react-bootstrap";

@connect((store) => {
	return {
        scoreCSVData: store.apps.scoreSummaryCSVData,
	};
})

export class DataPreviewLeftPanel extends React.Component {
	constructor(props) {
		super(props);
    }
    componentWillUnmount(){
        this.props.dispatch(fetchScoreSummaryCSVSuccess([]))
    }
     
    componentWillMount(){
       this.props.dispatch(getAppDetails(this.props.match.params.AppId));
       this.props.dispatch(getScoreSummaryInCSV(this.props.match.params.slug))
    }

    render() {
        var scoreLink = this.props.match.url.slice(0, this.props.match.url.lastIndexOf('/'));
        const scoreData = this.props.scoreCSVData;
		var tableThTemplate = "";
		var tableRowTemplate = "";
		if(scoreData.length > 0){
		    tableThTemplate = scoreData.map(function(row,id){
                let colData = "";
                if(id == 0){
                   colData =  row.map((colData,index) =>{
                       let colIndex = "row_"+id+index
                        return(<th key={colIndex}><b>{colData}</b></th>)
                    })
                }
                return colData!=""?colData:null;
            });
		    tableRowTemplate = scoreData.map(function(row,id){
		        if(row != ""){
                    let colData = "";
                    let colIndex = "row_"+id
                    if(id > 0){
                        colData =  row.map((colData,index) =>{
                            if(row.length-1==index || row.length-2==index)
                                return(<td  key={index} class="activeColumn">{colData}</td>)
                            else
                                return(<td key={index} >{colData}</td>)
                        })
                    }
                    return <tr key = {colIndex}>{colData}</tr>;
                }
            });
		    return(
		        <div className="side-body">
                    <div className="page-head">
		    			<div className="row">
			        		<div className="col-md-8">
				            	<h3 className="xs-mt-0 text-capitalize">Score Data Preview</h3>
					        </div>
					    </div>
					</div>
                    <div className="main-content">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="panel no-borders box-shadow xs-p-10">
                                    <div className="clearfix"></div>
                                    <div className="table-responsive scoreDataPreview">
                                        <Scrollbars>
                                            <table className="table table-condensed table-hover table-bordered table-striped cst_table">
                                                <thead>
                                                    <tr>
                                                        {tableThTemplate}
                                                    </tr>
                                                </thead>
                                                <tbody className="no-border-x">
                                                    {tableRowTemplate}
                                                </tbody>
                                            </table>
                                        </Scrollbars>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-md-12">
                                <div className="panel">
                                    <div className="panel-body no-border text-right box-shadow">
                                        <Link to={scoreLink} ><Button> Close</Button></Link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
		}else{
		    return ( 
                <div className="side-body">
                    <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
                </div>
            );
		}
    }
}
