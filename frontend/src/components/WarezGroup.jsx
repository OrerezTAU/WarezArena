import {useState, useEffect} from "react"
import axios from "axios"
import  List from "./List"
import AddIcon from '@material-ui/icons/Add';



function WarezGroup(){

    const [isExpanded, setExpanded]= useState(false)
    const [rows, setRows]= useState(1)


    const [groups, setNewWarezGroups] = useState(null)
    const [formWarezGroup, setFormWarezGroup] = useState({
        name: "",
        description: "",
        year_founded: "",
    })

    useEffect(() => {
        getWarezGroups()
    } ,[])


    function getWarezGroups() {
        /** When the GET request is made with axios, the data in the received response is assigned to the setNewWarezGroups
         * function, and this updates the state variable groups with a new state. Thus, the value of the state variable
         * changes from null to the data in the received response.
         */
        axios({
            method: "GET",
            url:"/cracken/warez_groups/",
        }).then((response)=>{
            const data = response.data
            setNewWarezGroups(data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response);
                console.log(error.response.status);
                console.log(error.response.headers);
            }
        })}

    function createWarezGroup(event) {
        /**
         * Here we are declaring the request method type as POST and then passing the absolute path cracken/warez_groups/ as the URL.
         * We also have an additional field here data. This will contain the data which we'll send to the backend for
         * processing and storage in the database. That is the data from the fields in the form.
         * */
        axios({
            method: "POST",
            url:"/cracken/warez_groups/",
            data:{
                name: formWarezGroup.name,
                description: formWarezGroup.description,
                year_founded: formWarezGroup.year_founded,
            }
        })
            .then((response) => {
                getWarezGroups()
            })

        setFormWarezGroup(({
            /** reset form inputs to empty after submit */
            name: "",
            description: "",
            year_founded: "",
        }))
        setExpanded(false)
        event.preventDefault()
    }
    function DeleteWarezGroup(id) {
        axios({
            method: "DELETE",
            url:`/cracken/warez_groups/${id}/`,
        })
            .then((response) => {
                getWarezGroups()
            });
    }

    function handleChange(event) {
        /**
         * The function monitors every single change in the form inputs and updates/delete where necessary.
         * Without this function, you won't see what you are typing in the form input fields and the values of your
         * input elements won't change as well
         */
        const {value, name} = event.target
        setFormWarezGroup(prevWarezGroup => ({
            ...prevWarezGroup, [name]: value})
        )}

    function BackgroundShow(){
        setExpanded(true)
        setRows(3)
    }


    return (
        <div className=''>

            <form className="create-group">
                <input onChange={handleChange} text={formWarezGroup.name} name="name" placeholder="Enter the group name" value={formWarezGroup.name} />
                <textarea onClick={BackgroundShow} onChange={handleChange} name="description" placeholder="Enter the group description" value={formWarezGroup.description} />
                <input onClick={BackgroundShow} onChange={handleChange} name="year_founded" placeholder="Enter the year founded" value={formWarezGroup.year_founded} />
                {isExpanded && <button onClick={createWarezGroup}><AddIcon /></button>}
            </form>
            { groups && groups.map(group => <List
                    key={group.id}
                    id={group.id}
                    name={group.title}
                    description={group.description}
                    year_founded={group.year_founded}
                    deletion ={DeleteWarezGroup}
                />
            )}

        </div>
    );
}

export default WarezGroup;


