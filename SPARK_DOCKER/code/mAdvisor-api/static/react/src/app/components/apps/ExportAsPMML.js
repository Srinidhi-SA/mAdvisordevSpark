import React from "react";
import {connect} from "react-redux";
import {Modal,Button} from "react-bootstrap";
import store from "../../store";
import {handleExportAsPMMLModal,updateSelectedAlg} from "../../actions/appActions";
import {getUserDetailsOrRestart} from "../../helpers/helper";
import {API} from "../../helpers/env";

@connect((store) => {
    return {
        algorithmsList:store.apps.algorithmsList,
        exportAsPMMLModal:store.apps.exportAsPMMLModal,
        modelSlug:store.apps. modelSlug,
        selectedAlg:store.apps.selectedAlg,
    };
})

export class ExportAsPMML extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidUpdate(){
      if($("#PMMLalgorithms").val()!=undefined)
        this.props.dispatch(updateSelectedAlg($("#PMMLalgorithms").val()));
    }
    openCloseModal(flag){
        this.props.dispatch(handleExportAsPMMLModal(flag))
    }
    updateAlg(){
        this.props.dispatch(updateSelectedAlg($("#PMMLalgorithms").val()));
    }
    render() {
        let algorithms = store.getState().apps.algorithmsList;
        let algorithmNames = null;

        if(algorithms){
            algorithmNames = <select id="PMMLalgorithms" name="selectbasic" class="form-control" onChange={this.updateAlg.bind(this)}>
            {algorithms.map(algorithm =>
            <option key={algorithm.slug} value={algorithm.slug}>{algorithm.name} {algorithm.accuracy}</option>
            )}
            </select>
        }else{
            algorithmNames = "No Algorithms"
        }
        return (
            <div id="exportAsPMML"  role="dialog" className="modal fade modal-colored-header">
                <Modal show={store.getState().apps.exportAsPMMLModal} onHide={this.openCloseModal.bind(this,false)} dialogClassName="modal-colored-header">
                    <Modal.Header closeButton>
                        <h3 className="modal-title">Export As PMML</h3>
                    </Modal.Header>
                    <Modal.Body>
                        <div class="form-group">
                            <label>Select a Model</label>
                            {algorithmNames}
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button onClick={this.openCloseModal.bind(this,false)}>Close</Button>
                        <a href={API+"/api/get_xml/"+store.getState().apps.modelSlug+"/"+store.getState().apps.selectedAlg+"/?token="+getUserDetailsOrRestart.get().userToken} id="exportAsPMML" className="btn btn-primary" download>Download</a>
                    </Modal.Footer>
                </Modal>
            </div>
        )
    }
}
