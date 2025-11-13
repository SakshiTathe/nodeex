import React, { useEffect, useState } from "react";

function Exper5(){
    const [data,setdata]=useState([]);
    useEffect(()=>{
        fetch('http://localhost:3001/api/getitem')
        .then(response=>response.json())
        .then(data=>setdata(data))
        .catch(console.log("error"))
    })
    return(
        <div>
            <h1>All data</h1>
            <ul>
                {data.map(i=>(
                    
                    <li key={i.id}>{i.name}</li>
                ))}
            </ul>
        </div>
    )
}
export default Exper5;

/**
 * 

User Authentication and 
Authorization

React State Management
Context API in React.js
Data Fetching in React.js
Integrating React with Express

 */