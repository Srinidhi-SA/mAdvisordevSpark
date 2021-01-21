import React from "react";
import {API,STATIC_URL} from "../helpers/env";


export function missingValueTreatmentSelectedAction(colName,colType,colSlug, treatment, dispatch){
  return {
		type: "MISSING_VALUE_TREATMENT",
		colName,
    colType,
    colSlug,
    treatment
	}
}
export function outlierRemovalSelectedAction(colName,colType,colSlug, treatment, dispatch){
  return {
		type: "OUTLIER_REMOVAL",
		colName,
    colType,
    colSlug,
    treatment
	}
}
export function variableSelectedAction(colName,colSlug, selecteOrNot, dispatch){
  return {
		type: "VARIABLE_SELECTED",
    colName,
    colSlug,
    selecteOrNot
	}
}
export function checkedAllAction( selecteOrNot, dispatch){
  return {
		type: "CHECKED_ALL_SELECTED",
    selecteOrNot
	}
}
export function dataCleansingCheckUpdate( index,checkedOrNot){
  return {
		type: "DATA_CLEANSING_CHECK_UPDATE",
    checkedOrNot,
    index
	}
}

export function removeDuplicateObservationsAction(duplicate_observation_removal, yesOrNo, dispatch){
     return {
		type: "REMOVE_DUPLICATE_OBSERVATIONS",
    yesOrNo, 
    duplicate_observation_removal
	}
}

export function dataCleansingDataTypeChange(colSlug, newDataType, dispatch){
    return {
        type: "DATACLEANSING_DATA_TYPE_CHANGE",
        colSlug,
        newDataType
    }
}

export function searchTable(tableName,trVal,spanVal){
    var filter, table, tr, td, i, txtValue, matchFound=false, hasError=false;
    filter = document.getElementById("search").value.toUpperCase();
    table = document.getElementById(tableName);
    tr = table.getElementsByTagName("tr");
    // if value is not empty calling for loop and handle table rows using style.display
    if(filter!=""){
      for(i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[trVal];
        if(td){
          txtValue = td.textContent || td.innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1){
            tr[i].style.display = "";
          }else{
            if(!tr[i].firstChild.innerText.includes("No data found")){
              tr[i].style.display = "none";
            }
          }
        }
      }
    }else{
      //value is empty show all the rows by making dispaly="" for all the rows
      for (i = 0; i < tr.length; i++) {
        tr[i].style.display = "";
      }
    }
    //check whether the search result found and has an error row
    for(i=1;i<=tr.length-1;i++){
      if(tr[i].style.display=="" && !tr[i].firstChild.innerText.includes("No data found")){
        matchFound=true
      }
      if(tr[i].firstChild.innerText.includes("No data found")){
        hasError=true
      }
    }
    //using above flags, add and delete the error message row from the table
    if(!matchFound &&!hasError){
      var htmlContent = '<tr class="noData"><td class="searchErr" colspan="'+spanVal+'" style="text-align:center">"No data found for your selection"</td></tr>'
      var tableRef = document.getElementById('tableName').getElementsByTagName('tbody')[0];
      var newRow = tableRef.insertRow(tableRef.rows.length);
      newRow.innerHTML = htmlContent;
    }else if(hasError && matchFound){
      if(tr[tr.length-1].firstChild.innerText.includes("No data found"))
        document.getElementById("tableName").deleteRow(tr.length-1)
    }else{
      if(matchFound && tr[tr.length-1].firstChild.innerText.includes("No data found") && !hasError)
        document.getElementById("tableName").deleteRow(tr.length-1)
    }
}

export function sortTable(n, tableName) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById(tableName);
  switching = true;
  dir = "asc"; 
  while (switching) {
    switching = false;
    rows = table.rows;
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      if(rows[i].getElementsByTagName("TD")[n].childNodes[0]!= undefined && rows[i].getElementsByTagName("TD")[n].childNodes[0].tagName === "SELECT"){
        x = rows[i].getElementsByTagName("TD")[n].childNodes[0].selectedOptions[0]
        y = rows[i+1].getElementsByTagName("TD")[n].childNodes[0].selectedOptions[0]
      }else{
        x = rows[i].getElementsByTagName("TD")[n];
        y = rows[i + 1].getElementsByTagName("TD")[n];
      }

      if (dir == "asc") {
        if (x.innerText.toLowerCase() > y.innerText.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }else if (dir == "desc") {
        if (x.innerText.toLowerCase() < y.innerText.toLowerCase()) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if(shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount ++; 
    }else{
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
  if(dir=="asc"){
    rows[0].childNodes[n].classList.add("asc")
    rows[0].childNodes[n].classList.remove("desc")
  }else{
    rows[0].childNodes[n].classList.add("desc")
    rows[0].childNodes[n].classList.remove("asc")
  }
}