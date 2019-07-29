import React from "react"
import StickyFooter from 'react-sticky-footer';

function Footer() {
	return (
		<StickyFooter
			bottomThreshold={50}
			normalStyles={{
				backgroundColor: "#DC143C",
				color: "white",
				padding: "1rem"
			}}
			stickyStyles={{
				backgroundColor: "gainsboro",
				padding: "0.1rem"
			}
		}
		>
			&copy; Copyright {new Date().getFullYear()} Comviva A Tech Mahindra Company.  All rights reserved!
</StickyFooter>
	)
}
export default Footer