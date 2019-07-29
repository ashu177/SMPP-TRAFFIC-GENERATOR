	import React, { Component } from "react"

	class MainCon extends Component {
		constructor() {
			super()
			this.state = {
				systemId: "",
				password: "",
				systemType: "",
				ip: "",
				portNumber: "",
				sourceAddressTon: "",
				sourceAddressNpi: "",
				sourceAddress: "",
				sourceAddressRange: "",
				destinationAddressTon: "",
				destinationAddressNpi: "",
				destinationAddress: "",
				destinationAddressRange: "",
				registeredDelivery: "",
				dataCoding: "",
				shortMessage: "",
				id: "",
				messageMethod: "",
				//isFriendly: false,
				//favColor: "blue"
			}
			this.handleChange = this.handleChange.bind(this)
		}

		handleChange(event) {
			//const {name, value, type, checked} = event.target
			// type === "checkbox" ? this.setState({ [name]: checked }) : this.setState({ [name]: value })

			const { name, value } = event.target
			this.setState({ [name]: value })
		}

		handleSubmit(event) {
			event.preventDefault();
			const data = new FormData(event.target);
			let object = {}
			for (const [key, value] of data.entries()) {
				object[key] = value
			}
			object["msgSend"] = "0"
			object["timeStamp"] = Date.now()
			object["ackRecv"]="0"

			fetch('http://172.19.6.33:5000/reciveMessage', {
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
			return (
				<div>
					<div align="center">
						<form onSubmit={this.handleSubmit} className="tableStyle">
							<br />
							<label htmlFor="systemId" className="b">System ID:</label>
							<input
								className="a"
								type="text"
								value={this.state.systemId}
								name="systemId"
								placeholder="System ID"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="password">Password: </label>
							<input
								type="text"
								value={this.state.password}
								name="password"
								placeholder="Password"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="systemType">System Type:</label>
							<input
								type="text"
								value={this.state.systemType}
								name="systemType"
								placeholder="System Type"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="ip">IP Address: </label>
							<input
								type="text"
								value={this.state.ip}
								name="ip"
								placeholder="IP"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="portNumber">Port Number:</label>
							<input
								type="text"
								value={this.state.portNumber}
								name="portNumber"
								placeholder="Port Number"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="sourceAddressTon">Source Address Ton:</label>
							<input
								type="text"
								value={this.state.sourceAddressTon}
								name="sourceAddressTon"
								placeholder="Source Address Ton"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="sourceAddressNpi">Source Address Npi:</label>
							<input
								type="text"
								value={this.state.sourceAddressNpi}
								name="sourceAddressNpi"
								placeholder="Source Address Npi"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="sourceAddress">Source Address: </label>
							<input
								type="text"
								value={this.state.sourceAddress}
								name="sourceAddress"
								placeholder="Source Address"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="sourceAddressRange">Source Address Range:</label>
							<input
								type="text"
								value={this.state.sourceAddressRange}
								name="sourceAddressRange"
								placeholder="Source Address Range"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="destinationAddressTon">Destination Address Ton:</label>
							<input
								type="text"
								value={this.state.destinationAddressTon}
								name="destinationAddressTon"
								placeholder="Destination Address Ton"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="destinationAddressNpi">Destination Address Npi:</label>
							<input
								type="text"
								value={this.state.destinationAddressNpi}
								name="destinationAddressNpi"
								placeholder="Destination Address Npi"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="destinationAddress">Destination Address:</label>
							<input
								type="text"
								value={this.state.destinationAddress}
								name="destinationAddress"
								placeholder="Destination Address"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="destinationAddressRange">Destination Address Range:</label>
							<input
								type="text"
								value={this.state.destinationAddressRange}
								name="destinationAddressRange"
								placeholder="Destination Address Range"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="registeredDelivery">Registered Delivery:</label>
							<input
								type="text"
								value={this.state.registeredDelivery}
								name="registeredDelivery"
								placeholder="Registered Delivery"
								onChange={this.handleChange}
							/>
							<hr />
							<label htmlFor="dataCoding">Data Coding: </label>
							<input
								type="text"
								value={this.state.dataCoding}
								name="dataCoding"
								placeholder="Data Coding"
								onChange={this.handleChange}
							/>
							<hr />
							<label>
								<input
									type="radio"
									name="messageMethod"
									value="randomMessage"
									checked={this.state.messageMethod === "randomMessage"}
									onChange={this.handleChange}
								/> Random Message
					</label>
							<label>
								<input
									type="radio"
									name="messageMethod"
									value="customMessage"
									checked={this.state.messageMethod === "customMessage"}
									onChange={this.handleChange}
								/> Custom Message
					</label>
							<div className={this.state.messageMethod === "customMessage" ? null : "hideDontTakeUpSpace"}>
								<hr />
								<label htmlFor="shortMessage">Short Message:</label>
								<textarea
									//className="hideDontTakeUpSpace"
									value={this.state.shortMessage}
									name="shortMessage"
									placeholder="Short Message"
									onChange={this.handleChange}
								/>
							</div>
							<br />
							{/* Formik */}
							{/**
					<label>Favorite Color:</label>
					<select
						value={this.state.favColor}
						onChange={this.handleChange}
						name="favColor"
						<option value="blue">Blue</option>
						<option value="green">Green</option>
						<option value="red">Red</option>
						<option value="orange">Orange</option>
						<option value="yellow">Yellow</option>
					</select>
					*/}
							{/*<h1>{this.state.systemId} {this.state.password}</h1>*/}
							<hr />
							{/*<h2>Your favorite color is {this.state.favColor}</h2>*/}
							<div align="right">
								<button>Submit</button>
							</div>
						</form>
					</div>
				</div>
			)
		}
	}


	export default MainCon