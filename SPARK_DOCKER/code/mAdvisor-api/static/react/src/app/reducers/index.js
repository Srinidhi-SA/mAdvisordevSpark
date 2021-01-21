import { combineReducers } from "redux"

import login from "./loginReducers"
import signals from "./signalReducers"

import datasets from "./dataReducers"
import dataUpload from "./dataUploadReducers"
import dataSource from "./dataSourceReducers"
import apps from "./appReducers"
import chartObject from "./chartReducers"
import ocr from "./ocrReducers"
import { loadingBarReducer } from 'react-redux-loading-bar'

export default combineReducers({
  login,
  signals,
  datasets,
  dataUpload,
  dataSource,
  apps,
  chartObject,
  ocr,
  loadingBar: loadingBarReducer,

})
