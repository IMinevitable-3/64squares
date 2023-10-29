import { Outlet } from "react-router-dom";
 function Layout  (){
    return (
        <div className="App">
            <Outlet/> 
            {/* represents all the children of Layout component  */}
        </div>
    )
}
export default  Layout ;