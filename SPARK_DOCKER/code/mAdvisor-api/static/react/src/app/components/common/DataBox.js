import React from "react";
export class DataBox extends React.Component {
	constructor(){
		super();
	}

	render() {
		var dataBox = this.props.jsonData;
		let columnsTemplates = dataBox.map((data,index)=>{
			return (
				<div key={index} className="col-md-2 col-sm-6 col-xs-12 bgStockBox">
					<h3 className="text-center">{data.value}<br/>
						<small data-toggle="tooltip" title={data.name.length>21?data.name:""}>{data.name}</small>
					</h3>
					<p>{data.description}</p>
				</div>
			);
		});
		return (
			<div className="documentDataBox">
				{columnsTemplates}
			</div>
		);
	}
}