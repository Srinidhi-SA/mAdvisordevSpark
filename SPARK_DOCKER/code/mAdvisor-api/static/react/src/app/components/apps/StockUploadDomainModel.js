import React from "react";
import {connect} from "react-redux";
import { Modal,Button,OverlayTrigger,Popover } from "react-bootstrap";
import store from "../../store";
import {STATIC_URL} from "../../helpers/env";
import {capitalizeArray} from "../../helpers/helper.js";
import {updateUploadStockPopup,uploadStockFiles,uploadStockFile} from "../../actions/appActions";

@connect((store) => {
  return {
		 			stockUploadDomainModal: store.apps.stockUploadDomainModal,
					stockUploadDomainFiles: store.apps.stockUploadDomainFiles,
					conceptList: store.apps.conceptList,
					stockSlug:store.apps.stockSlug,};
})

export class StockUploadDomainModel extends React.Component {

  constructor(props) {
    super(props);
  }

  updateUploadStockPopup(flag) {
    this.props.dispatch(updateUploadStockPopup(flag))
  }
  
	triggerStockAnalysis(){
			this.props.dispatch(uploadStockFile(store.getState().apps.stockSlug))
		}

  render() {
    var fileName = "";
    var fileSize = "";
    if (this.props.stockUploadDomainFiles[0]) {
      fileName = this.props.stockUploadDomainFiles[0].name;
      fileSize = this.props.stockUploadDomainFiles[0].size;
    }
    let conceptRs = this.props.conceptList;
    let concepts = Object.keys(conceptRs);
    var imgLink = STATIC_URL + "assets/images/m_carIcon.png";
    const conceptList = concepts.map((concept, i) => {
      let subconcepts = capitalizeArray(conceptRs[concept]);
      subconcepts = subconcepts.join(", ");
      return (
        <div className="col-md-4  top20 " key={i}>
          <div className="rep_block border-box" name={concept}>
            <div className="card-header"></div>
            <div className="card-center-tile">
              <div className="row">
                
                
                <div className="col-xs-8">
                  <h5 className="title newCardTitle pull-left">
                    {concept}
                  </h5>
                  </div>
                  <div className="col-xs-4">
                     <div class="card_icon">
                      <img src={imgLink} alt="LOADING"/>
                    </div>
                  </div>
                  <div className="clearfix"></div>
                  <div className="col-xs-12">
                  <OverlayTrigger trigger="click" rootClose placement="right" overlay={< Popover id = "popover-trigger-focus" > <h4>Sub-Concepts:</h4><br/><p>{subconcepts}</p> </Popover>}>
                    <a>
                    View Sub-Concepts
                   
                    </a>
                  </OverlayTrigger>
                  
                </div>


              </div>
            </div>
            
          </div>
        <div className="clearfix"></div>
        </div>
        
      )
    });

    return (
      <div id="uploadDomainModel" role="dialog" className="modal fade modal-colored-header">
        <Modal show={store.getState().apps.stockUploadDomainModal} onHide={this.updateUploadStockPopup.bind(this, false)} dialogClassName="modal-colored-header modal-lg uploadData">
          <Modal.Header closeButton>
            <h3 className="modal-title">Concepts - Stock Performance Analysis</h3>
          </Modal.Header>
          <Modal.Body>
            <div className="xs-p-20">
             
                  <div className="xs-pt-20"></div>
                    {conceptList}
                </div>
             <div className="clearfix"></div>
          </Modal.Body>
          <Modal.Footer>
            <Button bsStyle="primary" onClick={this.triggerStockAnalysis.bind(this,false)}>Analyse</Button>
          </Modal.Footer>
        </Modal>
      </div>
    )
  }
}
