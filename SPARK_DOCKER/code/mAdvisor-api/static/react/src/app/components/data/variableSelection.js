import React from "react";
import { Scrollbars } from 'react-custom-scrollbars';

import {connect} from "react-redux";
import {Link, Redirect} from "react-router-dom";
import {push} from "react-router-redux";
import {Modal,Button,Tab,Row,Col,Nav,NavItem} from "react-bootstrap";
import store from "../../store";

import {openCreateSignalModal,closeCreateSignalModal} from "../../actions/createSignalActions";
import {emptySignalAnalysis} from "../../actions/signalActions";

/*var dataSelection= {
     "metaData" : [   {"name": "Rows", "value": 30, "display":true},
                      {"name": "Measures", "value": 10, "display":true},
                     {"name": "Dimensions", "value": 5, "display":true},
                     {"name": "Ignore Suggestion", "value": 20, "display":false}
                 ],

    "columnData" : [{
			"name": "Age",
			"slug": "age_a",
			"columnStats":[ {"name": "Mean", "value":100}, {"name": "Sum", "value":1000}, {"name": "Min", "value":0},
							 {"name": "Max", "value":1000}	],
			"chartData" : {
                      "data": {
                  "columns": [
                      ['data1', 30, 200, 100, 400, 150, 250]

                  ],
                  "type": 'bar'
              },
              "size": {
                "height": 200
              },
              "legend": {
                 "show": false
               },
              "bar": {
                  "width": {
                      "ratio": 0.5
                  }

              }
          },
			"columnType": "measure"
      },
  	  {
  			"name": "Name",
  			"slug": "name_a",
  			"columnStats":[ {"name": "Mean", "value":200}, {"name": "Sum", "value":2000}, {"name": "Min", "value":0},
  							 {"name": "Max", "value":1000}	],
  			"chartData" : {
                        "data": {
                    "columns": [
                        ['data1', 30, 200, 100, 400, 150, 750]

                    ],
                    "type": 'bar'
                },
                "size": {
                  "height": 200
                },
                "legend": {
                "show": false
              },
                "bar": {
                    "width": {
                        "ratio": 0.5
                    }

                }
            },
  			"columnType": "dimension"
      },
      {
  			"name": "Sale Date",
  			"slug": "sale_a",
  			"columnStats":[ {"name": "Mean", "value":1100}, {"name": "Sum", "value":1030}, {"name": "Min", "value":0},
  							 {"name": "Max", "value":1000}	],
  			"chartData" : {
                        "data": {
                    "columns": [
                        ['data1', 30, 200, 100, 400, 950, 250]

                    ],
                    "type": 'bar'
                },
                "size": {
                  "height": 200
                },
                "legend": {
                   "show": false
                 },
                "bar": {
                    "width": {
                        "ratio": 0.5
                    }

                }
            },
  			"columnType": "datetime"
        }],
    "headers" :[
        {   "name": "Age",
          "slug" : "age_a" },
		  {   "name": "Name",
          "slug" : "name_a", },
          {   "name": "Sale Date",
              "slug" : "sale_a", }

      ],
    "sampleData" :[[20,30,'20/01/1990'],
	               [33,44,'10/01/1990'],
				   [24,33,'30/01/1990'],
				   [44,36,'20/02/1990']]
};*/

var selectedVariables = {measures:[],dimensions:[],date:null};  // pass selectedVariables to config

@connect((store) => {
	return {login_response: store.login.login_response,
		newSignalShowModal: store.signals.newSignalShowModal,
		dataList: store.datasets.dataList,
  dataPreview: store.datasets.dataPreview};
})

export class VariableSelection extends React.Component {
	constructor(props) {
		super(props);
    this.state={
      countOfSelected:0,
      radioChecked:""
    };
	props.dispatch(emptySignalAnalysis());
	}



componentDidMount(){
  var that = this;
 $(function(){
   selectedVariables.date = $("#rad_dt0").val();
    $("[type='radio']").click(function(){
         let id=$(this).attr("id");

        selectedVariables.date = $("#"+id).val();
         that.setState(previousState => {
          return {radioChecked:id
                    };
        });

    });

   $("#mea").click(function(){ 
     let count=0;
      if($(this).is(":checked")){
        $('.measure[type="checkbox"]').prop('checked', true);
      }else{
        $('.measure[type="checkbox"]').prop('checked', false);
      }
      selectedVariables.dimensions=[];
      $('.dimension[type="checkbox"]').each(function(){

         if($(this).is(":checked")){
           count++;
           selectedVariables.dimensions.push($(this).val());
         }
      });

      selectedVariables.measures=[];
      $('.measure[type="checkbox"]').each(function(){

         if($(this).is(":checked")){
           count++;
           selectedVariables.measures.push($(this).val());
         }
      });

      that.setState(previousState => {
       return { countOfSelected: count};
     });
   });

   $("#dim").click(function(){    
     let count=0;
      if($(this).is(":checked")){
         $('.dimension[type="checkbox"]').prop('checked', true);
      }else{
         $('.dimension[type="checkbox"]').prop('checked', false);
      }

      selectedVariables.dimensions=[];
      $('.dimension[type="checkbox"]').each(function(){

         if($(this).is(":checked")){
           count++;
           selectedVariables.dimensions.push($(this).val());
         }
      });
      selectedVariables.measures=[];
      $('.measure[type="checkbox"]').each(function(){

         if($(this).is(":checked")){
           count++;
           selectedVariables.measures.push($(this).val());
         }
      });


      that.setState(previousState => {
       return { countOfSelected: count};
     });

   });

$('.measure[type="checkbox"]').click(function(){
  let count = 0;
  selectedVariables.measures=[];
  $('.measure[type="checkbox"]').each(function(){
     if(!$(this).is(":checked")){
       $('#mea[type="checkbox"]').prop('checked',false);
     }else{

       count++;
        selectedVariables.measures.push($(this).val());
     }
  });
  selectedVariables.dimensions=[];
  $('.dimension[type="checkbox"]').each(function(){

     if(!$(this).is(":checked")){
       $('#mea[type="checkbox"]').prop('checked',false);
     }else{

       count++;
       selectedVariables.dimensions.push($(this).val());
     }
  });
  that.setState(previousState => {
   return { countOfSelected: count};
 });

});

$('.dimension[type="checkbox"]').click(function(){
  let count=0;
   selectedVariables.dimensions=[];
  $('.dimension[type="checkbox"]').each(function(){
     if(!$(this).is(":checked")){
       $('#dim[type="checkbox"]').prop('checked',false);
     }else{

       count++;
       selectedVariables.dimensions.push($(this).val());
     }
  });
   selectedVariables.measures=[];
  $('.measure[type="checkbox"]').each(function(){
     if(!$(this).is(":checked")){
       $('#mea[type="checkbox"]').prop('checked',false);
     }else{

       count++;
        selectedVariables.measures.push($(this).val());
     }
  });
  that.setState(previousState => {
   return { countOfSelected: count};
 });
});

 });



}



	render() {
    const metaData = dataSelection.columnData;
    var measures =[], dimensions =[],datetime =[];
    metaData.map((metaItem,metaIndex)=>{
      switch(metaItem.columnType){
        case "measure":
         measures.push(metaItem.name);
         break;
        case "dimension":

         dimensions.push(metaItem.name);
        break;
        case "datetime":
          datetime.push(metaItem.name);
        break;
      }

    });

  if(measures.length>0){
  var measureTemplate = measures.map((mItem,mIndex)=>{
      const mId = "chk_mea" + mIndex;
      return(
        <li key={mIndex}><div className="ma-checkbox inline"><input id={mId} type="checkbox" className="measure" value={mItem} defaultChecked={true}/><label htmlFor={mId} className="radioLabels">{mItem}</label></div> </li>
      );
  });
}else{
  var measureTemplate =  <label>No measure variable present</label>
}

if(dimensions.length>0){
  var dimensionTemplate = dimensions.map((dItem,dIndex)=>{
      const dId = "chk_dim" + dIndex;
    return(
     <li key={dIndex}><div className="ma-checkbox inline"><input id={dId} type="checkbox" className="dimension" value={dItem} defaultChecked={true}/><label htmlFor={dId}>{dItem}</label></div> </li>
   );
  });
}else{
  var dimensionTemplate =  <label>No dimension variable present</label>
}

if(datetime.length>0){
  var datetimeTemplate = datetime.map((dtItem,dtIndex)=>{
    const dtId = "rad_dt" + dtIndex;
  return(
   <li key={dtIndex}><div className="ma-radio inline"><input type="radio" checked={this.state.radioChecked === dtId} name="date_type" id={dtId} value={dtItem}/><label htmlFor={dtId}>{dtItem}</label></div></li>
 );
  });
}else{
  var datetimeTemplate = <label>No date dimensions to display</label>
}

		return (

      <div className="main-content">
<div className="panel panel-default">
  <div className="panel-body">

  <div className="row">
   <label className="col-lg-2" for="signalVariableList">I want to analyze</label>
  <div className="col-lg-4">
      <div className="htmlForm-group">
        <select className="htmlForm-control" id="selectAnalyse">
          <option>I want to analyze</option>
          <option>I want to analyze 2</option>
          <option>I want to analyze 3</option>
          <option>I want to analyze 4</option>
        </select>
      </div>
  </div>{/*<!-- /.col-lg-4 -->*/}

  </div>{/*<!-- /.row -->*/}
  <div className="row">
  <div className="col-lg-4">
      <label>Including the following variables:</label>
  </div>{/*<!-- /.col-lg-4 -->*/}
  </div>
  <div className="row">
  <div className="col-lg-4">
    <div className="panel panel-primary-p1 cst-panel-shadow">
    <div className="panel-heading"><i className="pe-7s-graph1"></i> Measures</div>
    <div className="panel-body">
      {/*<!-- Row htmlFor select all-->*/}
      <div className="row">
        <div className="col-md-4">
          <div className="ma-checkbox inline">
          <input id="check1" type="checkbox" className="needsclick">
          <label htmlFor="check1">Select All</label>
          </div>
        </div>
        <div className="col-md-8">
          <div className="input-group pull-right">
            <input type="text" className="htmlForm-control" placeholder="Search measures..." name="srch-measure" id="srch-measure">
          <span className="input-group-btn">
          <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i className="fa fa-sort-alpha-asc fa-lg"></i> <span className="caret"></span></button>
          <ul role="menu" className="dropdown-menu dropdown-menu-right">
          <li><a href="#">Name Ascending</a></li>
          <li><a href="#">Name Descending</a></li>
          <li><a href="#">Date Ascending</a></li>
          <li><a href="#">Date Descending</a></li>
          </ul>
          </span>
          </div>
        </div>
      </div>
      {/*<!-- End -->*/}
      <hr />
      {/*<!-- Row htmlFor list of variables-->*/}
      <div className="row">
        <div className="col-md-12 cst-scroll-panel">
		<Scrollbars>
          <ul className="list-unstyled">
                              {measureTemplate}
          </ul>
		 </Scrollbars>
        </div>
      </div>
      {/*<!-- End Row htmlFor list of variables-->*/}
    </div>
    </div>

  </div>{/*<!-- /.col-lg-4 -->*/}
  <div className="col-lg-4">
      <div className="panel panel-primary-p2 cst-panel-shadow">
      <div className="panel-heading"><i className="pe-7s-graph2"></i> Dimensions</div>
        <div className="panel-body">
            {/*<!-- Row htmlFor select all-->*/}
            <div className="row">
              <div className="col-md-4">
                <div className="ma-checkbox inline">
                <input id="check2" type="checkbox" className="needsclick">
                <label htmlFor="check2">Select All</label>
                </div>
              </div>
            <div className="col-md-8">
              <div className="input-group pull-right">
              <input type="text" className="htmlForm-control" placeholder="Search dimension..." name="srch-dimension" id="srch-dimension">
              <span className="input-group-btn">
              <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i className="fa fa-sort-alpha-asc fa-lg"></i>&nbsp;<span className="caret"></span></button>
              <ul role="menu" className="dropdown-menu dropdown-menu-right">
              <li><a href="#"><i class="fa fa-sort-alpha-asc" aria-hidden="true"></i> Name Ascending</a></li>
              <li><a href="#"><i class="fa fa-sort-alpha-desc" aria-hidden="true"></i> Name Descending</a></li>
              <li><a href="#"><i class="fa fa-sort-numeric-asc" aria-hidden="true"></i> Date Ascending</a></li>
              <li><a href="#"><i class="fa fa-sort-numeric-desc" aria-hidden="true"></i> Date Descending</a></li>
              </ul>
              </span>
              </div>
            </div>
            </div>
            {/*<!-- End -->*/}
            <hr />
            {/*<!-- Row htmlFor list of variables-->*/}
            <div className="row">
            <div className="col-md-12 cst-scroll-panel">
			<Scrollbars>
              <ul className="list-unstyled">
            {dimensionTemplate}
              </ul>
			</Scrollbars>
            </div>
            </div>
            {/*<!-- End Row htmlFor list of variables-->*/}


        </div>
      </div>


  </div>{/*<!-- /.col-lg-4 -->*/}
  <div className="col-lg-4">
      <div className="panel panel-primary-p3 cst-panel-shadow">
    <div className="panel-heading"><i className="pe-7s-date"></i> Dates</div>
    <div className="panel-body">

      {/*<!-- Row htmlFor options all-->*/}
            <div className="row">
              <div className="col-md-4">

              </div>
            <div className="col-md-8">
              <div className="input-group pull-right">
              <input type="text" className="htmlForm-control" placeholder="Search date type..." name="srch-dtype" id="srch-dtype">
              <span className="input-group-btn">
              <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i className="fa fa-sort-alpha-asc fa-lg"></i> <span className="caret"></span></button>
              <ul role="menu" className="dropdown-menu dropdown-menu-right">
              <li><a href="#">Name Ascending</a></li>
              <li><a href="#">Name Descending</a></li>
              <li><a href="#">Date Ascending</a></li>
              <li><a href="#">Date Descending</a></li>
              </ul>
              </span>
              </div>
            </div>
            </div>
            {/*<!-- End Row htmlFor options all -->*/}
            <hr />
            {/*<!-- Row htmlFor list of variables-->*/}
            <div className="row">
            <div className="col-md-12 cst-scroll-panel">
			<Scrollbars>
              <ul className="list-unstyled">
              {datetimeTemplate}
              </ul>
			</Scrollbars>
            </div>
            </div>
            {/*<!-- End Row htmlFor list of variables-->*/}

    </div>
    </div>
  </div>{/*<!-- /.col-lg-4 -->*/}
  </div>{/*<!-- /.row -->*/}

  <div className="row">
    <div className="col-md-4 col-md-offset-5">
        <h4>18 Variable selected <a href="javascript:;" className="pover" data-popover-content="#selected_var" data-placement="bottom" data-toggle="popover"><i className="pe-7s-more pe-2x pe-va"></i></a></h4>
    </div>

    <div id="selected_var" className="pop_box hide">
    <div className="row">
      <div className="col-md-6">
      <select className="htmlForm-control">
          <option selected>Variable Type</option>
          <option>Measures</option>
          <option>Dimensions</option>
        </select>
      </div>
      <div className="col-md-6">
        <div className="input-group pull-right">
          <input type="text" className="htmlForm-control" placeholder="Search date type..." name="srch-dtype" id="srch-dtype">
          <span className="input-group-btn">
          <button type="button" data-toggle="dropdown" title="Sorting" className="btn btn-default dropdown-toggle" aria-expanded="false"><i className="fa fa-sort-alpha-asc fa-lg"></i> <span className="caret"></span></button>
          <ul role="menu" className="dropdown-menu dropdown-menu-right">
          <li><a href="#">Name Ascending</a></li>
          <li><a href="#">Name Descending</a></li>
          <li><a href="#">Date Ascending</a></li>
          <li><a href="#">Date Descending</a></li>
          </ul>
          </span>
        </div>
      </div>
      <div className="clearfix"></div>
    </div>
    <div className="row">
      <div className="col-md-12">
        <div className="panel seld_var_box">
        <a>Tax rate <i className="remove pe-7s-close"></i></a>
        <a>City <i className="remove pe-7s-close"></i></a>
        <a>Unit price <i className="remove pe-7s-close"></i></a>
        <a>Gender <i className="remove pe-7s-close"></i></a>
        <a>Profits <i className="remove pe-7s-close"></i></a>
        </div>
      </div>
    </div>
    </div>

  </div>
  <div className="row">
    <div className="col-md-12">
      <div className="panel panel-alt4 panel-borders">
        <div className="panel-heading text-center">PerhtmlForming the following Analysis</div>
        <div className="panel-body text-center">
          <div className="ma-checkbox inline"><input id="chk_analysis0" type="checkbox" className="needsclick"><label htmlFor="chk_analysis0">Distribution Analysis </label></div>
          <div className="ma-checkbox inline"><input id="chk_analysis1" type="checkbox" className="needsclick"><label htmlFor="chk_analysis1">Trend Analysis </label></div>
          <div className="ma-checkbox inline"><input id="chk_analysis2" type="checkbox" className="needsclick"><label htmlFor="chk_analysis2">Anova </label></div>
          <div className="ma-checkbox inline"><input id="chk_analysis3" type="checkbox" className="needsclick"><label htmlFor="chk_analysis3">Regression </label></div>
          <div className="ma-checkbox inline"><input id="chk_analysis4" type="checkbox" className="needsclick"><label htmlFor="chk_analysis4">Decision Tree</label></div>
          <hr>
          <div className="pull-left">
          <div className="ma-checkbox inline"><input id="chk_results" type="checkbox" className="needsclick"><label htmlFor="chk_results">Statistically Significant Results</label></div>
          </div>
          <div className="pull-right">
          <a href="javascript:;" className="pull-right">Advanced Settings</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div className="row">
    <div className="col-lg-4 col-lg-offset-8">
      <div className="htmlForm-group">
        <input type="text" name="createSname" id="createSname" className="htmlForm-control input-sm" placeholder="Enter a signal name">
      </div>
    </div>{/*<!-- /.col-lg-4 -->*/}
  </div>
  <hr/>
  <div className="row">
    <div className="col-md-12 text-right">
      <button className="btn btn-primary">CREATE SIGNAL</button>
    </div>
  </div>


  </div>
</div>
    </div>

		)
	}

}
