import React from "react";
import { connect } from "react-redux";
import { OcrTopNavigation } from "./ocrTopNavigation";
import { STATIC_URL } from "../../../helpers/env";
@connect((store) => {
  return {
    login_response: store.login.login_response,
    dashboardMetrics: store.ocr.dashboardMetrics,
  };
})

export class OcrMain extends React.Component {
  constructor(props) {
    super(props);

  }

  render() {
    return (
      <div className="side-body">
        <OcrTopNavigation />
		<div className="main-content">
      
        <section class="ocr_section box-shadow">
          {Object.keys(this.props.dashboardMetrics).length != 0?
          <div class="container-fluid">
            {/* inroduction modal starts*/}
            <div className="modal fade" id="ocr_Instructions_modal" tabIndex="-1" data-backdrop="static" role="dialog" aria-labelledby="ocr_Instructions_modalTitle" aria-hidden="true">
              <div className="modal-dialog modal-dialog-centered" role="document">
                <div className="modal-content">
                  <div id="ocrInstructions" className="carousel slide" data-ride="carousel">
                    <div className="modal-body">
                      <div className="carousel-inner cst_carousel">
                        <div className="item active">
                          <h2>Introduction</h2>
                          <div className="clearfix"></div>
                          <ul className="nav nav-tabs cst-tab-steps">
                            <li className="text-center wow slideInLeft" >
                              <div className="img_block">
                                <img src={STATIC_URL + "assets/images/step11.png"} />
                              </div>
                              <h5>STEP 1</h5>
                              <h3 className="text-primary">Capture</h3>
                            </li>
                            <li class="text-center wow slideInLeft">
                              <div className="img_block">
                                <img src={STATIC_URL + "assets/images/step22.png"} />
                              </div>
                              <h5>STEP 2</h5>
                              <h3 className="text-primary">Classify</h3>

                            </li>
                            <li className="text-center wow bounceInDown">
                              <div className="img_block">
                                <img src={STATIC_URL + "assets/images/step33.png"} />
                              </div>
                              <h5>STEP 3</h5>
                              <h3 className="text-primary">Extract</h3>

                            </li>
                            <li className="text-center wow slideInRight">
                              <div className="img_block">
                                <img src={STATIC_URL + "assets/images/step44.png"} />
                              </div>
                              <h5>STEP 4</h5>
                              <h3 className="text-primary">Validate</h3>

                            </li>
                            <li className="text-center wow slideInRight">
                              <div className="img_block">
                                <img src={STATIC_URL + "assets/images/step55.png"} />
                              </div>
                              <h5>STEP 5</h5>
                              <h3 className="text-primary">Deliver</h3>
                            </li>
                          </ul>
                        </div>
                        <div className="item i_steps">
                          <div className="container-fluid">
                            <div className="row">

                              <div className="col-md-3 text-center wow bounceInDown">
                                <div className="img_block ">
                                  <img src={STATIC_URL + "assets/images/step11.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div className="col-md-9 wow slideInRight">
                                <h5>STEP 1</h5>
                                <h2 className="text-primary">Capture</h2>
                                <p>Uploading the different types of file which needs to be analyzed.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="item i_steps">
                          <div className="container-fluid">
                            <div className="row">

                              <div className="col-md-3 text-center wow bounceInDown">
                                <div className="img_block">
                                  <img src={STATIC_URL + "assets/images/step22.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div className="col-md-9 wow slideInRight">
                                <h5>STEP 2</h5>
                                <h2 className="text-primary">Classify</h2>
                                <p>Classification of the different uploaded files into the definded categories.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="item i_steps">
                          <div className="container-fluid">
                            <div className="row">
                              <div className="col-md-3 text-center wow bounceInDown">
                                <div className="img_block">
                                  <img src={STATIC_URL + "assets/images/step33.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div className="col-md-9 wow slideInRight">
                                <h5>STEP 3</h5>
                                <h2 className="text-primary">Extract</h2>
                                <p>Extraction of the text from the uploaded image using different predefined techniques.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="item i_steps">
                          <div className="container-fluid">
                            <div className="row">
                              <div className="col-md-3 text-center wow bounceInDown">
                                <div className="img_block">
                                  <img src={STATIC_URL + "assets/images/step44.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div className="col-md-9 wow slideInRight">
                                <h5>STEP 4</h5>
                                <h2 className="text-primary">Validate</h2>
                                <p>Validation of the recognized images by the assigned user.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="item i_steps">
                          <div className="container-fluid">
                            <div className="row">

                              <div className="col-md-3 text-center wow bounceInDown">
                                <div className="img_block">
                                  <img src={STATIC_URL + "assets/images/step55.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div className="col-md-9 wow slideInRight">
                                <h5>STEP 5</h5>
                                <h2 className="text-primary">Deliver</h2>
                                <p>Submitting the validated documnets.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <a className="left carousel-control" href="#ocrInstructions" data-slide="prev" style={{left:-30}}>
                      <span className="glyphicon glyphicon-chevron-left" style={{fontSize:21}}></span>
                      <span className="sr-only">Previous</span>
                    </a>
                    <a className="right carousel-control" href="#ocrInstructions" data-slide="next" style={{right:-30}}>
                      <span className="glyphicon glyphicon-chevron-right" style={{fontSize:21}}></span>
                      <span className="sr-only">Next</span>
                    </a>
                    </div>
                    <div className="modal-footer">
                      <ol className="carousel-indicators cst_indicators">
                        <li data-target="#ocrInstructions" data-slide-to="0" className="active"></li>
                        <li data-target="#ocrInstructions" data-slide-to="1"></li>
                        <li data-target="#ocrInstructions" data-slide-to="2"></li>
                        <li data-target="#ocrInstructions" data-slide-to="3"></li>
                        <li data-target="#ocrInstructions" data-slide-to="4"></li>
                        <li data-target="#ocrInstructions" data-slide-to="5"></li>
                      </ol>
                      <button type="button" className="btn btn-primary" data-dismiss="modal">SKIP</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {/* inroduction modal ends*/}
            <div className="row alignCenter xs-pt-0">
              <div className="col-sm-6">
                <h3 className="xs-mt-10">Project Metrics</h3>
              </div>
              <div className="col-sm-6">
                <button style={{ float: 'right' }} type="button" className="btn btn-primary" data-toggle="modal" data-target="#ocr_Instructions_modal">
                  Introduction
              	</button>
              </div>
            </div>

            <div className="row firstRow">
              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.Project.accuracy}`, '--fill': '#ff1888' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.Project.accuracy}% </span><br></br>
                          <span className="dashboard_acc" >Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-4"><span className="number">{this.props.dashboardMetrics.projectMetrics.Project.totalProject}</span> <span className="title">Projects</span></div>
                    <div className="col-md-8"><span className="number">60</span> <span className="title">Mins for 100 Images</span></div>

                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.Pages.accuracy}`, '--fill': '#ef27c0' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.Pages.accuracy}% </span><br></br>
                          <span className="dashboard_acc">Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-4"><span className="number">{this.props.dashboardMetrics.projectMetrics.Pages.TotalImages}</span> <span className="title">Page</span></div>
                    <div className="col-md-8"><span className="number">05</span> <span className="title">Mins for 1000 Texts</span></div>

                  </div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.TotalTexts.accuracy}`, '--fill': '#8458be' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.TotalTexts.accuracy}% </span><br></br>
                          <span className="dashboard_acc">Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-12 text-center">
                      <span className="number">{this.props.dashboardMetrics.projectMetrics.TotalTexts.totalTexts} &nbsp;</span>
                      <span className="title"> Texts Extracted</span></div>

                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.TypedTexts.accuracy}`, '--fill': '#c1556c' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.TypedTexts.accuracy}% </span><br></br>
                          <span className="dashboard_acc">Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-12 text-center">
                      <span className="number">{this.props.dashboardMetrics.projectMetrics.TypedTexts.typedTexts} &nbsp;</span>
                      <span className="title"> Typed Text Extracted</span></div>

                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.accuracy}`, '--fill': '#93c155' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.accuracy}% </span><br></br>
                          <span className="dashboard_acc">Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-12 text-center">
                      <span className="number">{this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.handPrintedTexts} &nbsp;</span>
                      <span className="title"> Hand Printed Text Extracted</span></div>

                  </div>
                </div>
              </div>

              <div className="col-md-4">
                <div className="widget widget-pie">
                  <div className="row chart-container">
                    <div className="col-md-12 text-center">
                      <div className="chart" id="widget-top-1">
                        <div className="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.accuracy}`, '--fill': '#58beae' }}>
                          <span className="dashboard_percnt">{this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.accuracy}%</span><br></br>
                          <span className="dashboard_acc">Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div className="row chart-info">
                    <div className="col-md-12 text-center">
                      <span className="number">{this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.handWrittenTexts} &nbsp;</span>
                    <span className="title"> Hand Written Text Extracted</span></div>

                  </div>
                </div>
              </div>

            </div>
            <h3>Reviewers L1 Metrics</h3>
            <div className="xs-mt-20"></div>
            <div className="row">
              <div className="col-md-3">
                <div className="widget widget-pie">
                  <div className="row chart-info">
                    <div className="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_reviewer.png"} />
                    </div>
          <div className="col-md-8"><span className="number">{this.props.dashboardMetrics.reviewerL1data.totalReviewers}</span><br></br>
                    <span className="title">Reviewers <br></br>&nbsp;</span></div>
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="widget widget-pie">
                  <div className="row chart-info">
                    <div className="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_docReview.png"} />
                    </div>
                    <div className="col-md-8"><span className="number">{this.props.dashboardMetrics.reviewerL1data.totalReviewedDocs}</span><br></br>
                    <span className="title">Documents <br></br>Reviewed</span></div>
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="widget widget-pie">
                  <div className="row chart-info">
                    <div className="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_docpendingReview.png"} />
                    </div>
                    <div className="col-md-8"><span className="number">{this.props.dashboardMetrics.reviewerL1data.totalPendingDocs}</span><br></br>
                    <span className="title">Documents <br></br>Pending Review</span></div>
                  </div>
                </div>
              </div>
              <div className="col-md-3">
                <div className="widget widget-pie">
                  <div className="row chart-info">
                    <div className="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_reviewersReview.png"} />
                    </div>
                    <div className="col-md-8"><span className="number">{this.props.dashboardMetrics.reviewerL1data.reviewsPerReviewer}</span><br></br>
                    <span className="title">Reviews <br></br>per reviewer</span></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
           :
           <img id="loading" className="xs-pt-0" style={{ position: 'relative'}} src={STATIC_URL + "assets/images/Preloader_2.gif"} />
          }
        </section>
		</div>
      </div>
    );
  }

}
