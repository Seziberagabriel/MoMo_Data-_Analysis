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

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/api/transactions");
                setData(response.data);


            }catch(err){
                setError(err);
            } finally {
                setLoading(false);

            }
        };
        fetchData();
    },[] )
    return (
        <div className="App">


            <table className="table">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Transaction Type</th>
                    <th scope="col">Transaction Details</th>
                    {/*<th scope="col">Handle</th>*/}
                </tr>
                </thead>
                <tbody>
                {data.map((item) => (
                    // <div key={item.id}>
                    //     <>Transaction
                    <tr>
                    <th scope="row">{item.id}</th>
                    <td>{item.type}</td>
                    <td>{item.details}</td>
                    </tr>
                ))}

                </tbody>
            </table>
        </div>
    );
};

export default App;