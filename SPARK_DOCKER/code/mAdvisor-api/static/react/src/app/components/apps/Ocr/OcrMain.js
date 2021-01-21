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
            <div class="modal fade" id="ocr_Instructions_modal" tabIndex="-1" data-backdrop="static" role="dialog" aria-labelledby="ocr_Instructions_modalTitle" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                  <div id="ocrInstructions" class="carousel slide" data-ride="carousel">
                    <div class="modal-body">
                      <div class="carousel-inner cst_carousel">
                        <div class="item active">
                          <h2>Introduction</h2>
                          <div class="clearfix"></div>
                          <ul class="nav nav-tabs cst-tab-steps">
                            <li class="text-center wow slideInLeft" >
                              <div class="img_block">
                                <img src={STATIC_URL + "assets/images/step11.png"} />
                              </div>
                              <h5>STEP 1</h5>
                              <h3 class="text-primary">Capture</h3>
                            </li>
                            <li class="text-center wow slideInLeft">
                              <div class="img_block">
                                <img src={STATIC_URL + "assets/images/step22.png"} />
                              </div>
                              <h5>STEP 2</h5>
                              <h3 class="text-primary">Classify</h3>

                            </li>
                            <li class="text-center wow bounceInDown">
                              <div class="img_block">
                                <img src={STATIC_URL + "assets/images/step33.png"} />
                              </div>
                              <h5>STEP 3</h5>
                              <h3 class="text-primary">Extract</h3>

                            </li>
                            <li class="text-center wow slideInRight">
                              <div class="img_block">
                                <img src={STATIC_URL + "assets/images/step44.png"} />
                              </div>
                              <h5>STEP 4</h5>
                              <h3 class="text-primary">Validate</h3>

                            </li>
                            <li class="text-center wow slideInRight">
                              <div class="img_block">
                                <img src={STATIC_URL + "assets/images/step55.png"} />
                              </div>
                              <h5>STEP 5</h5>
                              <h3 class="text-primary">Deliver</h3>
                            </li>
                          </ul>
                        </div>
                        <div class="item i_steps">
                          <div class="container-fluid">
                            <div class="row">

                              <div class="col-md-3 text-center wow bounceInDown">
                                <div class="img_block ">
                                  <img src={STATIC_URL + "assets/images/step11.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div class="col-md-9 wow slideInRight">
                                <h5>STEP 1</h5>
                                <h2 class="text-primary">Capture</h2>
                                <p>Uploading the different types of file which needs to be analyzed.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="item i_steps">
                          <div class="container-fluid">
                            <div class="row">

                              <div class="col-md-3 text-center wow bounceInDown">
                                <div class="img_block">
                                  <img src={STATIC_URL + "assets/images/step22.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div class="col-md-9 wow slideInRight">
                                <h5>STEP 2</h5>
                                <h2 class="text-primary">Classify</h2>
                                <p>Classification of the different uploaded files into the definded categories.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="item i_steps">
                          <div class="container-fluid">
                            <div class="row">
                              <div class="col-md-3 text-center wow bounceInDown">
                                <div class="img_block">
                                  <img src={STATIC_URL + "assets/images/step33.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div class="col-md-9 wow slideInRight">
                                <h5>STEP 3</h5>
                                <h2 class="text-primary">Extract</h2>
                                <p>Extraction of the text from the uploaded image using different predefined techniques.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="item i_steps">
                          <div class="container-fluid">
                            <div class="row">
                              <div class="col-md-3 text-center wow bounceInDown">
                                <div class="img_block">
                                  <img src={STATIC_URL + "assets/images/step44.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div class="col-md-9 wow slideInRight">
                                <h5>STEP 4</h5>
                                <h2 class="text-primary">Validate</h2>
                                <p>Validation of the recognized images by the assigned user.</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="item i_steps">
                          <div class="container-fluid">
                            <div class="row">

                              <div class="col-md-3 text-center wow bounceInDown">
                                <div class="img_block">
                                  <img src={STATIC_URL + "assets/images/step55.png"} alt="STEP 1" />
                                </div>
                              </div>
                              <div class="col-md-9 wow slideInRight">
                                <h5>STEP 5</h5>
                                <h2 class="text-primary">Deliver</h2>
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
                      <span class="sr-only">Next</span>
                    </a>
                    </div>
                    <div class="modal-footer">
                      <ol class="carousel-indicators cst_indicators">
                        <li data-target="#ocrInstructions" data-slide-to="0" class="active"></li>
                        <li data-target="#ocrInstructions" data-slide-to="1"></li>
                        <li data-target="#ocrInstructions" data-slide-to="2"></li>
                        <li data-target="#ocrInstructions" data-slide-to="3"></li>
                        <li data-target="#ocrInstructions" data-slide-to="4"></li>
                        <li data-target="#ocrInstructions" data-slide-to="5"></li>
                      </ol>
                      <button type="button" class="btn btn-primary" data-dismiss="modal">SKIP</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            {/* inroduction modal ends*/}
            <div className="row alignCenter xs-pt-0">
              <div className="col-sm-6">
                <h3 class="xs-mt-10">Project Metrics</h3>
              </div>
              <div className="col-sm-6">
                <button style={{ float: 'right' }} type="button" class="btn btn-primary" data-toggle="modal" data-target="#ocr_Instructions_modal">
                  Introduction
              	</button>
              </div>
            </div>

            <div class="row firstRow">
              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.Project.accuracy}`, '--fill': '#ff1888' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.Project.accuracy}% </span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-4"><span class="number">{this.props.dashboardMetrics.projectMetrics.Project.totalProject}</span> <span class="title">Projects</span></div>
                    <div class="col-md-8"><span class="number">60</span> <span class="title">Mins for 100 Images</span></div>

                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.Pages.accuracy}`, '--fill': '#ef27c0' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.Pages.accuracy}% </span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-4"><span class="number">{this.props.dashboardMetrics.projectMetrics.Pages.TotalImages}</span> <span class="title">Page</span></div>
                    <div class="col-md-8"><span class="number">05</span> <span class="title">Mins for 1000 Texts</span></div>

                  </div>
                </div>
              </div>
              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.TotalTexts.accuracy}`, '--fill': '#8458be' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.TotalTexts.accuracy}% </span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-12 text-center">
                      <span class="number">{this.props.dashboardMetrics.projectMetrics.TotalTexts.totalTexts} &nbsp;</span>
                      <span class="title"> Texts Extracted</span></div>

                  </div>
                </div>
              </div>

              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.TypedTexts.accuracy}`, '--fill': '#c1556c' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.TypedTexts.accuracy}% </span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-12 text-center">
                      <span class="number">{this.props.dashboardMetrics.projectMetrics.TypedTexts.typedTexts} &nbsp;</span>
                      <span class="title"> Typed Text Extracted</span></div>

                  </div>
                </div>
              </div>

              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.accuracy}`, '--fill': '#93c155' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.accuracy}% </span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-12 text-center">
                      <span class="number">{this.props.dashboardMetrics.projectMetrics.HandPrintedTexts.handPrintedTexts} &nbsp;</span>
                      <span class="title"> Hand Printed Text Extracted</span></div>

                  </div>
                </div>
              </div>

              <div class="col-md-4">
                <div class="widget widget-pie">
                  <div class="row chart-container">
                    <div class="col-md-12 text-center">
                      <div class="chart" id="widget-top-1" style={{ padding: 0, position: 'relative' }}>
                        <div class="semi-donut margin" style={{ '--percentage': `${this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.accuracy}`, '--fill': '#58beae' }}>
                          <span style={{ color: '#000', fontSize: 16 }}>{this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.accuracy}%</span><br></br>
                          <span style={{ color: '#777', fontSize: 16 }}>Accuracy</span>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="row chart-info">
                    <div class="col-md-12 text-center">
                      <span class="number">{this.props.dashboardMetrics.projectMetrics.HandWrittenTexts.handWrittenTexts} &nbsp;</span>
                    <span class="title"> Hand Written Text Extracted</span></div>

                  </div>
                </div>
              </div>

            </div>
            <h3>Reviewers L1 Metrics</h3>
            <div class="xs-mt-20"></div>
            <div class="row">
              <div class="col-md-3">
                <div class="widget widget-pie">
                  <div class="row chart-info">
                    <div class="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_reviewer.png"} />
                    </div>
          <div class="col-md-8"><span class="number">{this.props.dashboardMetrics.reviewerL1data.totalReviewers}</span><br></br>
                    <span class="title">Reviewers <br></br>&nbsp;</span></div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="widget widget-pie">
                  <div class="row chart-info">
                    <div class="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_docReview.png"} />
                    </div>
                    <div class="col-md-8"><span class="number">{this.props.dashboardMetrics.reviewerL1data.totalReviewedDocs}</span><br></br>
                    <span class="title">Documents <br></br>Reviewed</span></div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="widget widget-pie">
                  <div class="row chart-info">
                    <div class="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_docpendingReview.png"} />
                    </div>
                    <div class="col-md-8"><span class="number">{this.props.dashboardMetrics.reviewerL1data.totalPendingDocs}</span><br></br>
                    <span class="title">Documents <br></br>Pending Review</span></div>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="widget widget-pie">
                  <div class="row chart-info">
                    <div class="col-md-4">
                      <img src={STATIC_URL + "assets/images/icon_reviewersReview.png"} />
                    </div>
                    <div class="col-md-8"><span class="number">{this.props.dashboardMetrics.reviewerL1data.reviewsPerReviewer}</span><br></br>
                    <span class="title">Reviews <br></br>per reviewer</span></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
           :
           <img id="loading" style={{ position: 'relative', paddingTop: 0 }} src={STATIC_URL + "assets/images/Preloader_2.gif"} />
          }
        </section>
		</div>
      </div>
    );
  }

}
