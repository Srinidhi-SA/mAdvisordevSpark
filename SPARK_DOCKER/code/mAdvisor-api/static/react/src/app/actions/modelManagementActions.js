export function openDeployModalAction(selectedItem) {
  return {
    type: "DEPLOY_SHOW_MODAL" ,
    selectedItem
  }
}

export function closeDeployModalAction() {
   return {
     type: "DEPLOY_HIDE_MODAL",
   }
}

export function storeAlgoSearchElement(search_element) {
  return {type: "SEARCH_ALGORITHM", search_element}
}

export function saveDeployValueAction(colSlug,dataToSave){
  return {
    type: "SAVE_DEPLOY_DATA",
    colSlug,
    dataToSave
  }
}
export function closeViewModalAction() {
   return {
     type: "HIDE_VIEW_MODAL",
   }
}
