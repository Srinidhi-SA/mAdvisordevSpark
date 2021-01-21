import React from "react";
import {Link} from "react-router-dom";
import {STATIC_URL} from "../../helpers/env";
import {LIST_OF_KYLO_OPERATIONS} from "../../helpers/kyloHelper"
import {hidechatbot, removeChatbotOnLogout} from "../../helpers/helper"

export class KyloMenuList extends React.Component {
  constructor(props) {
    super(props);

  }
  componentWillMount() {
    hidechatbot()
    removeChatbotOnLogout()
  }

  render() {
    const cardListDetailsModified = LIST_OF_KYLO_OPERATIONS.map((card, i) => {
      var imageLink = STATIC_URL + "assets/images/" + card.logo
      var kyloCardLink = "/datamgmt/selected_menu/" + card.relative_url;
      return (
        <div class="col-md-4 xs-mb-20" key={i}>
          <div>
            <div className="app-block d_manage">
              <Link className="app-link" to={kyloCardLink} id={card.slug + "22"}>

                <div className="col-md-4 col-sm-3 col-xs-5 xs-p-20">
                  <img src={imageLink} className="img-responsive"/>
                </div>
                <div className="col-md-8 col-sm-9 col-xs-7">
                  <h4>
                    {card.displayName}
                  </h4>
                  <p>
                    {card.description}
                  </p>
                </div>
                <div class="clearfix"></div>
              </Link>

            </div>

          </div>
          <div className="clearfix"></div>
        </div>
      )
    })

    return (
      <div className="side-body">
        <div className="page-head">
          <h3 class="xs-mt-0">Data Manage</h3>
        </div>
        <div className="clearfix"></div>
        <div className="main-content">
          <div className="row">
            {cardListDetailsModified}
          </div>
        </div>
      </div>
    );
  }
}
