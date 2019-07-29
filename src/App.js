import React from "react"
import Header from "./Components/Header"
import MainCon from "./Components/MainCon"
import MainConDashboard from "./Components/MainConDashboard"
import Footer from "./Components/Footer"
import CompletedJobs from "./Components/completedJobs"
import { render } from "react-dom";
import Tabs from "./Components/Tabs/Tabs";

const styles = {
	fontFamily: "sans-serif",
	textAlign: "center"
};

const App = () => (
	<div style={styles}>
		<Header />
		<Tabs
			activeTab={{
				id: "tab1"
			}}
		>
			<Tabs.Tab id="tab1" title="Dashboard">
				<MainConDashboard />
			</Tabs.Tab>
			<Tabs.Tab id="tab2" title="Send Traffic">
				<MainCon />
			</Tabs.Tab>
			<Tabs.Tab id="tab3" title="Completed Jobs">
				<CompletedJobs />
			</Tabs.Tab>
			<Footer />
		</Tabs>
	</div>
);

render(<App />, document.getElementById("root"));

export default App