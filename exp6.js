import { useState } from "react"
import {useNavigate} from 'react-router-dom';

function Exper6(){
    const [uname,setUname]=useState("");
    const [pass,setPass]=useState("");
    const navigate=useNavigate();

    const handleChangen=(e)=>{
        e.preventDefault();
        setUname(e.target.value);
    }
    const handleChangep=(e)=>{
        e.preventDefault();
        setPass(e.target.value);
    }
    const handleSubmit=async (e)=>{
        e.preventDefault();
        const resp=await fetch("http://localhost:3001/api/submitform",{
            method:'POST',
            headers:{'Content-Type': 'application/json',},
            body:JSON.stringify({username:uname,password:pass})
        }).then((res) => res.json());
        if (resp.success === true) {
            navigate("/home");
        } else {
            alert("Invalid credentials");
        }
        setPass('');
        setUname('');
    }

    return(
    <>
        <form onSubmit={handleSubmit} method="post">
        <h2>Login</h2>
        <div>
            <label for="username">Username:</label>
            <input type="text" onChange={handleChangen} id="username" value={uname} name="username" required />
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" onChange={handleChangep} id="password" value={pass} name="password" required/>
        </div>
        <button type="submit">Login</button>
        </form>
    </>
    )
}

export default Exper6;