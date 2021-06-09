//all the ocr related reducers..
export default function reducer(state = {
  OcrfileUpload: "",
  OcrDataList: "",
  OcrProjectList:"",
  OcrReviewerList:"",
  OcrRevwrDocsList:'',
  imageFlag: false,
  originalImgPath: "",
  ocrImgPath:"",
  imageSlug:"",
  ocrS3BucketDetails: {},
  s3Uploaded: false,
  s3Loader: false,
  s3FileList:"",
  s3SelFileList:[],
  s3FileFetchErrorFlag:false,
  s3FileUploadErrorFlag:false,
  s3FileFetchSuccessFlag:false,
  s3FileFetchErrorMsg:"",
  ocrFilesSortType: null,
  ocrFilesSortOn: null,
  documentFlag:false,
  revDocumentFlag:false,
  filter_status: '',
  filter_confidence: '',
  filter_assignee: '',
  filter_fields:'',
  filter_template:'',
  filter_rd_status:'',
  filter_rd_confidence:'',
  filter_rd_fields:'',
  filter_rd_template:'',
  filter_rev_accuracy:'',
  filter_rev_time:'',
  checked_list: '',
  addUserPopupFlag : false,
  createUserFlag : false,
  loaderFlag : false,
  curUserSlug : "",
  newUserDetails : {},
  newUserProfileDetails : {},
  ocrUserProfileFlag : false,
  allOcrUsers : {},
  ocrReviwersList : [],
  appsList : [],
  selectedOcrUsers : [],
  isAllCheckedFlag : false,
  editOcrUserFlag:false,
  selUserSlug:"",
  selUserDetails:{},
  enableEditingFlag:false,
  editedUserDetails : {},
  userTableLoaderFlag : false,
  editUserSuccessFlag : false,
  roleFormSel : false,
  detailsFormSel : false,
  selectedTabId : "none",
  ocrSearchElement : "",
  ocrUserPageNum : 1,
  search_document:'',
  search_project:'',
  search_project_in_revtable:'',
  selected_project_slug:'',
  selected_project_name:'',
  selected_reviewer_slug:'',
  selected_reviewer_name:'',
  selected_image_name:'',
  configureTabSelected : "initialReview",
  iRLoaderFlag : false,
  iRToggleFlag : true,
  iRConfigureDetails : {"active":"","max_docs_per_reviewer":"","selectedIRList":[],"test":""},
  iRList : {},
  iRSearchElem : "",
  sRLoaderFlag : false,
  sRToggleFlag : true,
  sRConfigureDetails : {"active":"","max_docs_per_reviewer":"","selectedSRList":[],"test":""},
  sRList : {},
  sRSearchElem : "",
  configRules : {},
  iRFlag : true,
  sRFlag : true,
  tabActive:'backlog',
  docTaskId: [],
  projectTabLoaderFlag:false,
  dashboardMetrics: {},
  is_closed: "",
  template: [],
  classification: "",
  ocrImgHeight: "",
  ocrImgWidth: "",
  docTablePage: 1,
  projectPage:1,
  docTablePagesize:12,
  rDocTablePagesize:12,
  projectTablePagesize:12,
  userTablePagesize:12,
  reviewerTablePagesize:12,
  userDeleteFlag: false,
  customImgPath: "",
  customImageName:"",
  labelsList:[],
  pdfSize:1,
  pdfNumber:1,
  pdfDoc: false,
  pdfSlug: "",
  hideS3Modal: false

}, action) {
  switch (action.type) {
    case "OCR_UPLOAD_FILE":
      {
        return {
          ...state,
          OcrfileUpload:action.files,
        }
      }
    break;
    case "CLEAR_OCR_UPLOAD_FILES":
    {
      return {
        ...state,
        OcrfileUpload:{},
      }
    }
    break;
    //Projects,Documents,Reviewers Lists//
    case "OCR_PROJECT_LIST":
    {
      return {
        ...state,
        OcrProjectList: action.data
      }
    }
    break;
    case "OCR_PROJECT_LIST_FAIL":
    {
    throw new Error("Unable to fetch projects list!!");
    }
    break;
    case "OCR_UPLOADS_LIST":
    {
      return {
        ...state,
        OcrDataList: action.data
      }
    }
    break;
    case "OCR_UPLOADS_LIST_FAIL":
    {  
    throw new Error("Unable to fetch uploaded images list!!");
    }
    break;
    case "OCR_REV_DOCS_LIST":
    {
      return {
        ...state,
        OcrRevwrDocsList: action.data
      }
    }
    break;
    case "OCR_REV_DOCS_LIST_FAIL":
    {  
    throw new Error("Unable to fetch uploaded images list!!");
    }
    break;
    case "OCR_REVIEWERS_LIST":
    {
      return {
        ...state,
        OcrReviewerList: action.data
      }
    }
    break;
    case "OCR_REVIEWERS_LIST_FAIL":
    {
    throw new Error("Unable to fetch Reviewers list!!");
    }
    break;
     ////
    case "SAVE_DOCUMENT_FLAG":
      {
        return {
          ...state,
          documentFlag: action.flag
        }
      }
      break;
      case "SAVE_REV_DOCUMENT_FLAG":
      {
        return {
          ...state,
          revDocumentFlag: action.flag
        }
      }
      break;
      
    case "SAVE_S3_BUCKET_DETAILS": {
      let curS3Bucket = state.ocrS3BucketDetails;
      curS3Bucket[action.name]= action.val
      return {
        ...state,
        ocrS3BucketDetails : curS3Bucket
      }
    }
    break;
    case "SAVE_S3_FILE_LIST": {
      return {
        ...state,
        s3FileList : action.fileList,
        s3FileFetchErrorFlag : false,
        s3FileFetchSuccessFlag : true,
        s3Loader : false
      }
    }
    break;
    case "CLEAR_S3_DATA": {
      return {
        ...state,
        s3FileList : "",
        s3SelFileList: [],
        s3Loader: false,
        s3Uploaded: false,
        s3FileFetchErrorFlag : false,
        s3FileFetchSuccessFlag : false,
        s3FileFetchErrorMsg : "",
        s3FileUploadErrorFlag : false,
        ocrS3BucketDetails : {}
      }
    }
    break;
    case "SAVE_SEL_S3_FILES": {
      return {
        ...state,
        s3SelFileList : action.fileName
      }
    }
    break;
    case "S3_FILE_ERROR_MSG": {
      return {
        ...state,
        s3FileFetchErrorFlag : action.flag,
        s3Loader : false,
      }
    }
    break;
    case "S3_FETCH_ERROR_MSG": {
      return {
        ...state,
        s3FileFetchErrorMsg : action.msg
      }
    }
    break;
    case "S3_FILE_UPLOAD_ERROR_MSG": {
      return {
        ...state,
        s3Loader : false,
        s3FileUploadErrorFlag : true,
        s3FileFetchErrorMsg : "Failed to upload files, please try again."
      }
    }
    break;
    case "SET_S3_UPLOADED": {
      return {
        ...state,
        s3FileFetchSuccessFlag : false,
        s3Uploaded : action.flag,
        s3FileList: "",
        s3SelFileList:[]
      }
    }
    break;
    case "HIDE_S3_MODAL":{
      return {
        ...state,
        hideS3Modal : action.flag
      }
    }
    break;
    case "SET_S3_LOADER": {
      return {
        ...state,
        s3Loader : action.flag
      }
    }
    break;
    case "SAVE_IMAGE_FLAG":
      {
        return {
          ...state,
          imageFlag: action.flag
        }
      }
    break;
    case "SAVE_IMAGE_DETAILS":
      {
        let close= action.data.tasks === null ? "" : action.data.tasks.is_closed;
        let templateVal = action.data.values === undefined || action.data.values === null ? "" : action.data.values;
        let classificationVal = action.data.classification === undefined || action.data.classification === null  ? "" : action.data.classification;
        return {
          ...state,
          originalImgPath: action.data.imagefile ,
          ocrImgPath: action.data.generated_image,
          customImgPath: action.data.generated_image,
          imageSlug: action.data.slug,
          is_closed: close,
          template: templateVal,
          classification: classificationVal,
          ocrImgHeight: action.data.height,
          ocrImgWidth: action.data.width,
          customImageName: action.data.image_name,
          labelsList: action.data.labels_list,
        }
      }
      break;
      case "PDF_PAGINATION":
        {
        return{
          ... state,
          pdfSize: action.data.total_number_of_pages,
          pdfNumber: action.data.current_page,
          pdfDoc: true,
        }
        }
      break;
      case "SAVE_PDF_SLUG":
        {
          return{
            ...state,
            pdfSlug: action.data,
          }
        }
        case "TASK_ID":
          {
          let taskId = action.data.task_ids === null ? [] : action.data.task_ids;
            return{
            ...state,
            docTaskId: taskId,
            }
          }
      case "CLOSE_FLAG":
        {
          return{
            ...state,
          is_closed: action.data.is_closed,
          }
        }
        break;
        case "SELECTED_TEMPLATE":
          {
            return{
              ...state,
              classification: action.template,
            }
          }
          break;
      case "CLEAR_IMAGE_DETAILS":
        {
          return {
            ...state,
            originalImgPath: "" ,
            ocrImgPath: "",
            imageSlug: "",
            docTaskId: [],
            is_closed:"",
            template: [],
            classification: "",
            pdfDoc: false,
          }
        }
        break;
      case "UPDATE_OCR_IMAGE":
        {
          return {
            ...state,
            ocrImgPath: action.data + "?" +new Date().getTime(),
          }
        }
        break;
        case "UPDATE_CUSTOM_IMAGE":
          {
            return {
              ...state,
              customImgPath: action.data + "?" +new Date().getTime(),
            }
          }
          break;
    case "OCR_FILES_SORT":
      {
        return {
          ...state,
          ocrFilesSortOn: action.ocrFilesSortOn,
          ocrFilesSortType: action.ocrFilesSortType
        }
      }
    break;
    case "FILTER_BY_STATUS":
      {
        return {
          ...state,
          filter_status: action.value,
        }
      }
    break;
    case "FILTER_BY_CONFIDENCE":
      {
        return {
          ...state,
          filter_confidence: action.value,
        }
      }
    break;
    case "FILTER_BY_ASSIGNEE":
      {
        return {
          ...state,
          filter_assignee: action.value
        }
      }
    break;
    
    case "FILTER_BY_TEMPLATE":
    {
      return {
        ...state,
        filter_template: action.value
      }
    }
  break;
    case "FILTER_BY_FIELDS":
      {
        return {
          ...state,
          filter_fields: action.value
        }
      }
    break;
    
    case "RESET_OCR_TABLE_FILTERS":
    {
      return {
        ...state,
        filter_status:'',
        filter_confidence: '',
        filter_assignee:'',
        filter_fields:'',
        filter_template:''
      }
    }
  break;
    // filter for reviewers document table
    case "RESET_RD_FILTER_SEARCH":
    {
      return {
        ...state,
        filter_rd_status: '',
        filter_rd_confidence:'',
        filter_rd_fields:'',
        filter_rd_template:'',
        search_project_in_revtable:''
      }
    }
  break;
  case "UPDATE_FILTER_RD_DETAILS":
   {
        if(action.filterOn=="status"){
          return {
            ...state,
            filter_rd_status: action.value,
          }
        }else if(action.filterOn=='confidence'){
          return {
            ...state,
            filter_rd_confidence: action.value,
          }
        }else if(action.filterOn=='fields'){
          return {
            ...state,
            filter_rd_fields: action.value
          }
        }
        else if(action.filterOn=='template'){
          return {
            ...state,
            filter_rd_template: action.value
          }
        }
    }
    break;
    case "FILTER_REV_BY_ACCURACY":
    {
      return {
        ...state,
        filter_rev_accuracy: action.accuracy,
      }
    }
  break; 
    case "UPDATE_CHECKLIST":
      {
        return {
          ...state,
          checked_list: action.list
        }
      }
      break;
//For Manage Users screen
      case "OPEN_ADD_USER_POPUP": {
        return {
          ...state,
          addUserPopupFlag : true
        }
      }
      break;
      case "CLOSE_ADD_USER_POPUP": {
        return {
          ...state,
          addUserPopupFlag : false,
          newUserDetails : {},
          newUserProfileDetails : {},
          ocrUserProfileFlag : false,
          loaderFlag : false,
          createUserFlag : false,
          curUserSlug : "",
        }
      }
      break;
      case "SET_CREATE_USER_LOADER_FLAG": {
        return {
          ...state,
          loaderFlag : action.flag
        }
      }
      break;
      case "SAVE_NEW_USER_DETAILS": {
        let curUserDetails = state.newUserDetails;
        curUserDetails[action.name] = action.value
        return {
          ...state,
          newUserDetails : curUserDetails
        }
      }
      break;
      case "SAVE_NEW_USER_PROFILE":{
        let curUserStatus = state.newUserProfileDetails;
        curUserStatus[action.name] = action.value
        return {
          ...state,
          newUserProfileDetails : curUserStatus
        }
      }
      break;
      case "CREATE_NEW_USER_SUCCESS":{
        return {
          ...state,
          createUserFlag : action.flag,
          curUserSlug : action.slug,
        }
      }
      break;
      case "USER_PROFILE_CREATED_SUCCESS":{
        return {
          ...state,
          ocrUserProfileFlag : action.flag,
          createUserFlag : false
        }
      }
      break;
      case "SAVE_ALL_OCR_USERS_LIST":{
        return {
          ...state,
          allOcrUsers : action.json,
          selectedOcrUsers : [],
          isAllCheckedFlag : false
        }
      }
      break;
      case "SAVE_SELECTED_USERS_LIST":{
        return {
          ...state,
          selectedOcrUsers : action.curSelList
        }
      }
      break;
      case "SELECT_ALL_USERS":{
        return {
          ...state,
          isAllCheckedFlag : action.flag
        }
      }
      break;
      case "SAVE_REVIEWERS_LIST":{
        return {
          ...state,
          ocrReviwersList : action.json
        }
      }
      case "SAVE_APPS_LIST":{
        return {
          ...state,
          appsList : action.data
        }
      }
      case "OPEN_EDIT_USER_POPUP":{
        return{
          ...state,
          editOcrUserFlag : action.flag,
          selUserSlug : action.userSlug,
          selUserDetails : action.userDt,
          editedUserDetails : action.edtDet
        }
      }
      break;
      case "CLOSE_EDIT_USER_POPUP":{
        return{
          ...state,
          editOcrUserFlag : action.flag,
          selUserSlug : "",
          selUserDetails : {},
          editedUserDetails : {},
          detailsFormSel : false,
          roleFormSel : false,
          editUserSuccessFlag : false,
          loaderFlag : false,
        }
      }
      break;
      case "ENABLE_EDITING_USER": {
        return{
          ...state,
          enableEditingFlag : action.flag
        }
      }
      break;
      case "SAVE_EDITED_USER_DETAILS": {
        let curEditedUserStatus = state.editedUserDetails;
        curEditedUserStatus[action.name] = action.val
        return {
          ...state,
          editedUserDetails : curEditedUserStatus
        }
      }
      break;
      case "CLEAR_USER_FLAG":
      {
        return{
          ...state,
          selectedOcrUsers : [],
        }
      }
      break;
      case "SET_USER_TABLE_LOADER_FLAG":{
        return {
          ...state,
          userTableLoaderFlag : action.flag
        }
      }
      break;
      case "SET_PROJECT_TAB_LOADER_FLAG":{
        return {
          ...state,
          projectTabLoaderFlag : action.flag
        }
      }
      break;
      case "EDIT_USER_SUCCESS":{
        return {
          ...state,
          editUserSuccessFlag : action.flag,
        }
      }
      break;
      case "FORM_DETAILS_SELECTED":{
        return {
          ...state,
        detailsFormSel : action.flag
        }
      }
      break;
      case "FORM_ROLES_SELECTED":{
        return {
          ...state,
        roleFormSel : action.flag
        }
      }
      break;
      case "SELECTED_TAB_ID":{
        return {
          ...state,
          selectedTabId : action.id
        }
      }
      break;
      case "OCR_USER_SEARCH_ELEMENT":{
        return {
          ...state,
          ocrSearchElement : action.val
        }
      }
      break;
      case "OCR_USER_PAGE_NUM":{
        return {
          ...state,
          ocrUserPageNum : action.val
        }
      }
      break;
      case "CLEAR_USER_SEARCH_ELEMENT":{
        return {
          ...state,
          ocrSearchElement : ""
        }
      }
      break;
      case "SEARCH_OCR_DOCUMENT":
      {
        return {
          ...state,
          search_document:action.elem
        }
      }
      break;
      case "SEARCH_OCR_PROJECT":
      {
        return {
          ...state,
          search_project:action.elem
        }
      }
      break;
      case "SEARCH_OCR_PROJECT_IN_REV":
      {
        return {
          ...state,
          search_project_in_revtable:action.elem
        }
      }
      break;
      
       case "TAB_ACTIVE_VALUE":
      {
        return {
          ...state,
          tabActive:action.elem
        }
      }
      break;
      case "SELECTED_PROJECT_SLUG":
      {
        return {
          ...state,
          selected_project_slug:action.slug,
          selected_project_name:action.name

        }
      }
      break;
      case "SELECTED_REVIEWER_DETAILS":
      {
        return {
          ...state,
          selected_reviewer_slug:action.slug,
          selected_reviewer_name:action.name
        }
      }
      break;
      
      case "SELECTED_IMAGE_NAME":
      {
        return {
          ...state,
          selected_image_name:action.name
        }
      }
      break;
    //Configure Tab
    case "SAVE_SEL_CONFIGURE_TAB":
      {
        return {
          ...state,
          configureTabSelected : action.selTab
        }
      }
      break;
      case "SET_IR_LOADER_FLAG":
      {
        return {
          ...state,
          iRLoaderFlag : action.flag
        }
      }
      break;
      case "SAVE_IR_LIST":
      {
        return {
          ...state,
          iRList : action.data.allUsersList
        }
      }
      break;
      case "STORE_IR_TOGGLE_FLAG":
      {
        return{
          ...state,
          iRToggleFlag : action.val,
        }
      }
      break;
      case "SAVE_IR_DATA":{
        let curIRDetails = state.iRConfigureDetails
        curIRDetails[action.name] = action.value
        return{
          ...state,
          iRConfigureDetails : curIRDetails
        }
      }
      break;
      case "STORE_IR_SEARCH_ELEMENT" :
      {
        return {
          ...state,
          iRSearchElem : action.val
        }
      }
      break;
      case "SET_SR_LOADER_FLAG":
      {
        return {
          ...state,
          sRLoaderFlag : action.flag
        }
      }
      break;
      case "SAVE_SR_LIST":
      {
        return {
          ...state,
          sRList : action.data.allUsersList
        }
      }
      break;
      case "STORE_SR_TOGGLE_FLAG":
      {
        return{
          ...state,
          sRToggleFlag : action.val,
        }
      }
      break;
      case "STORE_SR_SEARCH_ELEMENT" :
      {
        return {
          ...state,
          sRSearchElem : action.val
        }
      }
      break;
      case "SAVE_SR_DATA":{
        let curSRDetails = state.sRConfigureDetails
        curSRDetails[action.name] = action.value
        return{
          ...state,
          sRConfigureDetails : curSRDetails
        }
      }
      break;

      case "CLEAR_REVIEWER_CONFIG":
      {
        return {
          ...state,
          iRToggleFlag : state.iRFlag,
          sRToggleFlag : state.sRFlag,
          configRules : {},
          iRConfigureDetails : {"active":"","max_docs_per_reviewer":"","selectedIRList":[],"test":""},
          sRConfigureDetails : {"active":"","max_docs_per_reviewer":"","selectedSRList":[],"test":""},
          iRSearchElem : "",
          sRSearchElem : ""
        }
      } 
      break;
      case "SAVE_RULES_FOR_CONFIGURE":
      {
        let data1 = action.data.rulesL1
        let irRules = {}
        let iFlag = action.data.auto_assignmentL1
        if(Object.keys(data1).length === 0){
          irRules = {"active":"","max_docs_per_reviewer":"","selectedIRList":[],"test":""}
        }else if(data1.auto.active === "True"){
          irRules = {"active":"all","max_docs_per_reviewer":data1.auto.max_docs_per_reviewer,"selectedIRList":[],"test":data1.auto.remainaingDocsDistributionRule}
        }else if(data1.custom.active === "True"){
          irRules = {"active":"select","max_docs_per_reviewer":data1.custom.max_docs_per_reviewer,"selectedIRList":data1.custom.selected_reviewers,"test":data1.custom.remainaingDocsDistributionRule}
        }
        let data2 = action.data.rulesL2
        let srRules = {}
        let sFlag = action.data.auto_assignmentL2
        if(Object.keys(data2).length === 0){
          srRules = {"active":"","max_docs_per_reviewer":"","selectedSRList":[],"test":""}
        }else if(data2.auto.active === "True"){
          srRules = {"active":"all","max_docs_per_reviewer":data2.auto.max_docs_per_reviewer,"selectedSRList":[],"test":data2.auto.remainaingDocsDistributionRule}
        }else if(data2.custom.active === "True"){
          srRules = {"active":"select","max_docs_per_reviewer":data2.custom.max_docs_per_reviewer,"selectedSRList":data2.custom.selected_reviewers,"test":data2.custom.remainaingDocsDistributionRule}
        }
        return {
          ...state,
          iRFlag : action.data.auto_assignmentL1,
          sRFlag : action.data.auto_assignmentL2,
          configRules : {"iRRule":action.data.rulesL1,"sRRule":action.data.rulesL2},
          iRConfigureDetails : irRules,
          sRConfigureDetails : srRules,
          iRToggleFlag : iFlag,
          sRToggleFlag : sFlag,
        }
      }
      break;
      case "DASHBOARD_METRICS" :
        {
          return {
            ...state,
            dashboardMetrics : action.data
          }
        }
        break;
      case "DOC_TABLE_PAGE" :
        {
          return {
            ...state,
            docTablePage : action.page
          }
        }
        break;
        case "DOC_TABLE_PAGESIZE" :
          {
            return {
              ...state,
              docTablePagesize : action.pagesize
            }
          }
          break;
          case "RDOC_TABLE_PAGESIZE" :
            {
              return {
                ...state,
                rDocTablePagesize : action.pagesize
              }
            }
            break;
          case "PROJECT_TABLE_PAGESIZE" :
            {
              return {
                ...state,
                projectTablePagesize : action.pagesize
              }
            }
            break;
            case "USER_TABLE_PAGESIZE" :
              {
                return {
                  ...state,
                  userTablePagesize : action.pagesize
                }
              }
              break;
              case "REVIEWER_TABLE_PAGESIZE" :
                {
                  return {
                    ...state,
                    reviewerTablePagesize : action.pagesize
                  }
                }
                break;
        case "PROJECT_PAGE" :
          {
            return {
              ...state,
              projectPage : action.page
            }
          }
          break;
          case "USER_DELETE_FLAG": {
            return {
              ...state,
              userDeleteFlag : action.flag
            }
          }
          break;
}
  return state
}
