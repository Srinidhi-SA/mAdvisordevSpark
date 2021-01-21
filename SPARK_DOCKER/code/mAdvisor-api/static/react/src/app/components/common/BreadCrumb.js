import React from "react";
import {NavLink} from "react-router-dom";

export class BreadCrumb extends React.Component {
  constructor() {
    super();
  }

  render() {
    let data = this.props.parameters;

    if (data) {
      let breadcrumb = data.map((page, i) => {
        if (page.url) {
          return (
            <ol key = {i} className="breadcrumb">
              <li>
                <NavLink to={page.url}>{page.name}</NavLink>
              </li>
            </ol>
          );
        } else {
          return (
            <ol key = {i} className="breadcrumb">
              <li>
                {page.name}
              </li>
            </ol>
          );
        }

      });

      return (
        <div>{breadcrumb}</div>
      );
    }
  }
}
