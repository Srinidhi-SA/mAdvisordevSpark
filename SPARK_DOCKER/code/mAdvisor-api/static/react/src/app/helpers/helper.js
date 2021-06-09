import React from "react";
import CircularProgressbar from 'react-circular-progressbar';
import {handleDecisionTreeTable} from "../actions/signalActions";
import {API, STATIC_URL} from "./env";
import {showLoading, hideLoading} from 'react-redux-loading-bar';
import { renderToString } from 'react-dom/server'
import Scrollbars from "react-custom-scrollbars/lib/Scrollbars";

function getHeader(token) {
  return {'Authorization': token, 'Content-Type': 'application/json'};
}

export function isEmpty(obj) {
  for (var prop in obj) {
    if (obj.hasOwnProperty(prop))
      return false;
    }

  return JSON.stringify(obj) === JSON.stringify({});
}

var USERDETAILS = {};

export const getUserDetailsOrRestart = {
  get: function() {
    let userDetails = {};
    if (document.cookie) {
      let allCookies = document.cookie.split(";");
      for (let i = 0; i < allCookies.length; i++) {
        let cur = allCookies[i].split('=');
        userDetails[cur[0].replace(/\s/g, '')] = cur[1];
      }
      return userDetails;
    } else {
      redirectToLogin();
    }

  }
}

function redirectToLogin() {
  var noOfUrls = window.history.length;
  window.history.go("-" + noOfUrls - 1);
}

const FILEUPLOAD = "fileUpload";
const MYSQL = "MySQL";
const MSSQL = "mssql";
const HANA = "Hana";
const HDFS = "Hdfs";
const INPUT = "Input";
const HOST = "Host";
const PORT = "Port";
const SCHEMA = "Schema";
const USERNAME = "Username";
const PASSWORD = "Password";
const TABLENAME = "tablename";
const PERPAGE = 12;
const NORMALTABLE = "normal";
const CONFUSIONMATRIX = "confusionMatrix";
const HEATMAPTABLE = "heatMap";
const CIRCULARCHARTTABLE = "circularChartTable";
const DULOADERPERVALUE = -1;
const CSLOADERPERVALUE = -1;
const APPSLOADERPERVALUE = -1;
const LOADERMAXPERVALUE = 99;
const DEFAULTINTERVAL = 10000;
const APPSDEFAULTINTERVAL = 10000;
const CUSTOMERDATA = "Customer Data";
const HISTORIALDATA = "Historial Data";
const EXTERNALDATA = "External Data";
const DELETEMODEL = "Delete Model";
const RENAMEMODEL = "Rename Model";
const DELETESCORE = "Delete Score";
const RENAMESCORE = "Rename Score";
const DELETEINSIGHT = "Delete Insight";
const RENAMEINSIGHT = "Rename Insight";
const SEARCHCHARLIMIT = 2;
const SUCCESS = "SUCCESS";
const FAILED = "FAILED";
const INPROGRESS = "INPROGRESS";
const APPNAME1 = "OPPORTUNITY SCORING";
const APPNAME2 = "AUTOMATED PREDICTION";
const APPNAME3 = "ROBO INSIGHTS";
const APPNAME5 = "STOCK ADVISOR";
const APPID1 = 1;
const APPID2 = 2;
const APPID3 = 3;
const APPID5 = 5;
const CUSTOMER = "customer";
const HISTORIAL = "historical";
const EXTERNAL = "external";
const APPID4 = 4;
const APPNAME4 = "Speech Analytics";
const DELETEAUDIO = "Delete Media File";
const RENAMEAUDIO = "Rename Media File";
const DULOADERPERMSG = "Preparing data for loading";
const RENAME = "rename";
const DELETE = "delete";
const REPLACE = "replace";
const DATA_TYPE = "data_type";
const REMOVE = "remove";
const CURRENTVALUE = "current value";
const NEWVALUE = "new value";
const TEXTHEATMAPTABLE = "textHeatMapTable";
const DEFAULTANALYSISVARIABLES = "high";
const MINROWINDATASET = 10;
const APPSPERPAGE = 9;
const POPUPDECISIONTREETABLE = "popupDecisionTreeTable";
const MAXTEXTLENGTH = 375;
const SET_VARIABLE = "set_variable";
const DIMENSION = "dimension";
const MEASURE = "measure";
const PERCENTAGE = "percentage";
const GENERIC_NUMERIC = "generic_numeric";
const SET_POLARITY = "set_polarity";
const UNIQUE_IDENTIFIER = "unique_identifier";
const DYNAMICLOADERINTERVAL = 2000;
const IGNORE_SUGGESTION = "ignore_suggestion";
const ACCESSDENIED = "Access Denied"
const CREATESIGNAL = "Create Signal";
const PROCEEDTODATACLEANSING = "Proceed to data cleansing";
const PROCEEDTOFEATUREENGINEERING ="proceed to feature Engineering"
const PROCEEDTOMODELMANAGEMENT= "proceed to model management"
const CREATEMODEL = "Create Model";
const CREATESCORE = "Create Score";
const DELETESTOCKMODEL = "Delete Analysis";
const RENAMESTOCKMODEL = "Rename Analysis";
const DELETEALGO ="Delete this Model";
const CLONEALGO ="Clone this Model"
const DELETEDEPLOYMENT ="Delete this Deployment"

export function generateHeaders(table) {
  var cols = table.tableData.map(function(rowData, i) {
    if (i == 0) {
      return rowData.map(function(colData, j) {
        return <th key={j}>{colData}</th>;
      });
    }
  })
  return cols;
}

export function generateHeatMapHeaders(table) {
  var cols = table.tableData.map(function(rowData, i) {
    if (i == 0) {
      var row = rowData.map(function(colData, j) {
        return <th key={j} className="first">{colData}</th>;
      });
      return <tr key={i} className="heatMapHeader">{row}</tr>
    }
  })

  return cols;
}

export function generateHeatMapRows(table) {
  var cols = table.tableData.map(function(rowData, i) {
    if (i != 0) {
      var row = rowData.map(function(colData, j) {
        if (j == 0) {
          return <td key={j} className="stats-title">{colData}</td>;
        } else {
          return <td key={j}>{colData}</td>;
        }

      });
      return <tr key={i} className="stats-row">{row}</tr>
    }
  })

  return cols;
}

export function generateTextHeatMapRows(table) {
  var cols = table.tableData.map(function(rowData, i) {
    if (i != 0) {
      var row = rowData.map(function(colData, j) {
        if (colData.value == 0 && colData.text == "") {
          return <td key={j} value={colData.value}></td>;
        } else {
          return <td key={j} value={colData.value}>{colData.text}<br/>
            <b>{colData.value}</b>
          </td>;
        }

      });
      return <tr key={i} className="stats-row">{row}</tr>
    }
  })

  return cols;
}

export function generateCircularChartRows(table) {
  var tbodyData = table.tableData.map(function(rowData, i) {
    if (i != 0) {
      var rows = rowData.map(function(colData, j) {
        if (isNaN(colData))
          return <td key={j}>{colData}</td>;
        else
          return <td style={{"width":"20%"}} key={j}><CircularProgressbar percentage={colData} initialAnimation={true}/></td>;
        }
      );
      return <tr key={i}>{rows}</tr>;
    }
  })
  return tbodyData;
}
export function generateRows(table) {
  var tbodyData = table.tableData.map(function(rowData, i) {
    if (i != 0) {
      var rows = rowData.map(function(colData, j) {
        return <td key={j}>{colData}</td>;
      });
      return <tr key={i}>{rows}</tr>;
    }
  })
  return tbodyData;
}

export function generateNormalTableRows(table) {
  var tbodyData = table.tableData.map(function(rowData, i) {
    if (i != 0) {
      var rows = rowData.map(function(colData, j) {
        if(typeof(colData)==="object" && colData != null){
          return <td key={j}>{colData["loss"]!=undefined?colData["loss"]:colData["optimizer"]}</td>
        }
        else if (j == 0 || j == 1)
          return <td key={j}>{colData}</td>;
        else
          return <td key={j}>{colData}</td>;
        }
      );
      return <tr key={i}>{rows}</tr>;
    }
  })
  return tbodyData;
}

export function subTreeSetting(urlLength, length, paramL2, classname = ".sb_navigation #subTab i.mAd_icons.ic_perf ~ span") {
  $(function() {
    if (urlLength == length) {
      $(".sb_navigation").show();
      $(classname).each(function() {
        if ($(this).attr('id') == paramL2) {
          $(this).parent().addClass('active');
        } else {
          $(this).parent().removeClass('active');
        }
      });

    } else {
      $(".sb_navigation").hide();
    } 

    if ($(".list-group").children()) { 
      if ($(".list-group").children().length == 1) {
        $('.row-offcanvas-left').addClass('active');
        $('.sdbar_switch i').removeClass('sw_on');
        $('.sdbar_switch i').addClass('sw_off');
      }
    }
  });

}

export function showHideSideChart(colType, chartData) {

  if (colType == "datetime" || $.isEmptyObject(chartData)) {
    $(function() {
      $("#tab_visualizations #pnl_visl").removeClass("in");
      $("#tab_visualizations a").addClass("collapsed");
    });
  } else {
    $(function() {
      $("#tab_visualizations #pnl_visl").addClass("in");
      $("#tab_visualizations a").removeClass("collapsed");
      $("#tab_visualizations #pnl_visl").removeAttr("style");
    });
  }

}

export function showHideSideTable(colstats) {
  let flag = false

  for (var i = 0; i < colstats.length; i++) {
    if (colstats[i].display) {
      flag = true;
    }
  }

  if (colstats.length == 0 || !flag) {

    $("#tab_statistics #pnl_stc").removeClass("in");
    $("#tab_statistics a").addClass("collapsed");
  } else {
    $("#tab_statistics #pnl_stc").addClass("in");
    $("#tab_statistics a").removeClass("collapsed");
    $("#tab_statistics #pnl_stc").removeAttr("style");
  }
}

export function decimalPlaces(number) {
  return ((+ number).toFixed(4)).replace(/^-?\d*\.?|0+$/g, '').length;
}

export function handleJobProcessing(slug) {
  return (dispatch) => {
    dispatch(showLoading());
    return updateJobStatus(slug, dispatch).then(([response, json]) => {
      dispatch(hideLoading());
    })
  }

}
export function updateJobStatus(slug, dispatch) {
  return fetch(API + '/api/get_job_kill/' + slug + '/', {
    method: 'get',
    headers: getHeader(getUserDetailsOrRestart.get().userToken)
  }).then(response => Promise.all([response, response.json()])).catch(function(error) {
    dispatch(hideLoading());
    bootbox.alert("Unable to connect to server. Check your connection please try again.")
  });
}
export {
  FILEUPLOAD,
  MYSQL,
  INPUT,
  PASSWORD,
  HOST,
  PORT,
  SCHEMA,
  USERNAME,
  TABLENAME,
  PERPAGE,
  NORMALTABLE,
  CONFUSIONMATRIX,
  HEATMAPTABLE,
  CIRCULARCHARTTABLE,
  DULOADERPERVALUE,
  CSLOADERPERVALUE,
  LOADERMAXPERVALUE,
  DEFAULTINTERVAL,
  APPSDEFAULTINTERVAL,
  CUSTOMERDATA,
  HISTORIALDATA,
  EXTERNALDATA,
  DELETEMODEL,
  RENAMEMODEL,
  DELETESCORE,
  RENAMESCORE,
  DELETEINSIGHT,
  RENAMEINSIGHT,
  SEARCHCHARLIMIT,
  SUCCESS,
  FAILED,
  INPROGRESS,
  APPNAME1,
  APPNAME2,
  APPNAME3,
  APPID1,
  APPID2,
  APPID3,
  CUSTOMER,
  HISTORIAL,
  EXTERNAL,
  APPID4,
  APPNAME4,
  RENAMEAUDIO,
  DELETEAUDIO,
  DULOADERPERMSG,
  RENAME,
  DELETE,
  REPLACE,
  DATA_TYPE,
  REMOVE,
  CURRENTVALUE,
  NEWVALUE,
  APPID5,
  APPNAME5,
  TEXTHEATMAPTABLE,
  APPSLOADERPERVALUE,
  USERDETAILS,
  DEFAULTANALYSISVARIABLES,
  MINROWINDATASET,
  APPSPERPAGE,
  POPUPDECISIONTREETABLE,
  MAXTEXTLENGTH,
  SET_VARIABLE,
  DIMENSION,
  MEASURE,
  PERCENTAGE,
  GENERIC_NUMERIC,
  SET_POLARITY,
  UNIQUE_IDENTIFIER,
  DYNAMICLOADERINTERVAL,
  IGNORE_SUGGESTION,
  HDFS,
  HANA,
  MSSQL,
  ACCESSDENIED,
  CREATESIGNAL,
  PROCEEDTODATACLEANSING,
  PROCEEDTOFEATUREENGINEERING,
  PROCEEDTOMODELMANAGEMENT,
  CREATESCORE,
  CREATEMODEL,
  DELETESTOCKMODEL,
  RENAMESTOCKMODEL,
  DELETEALGO,
  CLONEALGO,
  DELETEDEPLOYMENT

}
export function capitalizeArray(array) {
  let a = []
  let i = 0
  for (var val in array) {
    a[i] = array[val].charAt(0).toUpperCase() + array[val].slice(1);
    i++;
  }
  return a
}
export function predictionLabelClick() {
  var cell = document.querySelectorAll('.pred_disp_block');
  for (var i = 0; i < cell.length; i++) {
    cell[i].addEventListener('click', handleDecisionTreeTable, false);
  }

}

export function renderC3ChartInfo(info) {
  if (!isEmpty(info)) {

    var listOfData = "";
    info.map((item) => {
      listOfData += "<p>" + item + "</p>";
    });
    bootbox.dialog({
      title: "Statistical Info",
      size: 450,//'small',
      closeButton: true,
      message: "<div>" + listOfData + "</div>",
      onEscape: true
    })
  }

}

export function bytesToSize(bytes) {
  var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes == 0)
    return '0 Byte';
  var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
};

export function downloadSVGAsPNG(chartClassId) {
  var nodeList = []
  var nodeList2 = []
  var nodeList4 = []
  nodeList = document.querySelector("." + chartClassId + ">svg").querySelectorAll('.c3-chart .c3-chart-lines path');
  nodeList2 = document.querySelector("." + chartClassId + ">svg").querySelectorAll('.c3-axis path');
  nodeList4 = document.querySelector("." + chartClassId + ">svg").querySelectorAll(".c3-title");

  var line_graph = Array.from(nodeList);
  var x_and_y = Array.from(nodeList2);
  var titles = Array.from(nodeList4);

  line_graph.forEach(function(element) {
    element.style.fill = "none";
  });
  x_and_y.forEach(function(element) {
    element.style.fill = "none";
    element.style.stroke = "black";
  });
  titles.forEach(function(element){
    element.setAttribute("x",parseFloat(element.getAttribute("x"))+25)
  })
  saveSvgAsPng(document.querySelector("." + chartClassId + ">svg"), "chart.png", {
    backgroundColor: "white",
    height: parseFloat(document.querySelector("." + chartClassId + ">svg").getAttribute("height"))+20
  });

}
export function statusMessages(msg_type, msg, mascot_type) {
  let imgsrc_url = ""
  let status_text = ""
  let htmlString = ""
  switch (msg_type) {
    case "warning":
      {
        imgsrc_url = STATIC_URL + "assets/images/alert_warning.png"
        status_text = '<h4 class="text-warning">Warning !</h4>'
      }
      break;
    case "error":
      {
        imgsrc_url = STATIC_URL + "assets/images/alert_danger.png"
        status_text = '<h4 class="text-danger">Ooops !</h4>'
      }
      break;
    case "info":
      {
        imgsrc_url = STATIC_URL + ""
        status_text = ''
      }
      break;
    case "success":
      {
        imgsrc_url = STATIC_URL + "assets/images/alert_success.png"
        status_text = '<h4 class="text-primary">Success !</h4>'
      }
  }
  if (mascot_type == "without_mascot") {
    htmlString = '<div class="border border-danger"><h4 class="alert-heading">Error !</h4><p>' + msg + '</p></div>'
  }else if(mascot_type ==="failed_mascot"){
    let strng = renderToString(<Scrollbars autoHeight autoHeightMax={275} autoHide={false}
      renderTrackHorizontal={props => <div {...props} className="track-horizontal" style={{display:"none"}}/>} 
      renderThumbHorizontal={props => <div {...props} className="thumb-horizontal" style={{display:"none"}}/>}>
      {msg}</Scrollbars>)
    htmlString = '<div class="row" style="display:flex"><div class="col-md-4" style="display: flex"><img src=' + imgsrc_url + ' class="img-responsive" style="margin:auto"/></div><div class="col-md-8">'+status_text+'<p>'+strng+'</p></div></div>'
  }else {
    htmlString = '<div class="row"><div class="col-md-4"><img src=' + imgsrc_url + ' class="img-responsive" /></div><div class="col-md-8">' + status_text + '<p>' + msg + '</p></div></div>';
  }
  return htmlString
}


export function removeChatbotOnLogout() {
  var tags = document.getElementsByTagName('script');
  for (var i = tags.length; i >= 0; i--) { //search backwards within nodelist for matching elements to remove
    if (tags[i] && tags[i].getAttribute('src') != null && tags[i].getAttribute('src').indexOf("client-plugin/bot.js") != -1)
      tags[i].parentNode.removeChild(tags[i]); //remove element by calling parentNode.removeChild()
    }
  }

export function hidechatbot() {

  var chatwindow = document.getElementById("welcome-body-frame")
  if (chatwindow != null)
  chatwindow.parentNode.removeChild(chatwindow)

    Array.from(document.getElementsByClassName("chat-icon-container")).forEach(element => element.remove());

    Array.from(document.getElementsByClassName("chat-container")).forEach(element => element.remove());

}


export function checkChatbotPresent() {
  var tags = document.getElementsByTagName('script');
  for (var i = tags.length; i >= 0; i--) { //search backwards within nodelist for matching elements to remove
    if (tags[i] && tags[i].getAttribute('src') != null && tags[i].getAttribute('src').indexOf("client-plugin/bot.js") != -1)
      return true
  }
  return false
}

export function getRemovedVariableNames(dataset){
    var arr = [];

    var pickRemoved = function(item){
        if(item.targetColumn||!item.selected ){
            arr.push(item.name)
        }
    }
    dataset.CopyOfDimension.map(pickRemoved);
    dataset.CopyOfMeasures.map(pickRemoved);
    dataset.CopyTimeDimension.map(pickRemoved);
    return arr;

}

export function FocusSelectErrorFields(){
  var selectBoxList=[ "loss_pt",  "reduction_pt", "zero_infinity_pt",  "log_input_pt",
   "full_pt", "amsgrad_pt", "nesterov_pt", "line_search_fn_pt","centered_pt",
   "optimizer_pt","regularizer_pt","affine_pt","track_running_stats_pt","bias_pt",
   "add_bias_kv_pt","add_zero_attn_pt","head_bias_pt",
   "mode_pt" ,"nonlinearity_pt", "bias_init_pt", "weight_init_pt","num_parameters_pt"] // "dropout_pt" 
  var selectBoxError=false
    for(var i=0;i<selectBoxList.length;i++){
       if(($("."+selectBoxList[i])[0] != undefined) && ($("."+selectBoxList[i]+" option:selected").text().toLowerCase().includes("--select--"))){
       document.getElementsByClassName(selectBoxList[i])[0].classList.add('regParamFocus')
       selectBoxError=true
       }
    }
  return selectBoxError
}

export function FocusInputErrorFields(){
   var inputsError=false
   var inputFileds=["blank_pt","rho_pt","lr_pt","lr_decay_pt","weight_decay_pt"
   ,"eps_pt","max_iter_pt","max_eval_pt","tolerance_grad_pt","tolerance_change_pt","dampening_pt","lambd_pt",
   "alpha_pt","t0_pt","history_size_pt","betas1_pt","betas2_pt","eta1_pt","eta2_pt","step_sizes1_pt",
   "step_sizes2_pt","l1_decay_pt","l2_decay_pt","min_val_pt","max_val_pt","negative_slope_pt","kdim_pt",
   "vdim_pt","init_pt","lower_pt","upper_pt","p_pt","beta_pt","threshold_pt","value_pt","div_value_pt","val_pt",
   "mean_pt","std_pt","gain_pt","a_pt","sparsity_pt","std_pt","dropout_pt","lower_bound_pt","upper_bound_pt"
   ,"input_unit_pt","output_unit_pt"
   ]

   for(var i=0;i<inputFileds.length;i++){
       if($("."+inputFileds[i])[0] != undefined && (($("."+inputFileds[i])[0]).value === "" || $("."+inputFileds[i])[0].value === undefined)){
       document.getElementsByClassName(inputFileds[i])[0].classList.add('regParamFocus')
       inputsError=true
       }
   }
   return inputsError
}

export function setDateFormatHelper(created_at){
  let date = new Date( Date.parse(created_at) );
  let fomattedDate=date.toLocaleString('default', { month: 'short' })+" "+date.getDate()+","+date.getFullYear()+" "+(date.getHours() < 10 ? '0' : '')+date.getHours()+':'+(date.getMinutes() < 10 ? '0' : '')+date.getMinutes()
 return fomattedDate
 }