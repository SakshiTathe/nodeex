import React, { useContext } from "react";
import { UserContext } from "./UserContext";

function Fetchdata() {
    const { users } = useContext(UserContext);
    return (
        <div>
            <h1>All Users</h1>
            <ul>
                {users.map((user) => (
                    <li key={user._id}>{user.username}</li>
                ))}
            </ul>
        </div>
    );
}

export default Fetchdata;
