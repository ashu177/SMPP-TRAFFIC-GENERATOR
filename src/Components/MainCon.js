import React, { Component } from "react"
import {ToastsContainer, ToastsStore, ToastsContainerPosition} from 'react-toasts';

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
			messageMethod: "",
			errors: { 
				systemId: "initialError",
				password: "initialError",
				systemType: "initialError",
				ip: "initialError",
				portNumber: "initialError",
				sourceAddressTon: "initialError",
				sourceAddressNpi: "initialError",
				sourceAddress: "initialError",
				sourceAddressRange: "initialError",
				destinationAddressTon: "initialError",
				destinationAddressNpi: "initialError",
				destinationAddress: "initialError",
				destinationAddressRange: "initialError",
				registeredDelivery: "initialError",
				dataCoding: "initialError",
				shortMessage: "initialError",
				messageMethod: "initialError",
			}
		}
		this.handleChange = this.handleChange.bind(this)
		this.handleSubmit = this.handleSubmit.bind(this)
	}

	handleChange(event) {
		//const {name, value, type, checked} = event.target
		// type === "checkbox" ? this.setState({ [name]: checked }) : this.setState({ [name]: value })

		const { name, value } = event.target
		const validIpRegex = RegExp(/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/);
		//const validEmailRegex = RegExp(/^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i);

		let errors = this.state.errors;
		switch (name) {
			case 'systemId':
				errors.systemId =
					value.length < 1
						? 'System ID must not be blank!'
						: '';
				break;
			case 'password':
				errors.password =
					value.length < 1
						? 'Password must not be blank!'
						: '';
				break;
			case 'systemType':
				errors.systemType =
					value.length < 1
						? 'System Type must not be blank!'
						: '';
				break;
			case 'ip':
				errors.ip =
					validIpRegex.test(value)
						? ''
						: 'IP Address is not valid!';
				break;
			case 'portNumber':
				errors.portNumber =
					value.length === 4
						? ''
						: 'Port Number must not be blank!';
				break;
			case 'sourceAddressTon':
				errors.sourceAddressTon =
					value.length < 1
						? 'Source Address Ton must not be blank!'
						: '';
				break;
			case 'sourceAddressNpi':
				errors.sourceAddressNpi =
					value.length < 1
						? 'Source Address Npi must not be blank!'
						: '';
				break;
			case 'sourceAddress':
				errors.sourceAddress =
					value.length < 1
						? 'Source Address must not be blank!'
						: '';
				break;
			case 'sourceAddressRange':
				errors.sourceAddressRange =
					value.length < 1
						? 'Source Address Range must not be blank!'
						: '';
				break;
			case 'destinationAddressTon':
				errors.destinationAddressTon =
					value.length < 1
						? 'Destination Address Ton must not be blank!'
						: '';
				break;
			case 'destinationAddressNpi':
				errors.destinationAddressNpi =
					value.length < 1
						? 'Destination Address Npi must not be blank!'
						: '';
				break;
			case 'destinationAddress':
				errors.destinationAddress =
					value.length < 1
						? 'Destination Address must not be blank!'
						: '';
				break;
			case 'destinationAddressRange':
				errors.destinationAddressRange =
					value.length < 1
						? 'Destination Address Range must not be blank!'
						: '';
				break;
			case 'registeredDelivery':
				errors.registeredDelivery =
					value.length < 1
						? 'Registered Delivery must not be blank!'
						: '';
				break;
			case 'dataCoding':
				errors.dataCoding =
					value.length < 1
						? 'Data Coding must not be blank!'
						: '';
				break;
			case 'shortMessage':
				errors.shortMessage =
					value.length < 1
						? 'Short Message must not be blank!'
						: '';
				break;
			case 'messageMethod':
				if(value === "randomMessage"){
					errors.shortMessage = '';
				} else {
					errors.shortMessage = 'initialError';
				}
				errors.messageMethod =
					value.length < 1
						? 'Message Method must not be blank!'
						: '';
				break;
			
			/*case 'email':
				errors.email =
					validEmailRegex.test(value)
						? ''
						: 'Email is not valid!';
				break;
				case 'password':
				errors.password =
				value.length < 8
				? 'Password must be 8 characters long!'
				: '';
				break;
				*/
			default:
				break;
		}

		this.setState({ errors, [name]: value }, () => {
			console.log(errors)
		})
	}

	handleSubmit(event) {
		event.preventDefault();
		console.log(this.state.errors)
		if (validateForm(this.state.errors)) {
			try{
				console.info("Valid Form")
				const data = new FormData(event.target);
				let object = {}
				for (const [key, value] of data.entries()) {
					object[key] = value
				}
				object["msgSend"] ="0"
				object["ackRecv"] ="0"
				object["timeStamp"] = Date.now()
				
				fetch('http://172.19.6.33:5000/reciveMessage', {
					method: 'POST',
					headers: {
						Accept: 'application/json',
						'Content-Type': 'application/json',
						'Content-Length': '23'
					},
					body: JSON.stringify(object),
				});
				ToastsStore.success("Success")
			}
			catch(e){
				ToastsStore.warning("Request not sent" + e);
			}
		} else {
			ToastsStore.error("Invalid Form")
			console.error("Invalid Form")
		}
	}

	render() {
		return (
			<div>
				<br/>
				<div align="center">
					<form onSubmit={this.handleSubmit} className="tableStyle">
						<br />
						<label htmlFor="systemId" className="b">System ID:</label>
						<br />
						<input
							className="a"
							type="text"
							value={this.state.systemId}
							name="systemId"
							placeholder="System ID"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.systemId === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="systemId" className="makeError">{this.state.errors.systemId}</label>
						</div>
						<hr />
						<label htmlFor="password">Password: </label>
						<br />
						<input
							type="password"
							value={this.state.password}
							name="password"
							placeholder="Password"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.password === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="password" className="makeError">{this.state.errors.password}</label>
						</div>
						<hr />
						<label htmlFor="systemType">System Type:</label>
						<br />
						<input
							type="text"
							value={this.state.systemType}
							name="systemType"
							placeholder="System Type"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.systemType === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="systemType" className="makeError">{this.state.errors.systemType}</label>
						</div>
						<hr />
						<label htmlFor="ip">IP Address: </label>
						<br />
						<input
							type="text"
							value={this.state.ip}
							name="ip"
							placeholder="IP"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.ip === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="ip" className="makeError">{this.state.errors.ip}</label>
						</div>
						<hr />
						<label htmlFor="portNumber">Port Number:</label>
						<br />
						<input
							type="number"
							value={this.state.portNumber}
							name="portNumber"
							placeholder="Port Number"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.portNumber === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="portNumber" className="makeError">{this.state.errors.portNumber}</label>
						</div>
						<hr />
						<label htmlFor="sourceAddressTon">Source Address Ton:</label>
						<br />
						<input
							type="text"
							value={this.state.sourceAddressTon}
							name="sourceAddressTon"
							placeholder="Source Address Ton"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.sourceAddressTon === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="sourceAddressTon" className="makeError">{this.state.errors.sourceAddressTon}</label>
						</div>
						<hr />
						<label htmlFor="sourceAddressNpi">Source Address Npi:</label>
						<br />
						<input
							type="text"
							value={this.state.sourceAddressNpi}
							name="sourceAddressNpi"
							placeholder="Source Address Npi"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.sourceAddressNpi === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="sourceAddressNpi" className="makeError">{this.state.errors.sourceAddressNpi}</label>
						</div>
						<hr />
						<label htmlFor="sourceAddress">Source Address: </label>
						<br />
						<input
							type="text"
							value={this.state.sourceAddress}
							name="sourceAddress"
							placeholder="Source Address"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.sourceAddress === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="sourceAddress" className="makeError">{this.state.errors.sourceAddress}</label>
						</div>
						<hr />
						<label htmlFor="sourceAddressRange">Source Address Range:</label>
						<br />
						<input
							type="text"
							value={this.state.sourceAddressRange}
							name="sourceAddressRange"
							placeholder="Source Address Range"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.sourceAddressRange === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="sourceAddressRange" className="makeError">{this.state.errors.sourceAddressRange}</label>
						</div>
						<hr />
						<label htmlFor="destinationAddressTon">Destination Address Ton:</label>
						<br />
						<input
							type="text"
							value={this.state.destinationAddressTon}
							name="destinationAddressTon"
							placeholder="Destination Address Ton"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.destinationAddressTon === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="destinationAddressTon" className="makeError">{this.state.errors.destinationAddressTon}</label>
						</div>
						<hr />
						<label htmlFor="destinationAddressNpi">Destination Address Npi:</label>
						<br />
						<input
							type="text"
							value={this.state.destinationAddressNpi}
							name="destinationAddressNpi"
							placeholder="Destination Address Npi"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.destinationAddressNpi === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="destinationAddressNpi" className="makeError">{this.state.errors.destinationAddressNpi}</label>
						</div>
						<hr />
						<label htmlFor="destinationAddress">Destination Address:</label>
						<br />
						<input
							type="text"
							value={this.state.destinationAddress}
							name="destinationAddress"
							placeholder="Destination Address"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.destinationAddress === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="destinationAddress" className="makeError">{this.state.errors.destinationAddress}</label>
						</div>
						<hr /> 
						<label htmlFor="destinationAddressRange">Destination Address Range:</label>
						<br />
						<input
							type="text"
							value={this.state.destinationAddressRange}
							name="destinationAddressRange"
							placeholder="Destination Address Range"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.destinationAddressRange === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="destinationAddressRange" className="makeError">{this.state.errors.destinationAddressRange}</label>
						</div>
						<hr />
						<label htmlFor="registeredDelivery">Registered Delivery:</label>
						<br />
						<input
							type="text"
							value={this.state.registeredDelivery}
							name="registeredDelivery"
							placeholder="Registered Delivery"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.registeredDelivery === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="registeredDelivery" className="makeError">{this.state.errors.registeredDelivery}</label>
						</div>
						<hr />
						<label htmlFor="dataCoding">Data Coding: </label>
						<br />
						<input
							type="text"
							value={this.state.dataCoding}
							name="dataCoding"
							placeholder="Data Coding"
							onChange={this.handleChange}
						/>
						<div className={this.state.errors.dataCoding === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="dataCoding" className="makeError">{this.state.errors.dataCoding}</label>
						</div>
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
						<div className={this.state.errors.messageMethod === "initialError" ? "hideDontTakeUpSpace" : null}>
							<label htmlFor="messageMethod" className="makeError">{this.state.errors.messageMethod}</label>
						</div>
						<div className={this.state.messageMethod === "customMessage" ? null : "hideDontTakeUpSpace"}>
							<hr />
							<label htmlFor="shortMessage">Short Message:</label>
							<br />
							<textarea
								value={this.state.shortMessage}
								name="shortMessage"
								placeholder="Short Message"
								onChange={this.handleChange}
							/>
							<div className={this.state.errors.shortMessage === "initialError" ? "hideDontTakeUpSpace" : null}>
								<label htmlFor="shortMessage" className="makeError">{this.state.errors.shortMessage}</label>
							</div>
						</div>
						<br />
						<hr />
						<div align="right">
							<button>Submit</button>
						</div>
					</form>
					<br />
					<br />
				</div>
				<ToastsContainer store={ToastsStore} position={ToastsContainerPosition.BOTTOM_CENTER}/>
			</div>
		)
	}
}

function validateForm(errors) {
	let valid = true;
	Object.values(errors).forEach(
		(val) => val.length > 0 && (valid = false)
	);
	return valid;
}

export default MainCon