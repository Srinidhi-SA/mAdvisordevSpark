import React from "react";
import {connect} from "react-redux";
import {Modal,Button} from "react-bootstrap";
import store from "../../store";
import {showAudioFUModal,hideAudioFUModal,uploadAudioFileToStore,uploadAudioFile,clearAudioFile,pauseAudioFile,playAudioFile} from "../../actions/appActions";
import Dropzone from 'react-dropzone'

@connect((store) => {
	return {
		audioFileUploadShowFlag:store.apps.audioFileUploadShowFlag,
		audioFileUpload:store.apps.audioFileUpload,
		};
})

export class AudioFileUpload extends React.Component {
	constructor(props) {
		super(props);
		this.onDropAudioFile = this.onDropAudioFile.bind(this);
	}
	showAudioFUPopup(){
		this.props.dispatch(showAudioFUModal());
	}
	closeAudioFUPopup(){
		this.props.dispatch(hideAudioFUModal());
		this.props.dispatch(clearAudioFile());
	}
	onDropAudioFile(files) {
		this.props.dispatch(uploadAudioFileToStore(files))
	}
	showMsg(){
		bootbox.alert("Only WAV files are allowed to upload")
	}
	mediaFileUpload(){
		this.props.dispatch(uploadAudioFile())
	}
	playUploadedFile(){
		playAudioFile();
	}
	pauseUploadedFile(){
		pauseAudioFile();	
	}
	render() {
		var fileName = store.getState().apps.audioFileUpload.name;
        var fileSize = store.getState().apps.audioFileUpload.size;
 
		return (
				<div class="col-md-3 top20 list-boxes" onClick={this.showAudioFUPopup.bind(this)}>
				<div class="newCardStyle firstCard">
				<div class="card-header"></div>
				<div class="card-center newStoryCard">				
				 <h2 class="text-center"><i class="fa fa-file-audio-o fa-2x"></i> Analyse Speech </h2> 				
				</div>
				</div>
				
				<div id="newModel"  role="dialog" className="modal fade modal-colored-header">
				<Modal show={store.getState().apps.audioFileUploadShowFlag} onHide={this.closeAudioFUPopup.bind(this)} dialogClassName="modal-colored-header">
				<Modal.Header closeButton>
				<h3 className="modal-title">Media Upload</h3>
				</Modal.Header>
				<Modal.Body>
					<div className="row">
					<div className="col-xs-9">						
					<div className="form-group xs-ml-40 xs-mt-20">
					<div className="dropzone ">
					<Dropzone id={2} onDrop={this.onDropAudioFile} onDropRejected={this.showMsg} accept=".wav" >
					<p>Please drag and drop your file here or browse.</p>
					</Dropzone>
					<aside>
					<ul className={fileName != undefined ? "list-unstyled bullets_primary":"list-unstyled"}>
					<li>{fileName}{fileName != undefined ? " - ":""}{fileSize}{fileName != undefined ? " bytes ":""}</li>
					</ul>
					</aside>
					</div>
					</div>
					</div>
					<div className="col-xs-3">
					<audio id="myAudio" />
					<div className="xs-pt-50" ><i className="fa fa-play fa-3x cursor xs-p-5" id="audioPlay" onClick={this.playUploadedFile.bind(this)} aria-hidden="true"></i>
					<i className="fa fa-pause fa-3x cursor xs-p-5 hide" id="audioPause" onClick={this.pauseUploadedFile.bind(this)} aria-hidden="true"></i></div>
					</div>
					</div>
					
				</Modal.Body>
				<Modal.Footer>
				<Button className="btn btn-primary md-close" onClick={this.closeAudioFUPopup.bind(this)}>Close</Button>
                <Button bsStyle="primary" onClick={this.mediaFileUpload.bind(this)}>Analyse</Button>
				</Modal.Footer>
				</Modal>
				</div>
				</div>


		)
	}

}	  