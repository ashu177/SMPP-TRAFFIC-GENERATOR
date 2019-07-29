import React, { Component } from "react"
import ReactTable from 'react-table'
import 'react-table/react-table.css'
//import '/public/style.css'

class MainConDashboard extends Component {
	constructor(props) {
		super(props);
		this.state = {
			selected: {},
			selectAll: 0,
			data: this.makeData(),
			timeCheck: 0,
			error: null,
			isLoaded: false,
			posts: []
		};
		this.handleStop = this.handleStop.bind(this);
		this.handlePause = this.handlePause.bind(this);
		this.handleResume = this.handleResume.bind(this);
		this.makeData = this.makeData.bind(this);
	}

	makeData() {
		fetch('http://172.19.6.33:5000/makeData', {
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
	toggleRow(timeStamp) {
		this.setState({ timeCheck: timeStamp }, () => {
			const newSelected = {};
			newSelected[timeStamp] = !this.state.selected[timeStamp];
			this.setState({
				selected: newSelected,
			});
		})

	}


	handlePause(event) {
		event.preventDefault();
		let object = {}
		object["timeCheck"] = this.state.timeCheck;

		fetch('http://172.19.6.33:5000/pause', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				'Content-Length': '23'
			},
			body: JSON.stringify(object),
		});
	}
	handleDelete(event) {
		event.preventDefault();
		let object = {}
		object["timeCheck"] = this.state.timeCheck;

		fetch('http://172.19.6.33:5000/pause', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				'Content-Length': '23'
			},
			body: JSON.stringify(object),
		});
	}

	handleStop(event) {
		event.preventDefault();
		let object = {}
		object["timeCheck"] = this.state.timeCheck;
		console.log(object["timeCheck"]);

		fetch('http://172.19.6.33:5000/stop', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				'Content-Length': '23'
			},
			body: JSON.stringify(object),
		});
	}

	handleResume(event) {
		event.preventDefault();
		let object = {}
		object["timeCheck"] = this.state.timeCheck;

		fetch('http://172.19.6.33:5000/resume', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
				'Content-Length': '23'
			},
			body: JSON.stringify(object),
		});
	}

	render() {
		const columns = [
			{
				accessor: "",
				Cell: ({ original }) => {
					return (
						<input
							type="radio"
							name="checking"
							checked={this.state.selected[original.timeStamp] === true}
							onChange={() => this.toggleRow(original.timeStamp)}
						/>
					);
				},
				Header: "",
				sortable: false,
				width: 45
			},
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
				{this.state.data}
				<div align="center">
					<h2>{this.state.timeCheck}</h2>
					<button type="button" variant="primary" onClick={this.handlePause}>Pause</button>
					<button type="button" onClick={this.handleResume}>Resume</button>
					<button type="button" onClick={this.handleStop}>Stop</button>
					
				</div>
				<br />
				<ReactTable
					data= {this.state.posts}
					
					columns={columns}
					defaultSorted={[{ id: "timeStamp", desc: false }]}
				/>
				
			</div>
		);
	}
}

export default MainConDashboard