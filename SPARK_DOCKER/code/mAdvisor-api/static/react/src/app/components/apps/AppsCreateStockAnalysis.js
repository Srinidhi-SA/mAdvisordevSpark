import React from "react";
import { connect } from "react-redux";
import { Modal, Button } from "react-bootstrap";
import store from "../../store";
import { updateCreateStockPopup, addDefaultStockSymbolsComp, crawlDataForAnalysis, addMoreStockSymbols, removeStockSymbolsComponents, handleInputChange } from "../../actions/appActions";
import { storeSignalMeta } from "../../actions/dataActions";
import { MultiSelect } from 'primereact/multiselect';

@connect((store) => {
	return {
		appsCreateStockModal: store.apps.appsCreateStockModal,
	};
})

export class AppsCreateStockAnalysis extends React.Component {
	constructor(props) {
		super(props);
		this.state={ 
			domain:[],
			company:[],
		}
	}
	componentWillMount() {
		this.props.dispatch(updateCreateStockPopup(false));
		this.props.dispatch(storeSignalMeta(null, this.props.match.url));
		this.props.dispatch(addDefaultStockSymbolsComp())
	}
	updateCreateStockPopup(flag) {
		this.setState({domain:[],company:[]})
		this.props.dispatch(updateCreateStockPopup(flag))
	}
	handleInputChange(event) {
		this.props.dispatch(handleInputChange(event))
	}
	removeStockSymbolsComponents(data, event) {
		this.props.dispatch(removeStockSymbolsComponents(data));
	}
	addMoreStockSymbols(event) {
		this.props.dispatch(addMoreStockSymbols(event));
	}
	companyDetails(name, ticker) {
		this.name = name;
		this.ticker = ticker;
	}

	crawlDataForAnalysis(companyList) {
		var analysisName = $("#createStockAnalysisName").val();
		var domains = this.state.domain;
		var companies=this.state.company
		var list=[];
		let letters = /^[0-9a-zA-Z\-_\s]+$/;
		document.getElementById("resetMsg").innerText=''

		if(domains.length==0||companies.length==0){
			document.getElementById("resetMsg").innerText="Please select all mandatory fields."
			return false;
		}
		if (analysisName == ""||(analysisName != "" && analysisName.trim() == "")) {
			document.getElementById("resetMsg").innerText="Please enter stock analysis name."
			return false;
		} 
		if (letters.test(analysisName) == false){
			document.getElementById("resetMsg").innerText = "Please enter analysis name in a correct format. It should not contain special characters .,@,#,$,%,!,&.";
      return false
    }     
		for(var i=0;i<companies.length;i++){
			window['value'+i] = new this.companyDetails(companyList.filter(j=>j.value==companies[i])[0].label, companies[i]);
			list.push((window['value'+i]))
		}
    $('#extractData').prop('disabled', true);
		this.props.dispatch(crawlDataForAnalysis(domains, companies,analysisName,list));
	}
	render() {
		let domainList=[
			{label:"cnbc.com",value: "cnbc.com"} ,
			{label:"ft.com",value: "ft.com"} ,
			{label:"wsj.com",value: "wsj.com"},
			{label:"marketwatch.com",value: "marketwatch.com"},
			{label:"in.reuters.com",value: "in.reuters.com"},
			{label:"investopedia.com",value: "investopedia.com"},
			{label:"nytimes.com",value: "nytimes.com"} ,
			{label:"economictimes.indiatimes.com",value: "economictimes.indiatimes.com"},
			{label:"finance.yahoo.com",value: "finance.yahoo.com"},
			{label:"forbes.com",value: "forbes.com"} ,
			{label:"financialexpress.com",value: "financialexpress.com"} ,
			{label:"bloomberg.com",value: "bloomberg.com"} ,
			{label:"nasdaq.com",value: "nasdaq.com"} ,
			{label:"fool.com",value: "fool.com"}
		]

		let companyList=
		[             
			{value:"XOM"    ,label: "Exxon Mobil"},
			{value:"GE"     ,label:	"General Electric"},
			{value:"MSFT"	  ,label:	"Microsoft"},
			{value:"WMT" 	  ,label:	"Wal-Mart"},
			{value:"TM"  	  ,label:	"Toyota Motor"},
			{value:"JNJ" 	  ,label:	"JOHNSON & JOHNSON"},
			{value:"JPM" 	  ,label:	"J.P. Morgan Chase & Co."},
			{value:"INTC"	  ,label: "Intel"},
			{value:"IBM" 	  ,label:	"International Business Machines Corporation"},
			{value:"CSCO"	  ,label: "Cisco Systems"},
			{value:"HPQ" 	  ,label:	"Hewlett-Packard"},
			{value:"GOOG"	  ,label: "Google"},
			{value:"NOK" 	  ,label:	"Nokia"},
			{value:"QCOM"	  ,label: "QUALCOMM"},
			{value:"MRK" 	  ,label:	"Merck"},
			{value:"DELL"	  ,label:	"Dell"},
			{value:"AXP"  	  ,label:	"American Express"},
			{value:"MS"  	  ,label:	"Morgan Stanley"},
			{value:"ORCL"	  ,label: "Oracle"},
			{value:"AAPL"	  ,label:	"Apple Computer"},
			{value:"BA"  	  ,label:	"Boeing"},
			{value:"MCD" 	  ,label:	"McDonald's"},
			{value:"BP"  		,label:	"BP p.l.c."},
			{value:"C"   	  ,label:	"Citigroup"},
			{value:"PG"  	  ,label:	"Procter & Gamble"},
			{value:"BAC"	  ,label:	"Bank of America"},
			{value:"AIG" 	  ,label:	"American International Group"},
			{value:"CVX" 	  ,label:	"ChevronTexaco"},
			{value:"SNY" 	  ,label:	"Sanofi-Aventis SA"},
			{value:"VOD" 	  ,label:	"Vodafone"},
			{value:"E"   	  ,label:	"ENI S.p.A."},
			{value:"KO"  	  ,label:	"Coca-Cola"},
			{value:"CHL"    ,label:	"China Mobile"},
			{value:"PEP"    ,label:	"Pepsico"},
			{value:"VZ"     ,label:	"Verizon Communications"},
			{value:"COP"    ,label:	"CONOCOPHILLIPS"},
			{value:"HD"     ,label:	"Home Depot"},
			{value:"WB"     ,label:	"Wachovia"},
			{value:"SI"     ,label:	"Siemens AG"},
			{value:"UNH"    ,label:	"UnitedHealth Group"},
			{value:"AZN"    ,label:	"ASTRAZENECA PLC"},
			{value:"MDT"    ,label:	"Medtronic"},
			{value:"ABT"    ,label:	"Abbott Laboratories"},
			{value:"DT"   	,label:	"Deutsche Telekom AG"},
			{value:"TEF"    ,label:	"Telefonica SA"},
			{value:"MBT"    ,label:	"Mobile TeleSystems"},
			{value:"S" 		  ,label:	"Sprint Nextel"},
			{value:"LLY"    ,label:	"Eli Lilly and Company"},
			{value:"AMZN"   ,label:	"Amazon.com"},
			{value:"FB" 		,label:	"Facebook"},
			{value:"TWTR"   ,label:	"Twitte"}
			]
		
		return (
			<div class="col-md-3 top20 list-boxes" onClick={this.updateCreateStockPopup.bind(this, true)}>
				<div class="newCardStyle firstCard">
					<div class="card-header"></div>
					<div class="card-center newStoryCard">
						<div class="col-xs-3 col-xs-offset-2 xs-pr-0"><i class="fa fa-file-text-o fa-4x"></i></div>
						<div class="col-xs-6 xs-m-0 xs-pl-0"><small>Analyze</small></div>
					</div>
				</div>
				<div id="newCreateStock" role="dialog" className="modal fade modal-colored-header">
					<Modal class="stockExtractModel" show={store.getState().apps.appsCreateStockModal} onHide={this.updateCreateStockPopup.bind(this, false)} dialogClassName="modal-colored-header">
						<Modal.Header closeButton>
							<h3 className="modal-title">Input - Stocks and Data </h3>
						</Modal.Header>
						<Modal.Body>
							<form role="form" className="form-horizontal">
								<div className="form-group">
									<label className="col-sm-4 control-label mandate">Select News Source </label>
									<div class="col-sm-8">
									  <MultiSelect className="domainMultiselect" value={this.state.domain} options={domainList.sort((a, b) => (a.label > b.label) ? 1 : -1)} onChange={e => this.setState({ domain: e.value })}
                     style={{"width": "100%"}}  filter={true} placeholder="Choose News Source" />
                  </div>
								</div>
								<div className="form-group">
									<label className=" control-label col-md-4 mandate">Select Company </label>
									<div class="col-md-8">
										<MultiSelect className="comapanyMultiselect" value={this.state.company} options={companyList.sort((a, b) => (a.label > b.label) ? 1 : -1)} onChange={e => this.setState({ company: e.value })}
                     style={{"width": "100%"}}  filter={true} placeholder="Choose Company" />
                  </div>
								</div>
								<div className="xs-pb-25 clearfix"></div>
								<div class="form-group">
									<label className="col-md-4 control-label mandate">Name your Analysis </label>
									<div class="col-md-8">
										<input type="text" name="createStockAnalysisName" id="createStockAnalysisName" required={true} className="form-control input-sm" placeholder="Enter Analysis Name"/>
									</div>
								</div>
								<div className="clearfix"></div>
							</form>
							<div className="clearfix"></div>
						</Modal.Body>
						<Modal.Footer>
							<div id="resetMsg"></div>
							<Button className="btn btn-primary md-close" onClick={this.updateCreateStockPopup.bind(this, false)}>Close</Button>
							<Button bsStyle="primary" id='extractData' onClick={this.crawlDataForAnalysis.bind(this,companyList)}>Extract Data</Button>
						</Modal.Footer>
					</Modal>
				</div>
			</div>
		)
	}
}	  
	
	