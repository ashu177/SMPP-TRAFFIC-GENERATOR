import React from "react"

function Header() {
	return (
		<div>
 
			<header className="navbar"> 
				<img src={require('./../logo.jpg')} alt="logo" style={{height:50, marginTop: 25}} />
				<p>SMPP Traffic Generator</p>
			</header>
		</div>
	)
}

export default Header