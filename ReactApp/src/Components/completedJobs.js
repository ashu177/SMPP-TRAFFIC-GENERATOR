import React, { Component } from "react"
import ReactTable from 'react-table'
import 'react-table/react-table.css'
//import '/public/style.css'

class completedJobs extends Component {
	constructor(props) {
		super(props);
		this.state = {
			selected: {},
			selectAll: 0,
			data: this.getCompletedDJobs(),
			timeCheck: 0,
			error: null,
			isLoaded: false,
			posts: []
		};
		this.getCompletedDJobs = this.getCompletedDJobs.bind(this);
		
	}

	
	toggleRow(timeStamp) {
		this.setState({ timeCheck: timeStamp }, () => {
			const newSelected = {};
			newSelected[timeStamp] = !this.state.selected[timeStamp];
			this.setState({
				selected: newSelected,
			});
		})

	}
	
	getCompletedDJobs() {

		

		fetch('http://172.19.6.33:5000/getJob', {
			method: 'GET',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
			'Content-Length': '23'
		},
	})
		.then(response => response.json())
		.then(
			(result) => {
				this.setState({
					isLoaded: true,
					posts: result
				});
			},
			(error) => {
				this.setState({
					isLoaded: true,
					error
				})
			},
		)
	}


	

	render() {
		const columns = [
			
			{
				Header: "Job ID",
				accessor: "timeStamp"
			},
			{
				Header: "Message Sent",
				id: "messageSent",
				accessor: d => d.messageSent
			},
			{
				Header: "Message received",
				id: "messageReceived",
				accessor: d => d.messageReceived
			}
		];



		

		return (
			
				<div>
				<ReactTable variant="dark"
					data= {this.state.posts}
					
					columns={columns}
					defaultSorted={[{ id: "timeStamp", desc: false }]}
				/>
				
			</div>
		);
	}
}

export default completedJobs