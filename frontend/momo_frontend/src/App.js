import React, {useEffect} from "react";
import { Chart as ChartJS, defaults } from "chart.js/auto";
import { Bar, Doughnut, Line } from "react-chartjs-2";
import axios from "axios"

import "./App.css";

import revenueData from "./data/revenueData.json";
import sourceData from "./data/sourceData.json";


defaults.maintainAspectRatio = false;
defaults.responsive = true;

defaults.plugins.title.display = true;
defaults.plugins.title.align = "start";
defaults.plugins.title.font.size = 20;
defaults.plugins.title.color = "black";

export const App = () => {
    const [data,setData] = React.useState([]);
    const [loading,setLoading] =React.useState(true);
    const [error,setError] =React.useState(null);

    useEffect(() =>{
        const fetchData =async () => {
            try{
                const response = await axios.get("http://localhost:5000/api/users");
                setData(response.data);

            }catch(err){
                setError(err);
            } finally {
                setLoading(false);
                console.log(data);
            }
        };
        fetchData();
    },[] )
    return (
        <div className="App">
            <div className="dataCard revenueCard">
                <Line
                    data={{
                        labels: revenueData.map((data) => data.label),
                        datasets: [
                            {
                                label: "Revenue",
                                data: revenueData.map((data) => data.revenue),
                                backgroundColor: "#064FF0",
                                borderColor: "#064FF0",
                            },
                            {
                                label: "Cost",
                                data: revenueData.map((data) => data.cost),
                                backgroundColor: "#FF3030",
                                borderColor: "#FF3030",
                            },
                        ],
                    }}
                    options={{
                        elements: {
                            line: {
                                tension: 0.5,
                            },
                        },
                        plugins: {
                            title: {
                                text: "Monthly Revenue & Cost",
                            },
                        },
                    }}
                />
            </div>

            <div className="dataCard customerCard">
                <Bar
                    data={{
                        labels: sourceData.map((data) => data.label),
                        datasets: [
                            {
                                label: "Count",
                                data: sourceData.map((data) => data.value),
                                backgroundColor: [
                                    "rgba(43, 63, 229, 0.8)",
                                    "rgba(250, 192, 19, 0.8)",
                                    "rgba(253, 135, 135, 0.8)",
                                ],
                                borderRadius: 5,
                            },
                        ],
                    }}
                    options={{
                        plugins: {
                            title: {
                                text: "Revenue Source",
                            },
                        },
                    }}
                />
            </div>

            <div className="dataCard categoryCard">
                <Doughnut
                    data={{
                        labels: sourceData.map((data) => data.label),
                        datasets: [
                            {
                                label: "Count",
                                data: sourceData.map((data) => data.value),
                                backgroundColor: [
                                    "rgba(43, 63, 229, 0.8)",
                                    "rgba(250, 192, 19, 0.8)",
                                    "rgba(253, 135, 135, 0.8)",
                                ],
                                borderColor: [
                                    "rgba(43, 63, 229, 0.8)",
                                    "rgba(250, 192, 19, 0.8)",
                                    "rgba(253, 135, 135, 0.8)",
                                ],
                            },
                        ],
                    }}
                    options={{
                        plugins: {
                            title: {
                                text: "Revenue Sources",
                            },
                        },
                    }}
                />
            </div>
        </div>
    );
};

export default App;