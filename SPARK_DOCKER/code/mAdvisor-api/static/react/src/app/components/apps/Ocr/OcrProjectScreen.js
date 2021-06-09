import React from 'react'
import { Link } from "react-router-dom";
import { saveDocumentPageFlag, getOcrProjectsList, selectedProjectDetails, projectPage, projectTablePagesize } from '../../../actions/ocrActions';
import { connect } from "react-redux";
import { OcrCreateProject } from './OcrCreateProject';
import { STATIC_URL } from '../../../helpers/env';
import ReactTooltip from 'react-tooltip';
import { Modal, Button,Pagination } from "react-bootstrap/";
import { API } from "../../../helpers/env";
import { getUserDetailsOrRestart, statusMessages } from "../../../helpers/helper";

@connect((store) => {
   return {
      OcrProjectList: store.ocr.OcrProjectList
   };
})


export class OcrProjectScreen extends React.Component {
   constructor(props) {
      super(props);
      this.state = {
         editProjectFlag: false,
         editProjectName: "",
         editProjectSlug: "",
         deleteProjectSlug: "",
         deleteProjectFlag: false,
         deleteProjectName: "",
      }

   }

   handleDocumentPageFlag = (slug, name) => {
      this.props.dispatch(saveDocumentPageFlag(true));
      this.props.dispatch(selectedProjectDetails(slug, name))
   }
   componentWillMount = () => {    
      this.props.dispatch(getOcrProjectsList())
   }

   handlePagination = (pageNo) => {
      this.props.dispatch(projectPage(pageNo))
      this.props.dispatch(getOcrProjectsList(pageNo))
   }
   handlePageRow=(e)=>{
      this.props.dispatch(projectTablePagesize(e.target.value));
      this.props.dispatch(getOcrProjectsList())
    }
   closePopup = () => {
      this.setState({ editProjectFlag: false })
   }
   closeDeletePopup = () => {
      this.setState({ deleteProjectFlag: false })
   }
   openPopUp = (name, slug) => {
      this.setState({ editProjectName: name, editProjectSlug: slug, editProjectFlag: true })
   }
   openDeletePopUp = (name, slug) => {
      this.setState({ deleteProjectName: name, deleteProjectSlug: slug, deleteProjectFlag: true })
   }
   handleNameChange = (e) => {
      document.getElementById("resetMsg").innerText = "";
      this.setState({ editProjectName: e.target.value });
   }
   getHeader = (token) => {
      return {
         'Authorization': token,
         'Content-Type': 'application/json',
      }
   }

   saveProjectName = () => {
      if (this.state.editProjectName == "") {
         document.getElementById("resetMsg").innerText = "Please enter project name";
         return false;
      }
      return fetch(API + '/ocr/project/' + this.state.editProjectSlug + '/', {
         method: 'put',
         headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
         body: JSON.stringify({ name: this.state.editProjectName })
      }).then(response => response.json())
         .then(data => {
            if (data.edited === true) {
               this.closePopup(),
                  bootbox.alert(statusMessages("success", "Project name changed.", "small_mascot"))
               setTimeout(() => {
                  this.props.dispatch(getOcrProjectsList())
               }, 1000)
            }
            else {
               document.getElementById("resetMsg").innerText = data.exception;
            }
         })
   }
   deleteProject = () => {
      return fetch(API + '/ocr/project/' + this.state.deleteProjectSlug + '/', {
         method: 'put',
         headers: this.getHeader(getUserDetailsOrRestart.get().userToken),
         body: JSON.stringify({ deleted: true })
      }).then(response => response.json())
         .then(data => {
            if (data.message === "Deleted") {
               this.closeDeletePopup(),
                  bootbox.alert(statusMessages("success", "Project deleted.", "small_mascot"))
               this.props.dispatch(getOcrProjectsList())
            }
         })
   }

   render() {
      const pages = this.props.OcrProjectList.total_number_of_pages;
      const current_page = this.props.OcrProjectList.current_page;
      let paginationTag = null
      if (pages >= 1) {
         paginationTag = (
            <div className="col-md-12 text-center">
               <div className="footer" id="Pagination">
                  <div className="pagination pageRow">
                  <span>Rows per page:</span>
                  <select className="xs-mr-20 xs-ml-10" onChange={this.handlePageRow}>
                     <option value="12">12</option>
                     <option value="50">50</option>
                     <option value="100">100</option>
                     <option value="All">All</option>
                  </select>
                  <Pagination ellipsis bsSize="medium" maxButtons={10} onSelect={this.handlePagination} first last next prev boundaryLinks items={pages} activePage={current_page} />
                  </div>
               </div>
            </div>
         )
      }
      var OcrProjectTable = (
         this.props.OcrProjectList != '' ? (this.props.OcrProjectList.data.length != 0 ? this.props.OcrProjectList.data.map((item, index) => {
            return (
               <tr key={index} id={index}>
                  <td>
                     <Link to='/apps/ocr-mq44ewz7bp/project/' onClick={() => this.handleDocumentPageFlag(item.slug,item.name)}>{item.name}</Link>
                  </td>
                  <td>{item.project_overview.workflows}</td>
                  <td>{item.project_overview.completion}%</td>
                  <td>{new Date(item.created_at).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
                  <td>{new Date(item.updated_at).toLocaleString().replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3")}</td>
                  <td><span title="Edit Project Name" style={{ cursor: 'pointer', color: '#ff9900', fontSize: 16 }} className="fa fa-pencil-square-o xs-mr-10" onClick={() => this.openPopUp(item.name, item.slug)}></span>
                     <span title="Delete Project" style={{ cursor: 'pointer', fontSize: 16 }} className="fa fa-trash text-danger xs-mr-5" onClick={() => this.openDeletePopUp(item.name, item.slug)}></span>
                  </td>
               </tr>
            )
         }
         )
            : (<tr><td className='text-center' colSpan={6}>"No data found for your selection"</td></tr>)
         )
     : (<tr><td colSpan={6}><img src={STATIC_URL + "assets/images/Preloader_2.gif"} /></td></tr>)
            )
      return (
         <div>
            <OcrCreateProject />
            <ReactTooltip place="top" type="light" />
            <div className="table-responsive">
               <table className="table table-condensed table-hover cst_table ">
                  <thead>
                     <tr>
                        <th data-tip="Click here to see workflows under the respective project" >Project Name</th>
                        <th>Pages</th>
                        <th>Complete %</th>
                        <th>Created At</th>
                        <th>Last Update</th>
                        <th>Action</th>
                     </tr>
                  </thead>
                  <tbody className="no-border-x">
                     {OcrProjectTable}
                  </tbody>
               </table>
               {paginationTag}
            </div>

            <div id="editProject" role="dialog" className="modal fade modal-colored-header">
               <Modal backdrop="static" show={this.state.editProjectFlag} onHide={this.closePopup} dialogClassName="modal-colored-header">
                  <Modal.Header closeButton>
                     <h3 className="modal-title">Edit Project</h3>
                  </Modal.Header>
                  <Modal.Body>
                     <div className="row">
                        <div className="col-md-12">
                        <div className="form-group">
                              <label for="projectName" className="form-label">Project Name <span className="text-danger">*</span></label>
                              <input className="form-control" id="projectName" type="text" defaultValue={this.state.editProjectName} onChange={this.handleNameChange} />
                        </div>
                     </div>
                     </div>
                  </Modal.Body>
                  <Modal.Footer>
                     <div id="resetMsg"></div>
                     <Button onClick={this.closePopup}> Close</Button>
                     <Button bsStyle="primary" onClick={this.saveProjectName}>Save</Button>
                  </Modal.Footer>
               </Modal>
            </div>

            <div id="deleteProject" role="dialog" className="modal fade modal-colored-header">
               <Modal backdrop="static" show={this.state.deleteProjectFlag} onHide={this.closeDeletePopup} dialogClassName="modal-colored-header">
                  <Modal.Header closeButton>
                     <h3 className="modal-title">Delete Project</h3>
                  </Modal.Header>
                  <Modal.Body style={{ padding: '20px 15px 25px 15px' }}>
                     <div className="row">
                        <div className="col-sm-4">
                           <img style={{ width: '100%' }} src={STATIC_URL + "assets/images/alert_warning.png"} />
                        </div>
                        <div className="col-sm-8">
                           <h4 className="text-warning">Warning !</h4>
                           <div>Are you sure you want to delete {this.state.deleteProjectName} project?</div>
                           <div className="xs-mt-10">
                              <Button bsStyle="primary" onClick={this.deleteProject}>Yes</Button>
                              <Button onClick={this.closeDeletePopup}>No</Button>
                           </div>
                        </div>
                     </div>
                  </Modal.Body>
               </Modal>
            </div>
         </div>
      )
   }
   componentWillUnmount=()=>{
      this.props.dispatch(projectTablePagesize("12"));
   }
}
