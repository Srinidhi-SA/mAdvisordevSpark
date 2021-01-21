export function openBinsOrLevelsModalAction(selectedItem) {
  return {
    type: "BINS_LEVELS_SHOW_MODAL",
    selectedItem
  }
}

export function closeBinsOrLevelsModalAction() {
   return {
     type: "BINS_LEVELS_HIDE_MODAL",
   }
}

export function openTransformColumnModalAction(selectedItem) {
  return {
    type: "TRANSFORM_COLUMN_SHOW_MODAL" ,
    selectedItem
  }
}

export function closeTransformColumnModalAction() {
   return {
     type: "TRANSFORM_COLUMN_HIDE_MODAL",
   }
}

export function selectedBinsOrLevelsTabAction(selectedBinsOrLevelsTab) {
  return {
    type: "BINS_OR_LEVELS",
    selectedBinsOrLevelsTab
  }
}

export function binningOptionsOnChangeAction(isNoOfBinsEnabled,isSpecifyIntervalsEnabled) {
  return {
    type: "NUM_OF_BINS_SPECIFY_INTERVALS",
    isNoOfBinsEnabled,
    isSpecifyIntervalsEnabled
  }
}

export function saveBinLevelTransformationValuesAction(coloumnSlug, actionType, userData){
  return {
    type: "SAVE_BIN_LEVEL_TRANSFORMATION_DATA",
    coloumnSlug,
    userData,
    actionType
  }
}
export function saveTopLevelValuesAction(yesNoValue, numberOfBins){
  return {
    type: "FE_SAVE_TOP_LEVEL_DATA",
    yesNoValue,
    numberOfBins
  }
}
