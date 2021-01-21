import React from "react";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";
import {STATIC_URL} from "../../helpers/env.js"

export class SignalAnalysisPage extends React.Component {
  constructor(){
    super();
  }
  render() {
    return(
      <div className="main_wrapper">

        {/*<!-- Header Menu -->*/}
        <nav className="navbar navbar-default navbar-fixed-top" role="navigation">
{        /* <!-- Brand and toggle get grouped for better mobile display -->*/}          <div className="navbar-header">
            <div className="brand-wrapper">
{             /* <!-- Hamburger -->*/}
            <button type="button" className="navbar-toggle"> <span className="sr-only">Toggle navigation</span> <span className="icon-bar"></span> <span className="icon-bar"></span> <span className="icon-bar"></span> </button>

              {/*<!-- Brand -->*/}
              <div className="brand-name-wrapper"> <a className="navbar-brand" href="#"></a> </div>
            </div>
          </div>
          <div className="dropdown ma-user-nav"> <a className="dropdown-toggle" href="#" data-toggle="dropdown"> <i className="avatar-img img-circle">M</i> <img src="/assets/images/avatar.jpg" alt="M" className="avatar-img img-circle hide"/><span className="user-name">Marlabs BI</span> <span className="caret"></span></a>
            <ul className="dropdown-menu dropdown-menu-right">
              <li><a href="#">Profile</a></li>
              <li><a href="#">Logout</a></li>
            </ul>
          </div>
          <div className="clearfix"></div>
        </nav>
        {/*<!--/.Header Menu -->

        <!-- Side bar Main Menu -->*/}
        <div className="side-menu">
          <div className="side-menu-container">
            <ul className="nav navbar-nav">
              <li><a href="#" className="sdb_signal"> <span></span> SIGNAL</a></li>
              <li className="active"><a href="#" className="sdb_story"> <span></span> STORY</a></li>
              <li><a href="#" className="sdb_app"> <span></span> APPS</a></li>
              <li><a href="#" className="sdb_data"> <span></span> DATA</a></li>
              <li><a href="#" className="sdb_settings"> <span></span> SETTINGS</a></li>
            </ul>
          </div>
        {  /*<!-- /.Side bar Main Menu  -->*/}
        </div>
        {/*<!-- ./Side bar Main Menu -->

        <!-- Main Content starts with side-body -->*/}
        <div className="side-body">

          {/*<!-- Page Title and Breadcrumbs -->*/
          <div className="page-head">
            <div className="row">
              <div className="col-md-8">
                <ol className="breadcrumb">
                  <li><a href="dashboard.html">Story</a></li>
                  <li><a href="story.html">Sales Performance Report</a></li>
                  <li className="active">Overview</li>
                </ol>
              </div>
              <div className="col-md-4">
                <div className="input-group pull-right">
                  <input type="text" name="search_global" title="Search Global" id="search_global" className="form-control" placeholder="Search..."/>
                  <span className="input-group-addon"><i className="fa fa-search fa-lg"></i></span></div>
              </div>
            </div>
            <div className="clearfix"></div>
          </div>
          {/*<!-- /.Page Title and Breadcrumbs -->

          <!-- Page Content Area -->*/}
          <div className="main-content">

          { /* <!-- Copy from here -->*/}

            <div className="row">
              <div className="col-md-12">
                <div className="panel panel-mAd">
                  <div className="panel-heading">
                    <h2 className="pull-left">Sales Performance Report</h2>
                    <div className="btn-toolbar pull-right">
                      <div className="btn-group btn-space">
                        <button type="button" className="btn btn-default"  title="Card mode"><i class="zmdi zmdi-hc-lg zmdi-view-carousel"></i></button>
                        <button type="button" className="btn btn-default" title="Document mode"><i class="zmdi zmdi-hc-lg zmdi-view-web"></i></button>
                        <button type="button" className="btn btn-default"><i class="zmdi zmdi-hc-lg zmdi-close"></i></button>
                      </div>
                    </div>
                    <div className="clearfix"></div>
                  </div>
                  <div className="panel-body no-border">
                    <div className="card full-width-tabs">
                      <ul className="nav nav-tabs" id="guide-tabs" role="tablist">
                        <li className="active"><a href="#overview" aria-controls="overview" role="tab" data-toggle="tab"><i className="mAd_icons tab_overview"></i><span>Overview</span></a></li>
                        <li><a href="#trend" aria-controls="trend" role="tab" data-toggle="tab"><i className="mAd_icons tab_trend"></i><span>Trend</span></a></li>
                        <li><a href="#performance" aria-controls="performance" role="tab" data-toggle="tab"><i className="mAd_icons tab_performance"></i><span>Performance</span></a></li>
                        <li><a href="#influences" aria-controls="influences" role="tab" data-toggle="tab"><i className="mAd_icons tab_influences"></i><span>Influences</span></a></li>
                        <li><a href="#predictions" aria-controls="predictions" role="tab" data-toggle="tab"><i className="mAd_icons tab_predictions"></i><span>Predictions</span></a></li>
                      </ul>

                      {/*<!-- Tab panes -->*/}
                      <div className="tab-content">
                        <div role="tabpanel" className="tab-pane active" id="overview">
      					<div className="content_scroll">
                          <h4 className="text-primary">Executive Summary</h4>
                          <div className="row">
                            <div className="col-md-4">
                              <div className="panel">
                                <div className="panel-heading summary_heading">
                                  <div className="btn-toolbar pull-right">
                                    <div className="btn-group btn-space">
                                      <button type="button" className="btn btn-default" data-target="#detail_view" data-toggle="modal"><i className="fa fa-search-plus"></i></button>
                                    </div>
                                  </div>
                                  <span className="title">Phenomenal growth during Jan-Dec - 2014</span> </div>
                                <div className="panel-body">
                                  <div className="grp_height"> <img src={ STATIC_URL + "assets/images/grp1.jpg"} alt="grp 1" className="img-responsive"/> </div>
                                  <div className="grp_legends grp_legends_green">
                                    <div className="grp_legend_label">
                                      <h3> 32% <small>Strong Growth</small> </h3>
                                    </div>
                                    <div className="grp_legend_label">
                                      <h3> $128K <small>Total Sales</small> </h3>
                                    </div>
                                    <div className="grp_more"> <a href="#"><span className="fa fa-ellipsis-h fa-2x"></span></a> </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div className="col-md-4">
                              <div className="panel">
                                <div className="panel-heading summary_heading">
                                  <div className="btn-toolbar pull-right">
                                    <div className="btn-group btn-space">
                                      <button type="button" className="btn btn-default"><i className="fa fa-search-plus"></i></button>
                                    </div>
                                  </div>
                                  <span className="title">Moderate Decline - Mar to June 2014</span> </div>
                                <div className="panel-body">
                                  <div className="grp_height"> <img src={ STATIC_URL + "assets/images/grp2.jpg" } alt="grp 2" className="img-responsive"/> </div>
                                  <div className="grp_legends grp_legends_red">
                                    <div className="grp_legend_label">
                                      <h3> 9% <small>Decline</small> </h3>
                                    </div>
                                    <div className="grp_legend_label">
                                      <h3> $170k <small>March to June </small> </h3>
                                    </div>
                                    <div className="grp_more"> <a href="#"><span className="fa fa-ellipsis-h fa-2x"></span></a> </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div className="col-md-4">
                              <div className="panel">
                                <div className="panel-heading summary_heading">
                                  <div className="btn-toolbar pull-right">
                                    <div className="btn-group btn-space">
                                      <button type="button" className="btn btn-default"><i className="fa fa-search-plus"></i></button>
                                    </div>
                                  </div>
                                  <span className="title">Variance in sales</span> </div>
                                <div className="panel-body">
                                  <div className="grp_height"> <img src={ STATIC_URL + "assets/images/grp3.jpg"} alt="grp 3" className="img-responsive"/> </div>
                                  <div className="grp_legends grp_legends_primary">
                                    <div className="grp_legend_label">
                                      <h3> 6% <small>Average Sale</small> </h3>
                                    </div>
                                    <div className="grp_more"> <a href="#"><span className="fa fa-ellipsis-h fa-2x"></span></a> </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="panel">
                            <div className="panel-heading summary_heading">
                              <div className="btn-toolbar pull-right">
                                <div className="btn-group btn-space">
                                  <button type="button" className="btn btn-default"><i className="fa fa-search-plus"></i></button>
                                </div>
                              </div>
                              <span className="title">Opportunities</span> </div>
                            <div className="panel-body">
                              <div className="row">
                                <div className="col-md-2">
                                  <div className="mAd_icons oppr_icon"> </div>
                                </div>
                                <div className="col-md-10">
                                  <p className="lead">mAdvisor has observed opportunities for improving the sales figures by engaging with other key factor and metrics.</p>
                                  <ul>
                                    <li> Focusing more on cities, Miami, Seattle, and Boston would enhance overall sales, as they show high potential for growth and hold significant portion of current sales.</li>
                                    <li>A one percentage increase in marketing cost for the segment, where Deal Type is Gourmet, Discount Range is 21 to 30 percent, and Marketing Channel is Google Ads, will correspond to 0.7% increase in sales.</li>
                                    <li>The marginal effect of shipping cost on sales is very significant on Price Range, 101 to 500, as sales move by almost 46 units for every unit decrease in marketing cost.</li>
                                  </ul>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
      				  </div>
                        <div role="tabpanel" className="tab-pane" id="trend">
                          <div className="content_scroll">
      					<h3>Trend</h3>
      					<div className="panel">
                                <div className="panel-heading summary_heading">
                                  <div className="btn-toolbar pull-right">
                                    <div className="btn-group btn-space">
                                      <button type="button" className="btn btn-default"><i className="fa fa-search-plus"></i></button>
                                    </div>
                                  </div>
                                  <span className="title">Variance in sales</span> </div>
                                <div className="panel-body">
                                  <div className="grp_height"> <img src={ STATIC_URL + "assets/images/graph_1.png"} alt="grp 3" className="img-responsive"/> </div>
                                  <div className="grp_legends grp_legends_primary">
                                    <div className="grp_legend_label">
                                      <h3> 6% <small>Average Sale</small> </h3>
                                    </div>
                                    <div className="grp_more"> <a href="#"><span className="fa fa-ellipsis-h fa-2x"></span></a> </div>
                                  </div>
                                </div>
                              </div>
      					</div>
                        </div>
                        <div role="tabpanel" className="tab-pane" id="performance">
                          <div className="sb_navigation">
                            <div className="row">
                              <div className="col-xs-11">
                                <div className="scroller scroller-left"><i className="glyphicon glyphicon-chevron-left"></i></div>
                                <div className="scroller scroller-right"><i className="glyphicon glyphicon-chevron-right"></i></div>
                                <div className="wrapper">
                                  <ul className="nav nav-tabs list" id="myTab">
                                    <li><a href="#" className="active" title="Average Number of cart 1"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 1</span></a></li>
                                    <li><a href="#" title="Average Number of cart 2"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 2</span></a></li>
                                    <li><a href="#" title="Average Number of cart 3"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 3</span></a></li>
                                    <li><a href="#" title="Average Number of cart 4"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 4</span></a></li>
                                    <li><a href="#" title="Average Number of cart 5"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 5</span></a></li>
                                    <li><a href="#" title="Average Number of cart 6"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 6</span></a></li>
                                    <li><a href="#" title="Average Number of cart 7"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 7</span></a></li>
                                    <li><a href="#" title="Average Number of cart 8"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 8</span></a></li>
                                    <li><a href="#" title="Average Number of cart 9"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 9</span></a></li>
                                    <li><a href="#" title="Average Number of cart 10"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 10</span></a></li>
                                    <li><a href="#" title="Average Number of cart 11"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 11</span></a></li>
                                    <li><a href="#" title="Average Number of cart 12"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 12</span></a></li>
                                    <li><a href="#" title="Average Number of cart 13"><i className="mAd_icons ic_perf"></i><span>Average Number of cart 13</span></a></li>
                                  </ul>
                                </div>
                              </div>
                              <div className="col-xs-1">
                                <div className="input-group">
                                  <button id='search-button' className='btn btn-default '><span className='glyphicon glyphicon-search'></span></button>
                                </div>
                              { /* <!-- Search form */}<a href="javascript:;" className="input-group-addon"><i className="fa fa-search fa-2x"></i></a>-->
                                <div id='search-form' className="form-group">
                                  <div className="input-group"> <span id='search-icon' className="input-group-addon"><span className='glyphicon glyphicon-search'></span></span>
                                    <input type="text" className="form-control" placeholder="Search"/>
                                  </div>
                                </div>
                              { /* <!-- /.Search form -->*/}

                              </div>
                            </div>
                          </div>
                          <div className="content_scroll container-fluid">
                            <div className="row row-offcanvas row-offcanvas-left">

                            { /* <!--/span-->*/}
                              <div className="col-xs-12 col-sm-9 content"> <img src={ STATIC_URL + 'assets/images/graph_1.png' } className="img-responsive text-center"/>
                                <p> Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passage.. </p>
                              </div>
                            { /* <!--/span-->*/}

                              <div className="col-xs-6 col-sm-3 sidebar-offcanvas" id="sidebar" role="navigation">
                                <div className="side_panel"> <a href="javscript:;" data-toggle="offcanvas" className="sdbar_switch"><i className="mAd_icons sw_on"></i></a>
                                  <div className="panel panel-primary">
                                    <div className="panel-heading"> <span className="title"><i className="mAd_icons ic_perf active"></i> Measure 1 </span> </div>
                                    <div className="panel-body no-border">
                                      <div className="list-group"> <a href="#" className="list-group-item active">Miami's sales performance over time</a> <a href="#" className="list-group-item">City-Sales Performance Decision Matrix</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> <a href="#" className="list-group-item">Link</a> </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <div className="clearfix"></div>
                            </div>
                            {/*<!--/row-->*/}

                          </div>
                          {/*<!-- /.container -->*/}
                        </div>
                        <div role="tabpanel" className="tab-pane" id="influences">
      				  <h1>Influences</h1>
      				  <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passage..</p></div>
                        <div role="tabpanel" className="tab-pane" id="predictions">
      				  <h1>Predictions</h1>
      				  <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passage..</p></div>
                        <a className="tabs-control left grp_legends_green back" href="#" > <span className="fa fa-chevron-left"></span> </a> <a className="tabs-control right grp_legends_green continue" href="#" > <span className="fa fa-chevron-right"></span> </a> </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

        {   /* <!-- Till this end copy the above code -->*/}

          </div>
        { /* <!-- /.Page Content Area -->*/}

        </div>
        {/*<!-- /. Main Content ends with side-body -->*/}

      </div>

    )
  }
}
