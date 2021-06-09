import React from "react";
import { connect } from "react-redux";
import { Button, Modal } from "react-bootstrap";
import {closeDtModalAction} from "../../actions/dataActions";
import {Scrollbars} from 'react-custom-scrollbars';
import {STATIC_URL} from "../../helpers/env";
import store from "../../store";
@connect((store) => {
  return {
    dtModelShow: store.datasets.dtModelShow,
    dtRule: store.datasets.dtRule,
    dtData: store.signals.signalAnalysis.listOfNodes,
    dtPath: store.datasets.dtPath,
    dtJsonFormat: store.datasets.dtJsonFormat,
    dtName: store.datasets.dtName,
  };
})

export class DecisionTree extends React.Component {
  constructor(props) {
    super(props);
  }
 
  componentDidMount(){
    this.refs.test.innerHTML = this.props.dtRule;
    let Json = "";
    let newObject;
    if(!window.location.href.includes("scores")){
      if(store.getState().signals.signalAnalysis.listOfNodes.filter(i=>i.name==="Prediction")[0].listOfNodes!=undefined){
        Json = this.props.dtData.filter(i=>i.name=="Prediction")[0].decisionTree 
      }else{
        var predConfig = store.getState().signals.signalAnalysis.listOfNodes.filter(i=>i.name==="Prediction")[0]
        Json = predConfig[store.getState().datasets.dtName].decisionTree
      }
    }else{
      Json = store.getState().apps.scoreSummary.data.listOfCards[0].decisionTree
    }
    if(Json != undefined && document.getElementById("tree-vertical").childNodes.length===0){
      newObject =  JSON.parse(JSON.stringify(Json))
      this.BuildHorizontalTree(newObject, "#tree-vertical")
    }
  }
 
  closeDTModal() {
    this.props.dispatch(closeDtModalAction());
  }
 
  BuildHorizontalTree(treeData, treeContainerDom) {
    var screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    var margin = {
      top: 20,
      right: 120,
      bottom: 20,
      left: 120
    };
    var width = screenWidth - margin.right - margin.left;
    var height = screenHeight - margin.top - margin.bottom;

    // Create a svg canvas
    var vis = d3.select("#viz").append("svg:svg")
      .attr("width", 400)
      .attr("height", 300)
      .append("svg:g")
      .attr("transform", "translate(40, 30)"); // shift everything to the right

    // Add tooltip div
    var div = d3.select("body").append("div")
      .attr("class", "dtTooltip")
      .style("opacity", 1e-6);

    // Create a tree "canvas"
    var tree = d3.layout.tree()
      .size([300, 150]);

    var i = 0,
      duration = 750;
    var tree = d3.layout.tree()
      .size([height, width]);
    var diagonal = d3.svg.diagonal()
      .projection(function (d) {
        return [d.y, d.x];
      });
    var svg = d3.select(treeContainerDom)
      .append("svg")
      .attr("width", width + margin.right + margin.left)
      .attr("height", height + margin.top + margin.bottom)
      //.attr("height", 500)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var Root = treeData;
    String.prototype.unquoted = function () { return this.replace(/(^")|("$)/g, '') }
    var rootArr= this.props.dtPath;
    for (var i = 0; i < rootArr.length; i++) {
      collapse(eval(rootArr[i]));
    }
    update(Root);

    function update(source) {
      // Compute the new tree layout.
      var nodes = tree.nodes(Root).reverse(),
      links = tree.links(nodes);
      // Normalize for fixed-depth.
      nodes.forEach(function (d) {
        d.y = d.depth * 150;
      });
      // Declare the nodes…
      var node = svg.selectAll("g.node")
        .data(nodes, function (d) {
          return d.id || (d.id = ++i);
        });

      // Stash the old positions for transition.
      nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
      });
      // Enter the nodes.
      var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
          return "translate(" + source.y0 + "," + source.x0 + ")";
        }).on("click", nodeclick);
      nodeEnter.append("circle")
        .on("mouseover", mouseover)
        .on("mousemove", function (d) { mousemove(d); })
        .on("mouseout", mouseout)
        .attr("fill", "red")
        .attr("r", 5.5)
        .attr("r", 10)
        .attr("stroke", function (d) {
          return d.children || d._children ? "steelblue" : "#00c13f";
        })
        .style("fill", function (d) {
          return d.children || d._children ? "lightsteelblue" : "#fff";
        });
      //.attr("r", 10)
      //.style("fill", "#fff");
      nodeEnter.append("text")
        .attr("y", function (d) {
          return d.children || d._children ? -18 : -18;
        })
        .attr("x", function (d) {
          return d.children || d._children ? 10 : 10;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", "right")
        .attr("class", 'text-tag')
        .text(function (d) {
          return d.name;
        })
        .call(wrap, 130)
        ;

      // Transition nodes to their new position.
      //horizontal tree
      var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) {
          return "translate(" + d.y + "," + d.x + ")";
        });
      nodeUpdate.select("circle")
        .attr("r", 10)
        .style("fill", function (d) {
          return d._children ? "lightsteelblue" : "#fff";
        });
      nodeUpdate.select("text")
        .style("fill-opacity", 1);

      // Transition exiting nodes to the parent's new position.
      var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) {
          return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();
      nodeExit.select("circle")
        .attr("r", 1e-6);
      nodeExit.select("text")
        .style("fill-opacity", 1e-6);

      // Update the links…
      // Declare the links…
      var link = svg.selectAll("path.link")
        .data(links, function (d) {
          return d.target.id;
        });
      // Enter the links.
      link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function (d) {
          var o = {
            x: source.x0,
            y: source.y0
          };
          return diagonal({
            source: o,
            target: o
          });
        });
      // Transition links to their new position.
      link.transition()
        .duration(duration)
        .attr("d", diagonal);

      // Transition exiting nodes to the parent's new position.
      link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
          var o = {
            x: source.x,
            y: source.y
          };
          return diagonal({
            source: o,
            target: o
          });
        })
        .remove();
    }
    function wrap(text, width) {
      text.each(function () {
        var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          lineNumber = 0,
          lineHeight = 1.4, // ems
          x = text.attr("x"),
          y = text.attr("y"),
          dy = 0, //parseFloat(text.attr("dy")),
          tspan = text.text(null)
            .append("tspan")
            .attr("x", x)
            .attr("y", y)
            .attr("dy", dy + "em");
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(" "));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(" "));
            line = [word];
            tspan = text.append("tspan")
              .attr("x", x)
              .attr("y", y)
              .attr("dy", ++lineNumber * lineHeight + dy + "em")
              .text(word);
          }
        }
      });
    }
    function collapse(d) {
      if (d.children) {
        d._children = d.children
        d._children.forEach(collapse)
        d.children = null
      }
    }
   
    // Toggle children on click.
    function nodeclick(d) {
      if (d.children) {
        d._children = d.children;
        d.children = null;
      } else {
        d.children = d._children;
        d._children = null;
      }
      update(d);
    }
    function mouseover() {
      div.transition()
        .duration(300)
        .style("opacity", 1);
    }
    function mousemove(d) {
      div
        // .text("Info about " + d.name1)
        .text(d.name1)
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY) + "px");
    }
    function mouseout() {
      div.transition()
        .duration(300)
        .style("opacity", 1e-6);
    }
  }

  render() {
    return (
      <div id="decisionTreePopup" role="dialog" className="modal fade modal-colored-header ">
        <Modal show={this.props.dtModelShow} onHide={this.closeDTModal.bind(this)} dialogClassName="modal-colored-header dtModal modal-md modalOpacity">
          <Modal.Header>
            <h3 className="modal-title">Prediction Rule</h3>
          </Modal.Header>
          <Modal.Body>
            {window.location.href.includes("scores")?
            <div className="row">
              <div className="col-sm-12" >
                <div ref="test" style={{padding: '0 15px'}}></div>
                {store.getState().apps.scoreSummary.data.listOfCards[0].decisionTree != undefined &&
                  <div className="legends">
                    <img src={STATIC_URL + "assets/images/node.jpg"} className="img-responsive dtImage" />
                    <span>node</span>
                    <img src={STATIC_URL + "assets/images/collapseNode.jpg"} className="img-responsive dtImage" />
                    <span>collapsed node</span>
                    <img src={STATIC_URL + "assets/images/endNode.jpg"} className="img-responsive dtImage" />
                    <span>end node</span>
                  </div>
                }
              </div>
              <Scrollbars style={store.getState().apps.scoreSummary.data.listOfCards[0].decisionTree != undefined ? {height:450} : {minHeight:90,maxHeight:250} }>
                <div id="tree-vertical"></div>
              </Scrollbars>
            </div>
            :
            <div className="row">
              <div className="col-sm-12" >
                <div ref="test" style={{padding: '0 15px'}}></div>
                {this.props.dtData.filter(i=>i.name=="Prediction")[0].decisionTree != undefined &&
                  <div className="legends">
                    <img src={STATIC_URL + "assets/images/node.jpg"} className="img-responsive dtImage" />
                    <span>node</span>
                    <img src={STATIC_URL + "assets/images/collapseNode.jpg"} className="img-responsive dtImage" />
                    <span>collapsed node</span>
                    <img src={STATIC_URL + "assets/images/endNode.jpg"} className="img-responsive dtImage" />
                    <span>end node</span>
                  </div>
                }
              </div>
              <Scrollbars style={this.props.dtData.filter(i=>i.name=="Prediction")[0].decisionTree != undefined ? {height:450} : {minHeight:250,maxHeight:450} }>
                <div id="tree-vertical"></div>
              </Scrollbars>
            </div>
            }
          </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.closeDTModal.bind(this)}>Cancel</Button>
        </Modal.Footer>
      </Modal>
    </div>
    );
  }
}