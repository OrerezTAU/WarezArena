import {useState, useEffect} from "react"
import axios from "axios"
import  List from "./List"
import AddIcon from '@material-ui/icons/Add';



function Store(){

    const [isExpanded, setExpanded]= useState(false)
    const [rows, setRows]= useState(1)


    const [stores, setNewStores] = useState(null)
    const [formStore, setFormStore] = useState({
        name: "",
        url: "",
        description: "",
    })

    useEffect(() => {
        getStores()
    } ,[])


    function getStores() {
        /** When the GET request is made with axios, the data in the received response is assigned to the setNewStores
         * function, and this updates the state variable stores with a new state. Thus, the value of the state variable
         * changes from null to the data in the received response.
         */
        axios({
            method: "GET",
            url:"/cracken/stores/",
        }).then((response)=>{
            const data = response.data
            setNewStores(data)
        }).catch((error) => {
            if (error.response) {
                console.log(error.response);
                console.log(error.response.status);
                console.log(error.response.headers);
            }
        })}

    function createStore(event) {
        /**
         * Here we are declaring the request method type as POST and then passing the absolute path cracken//stores/ as the URL.
         * We also have an additional field here data. This will contain the data which we'll send to the backend for
         * processing and storage in the database. That is the data from the fields in the form.
         * */
        axios({
            method: "POST",
            url:"/cracken/stores/",
            data:{
                name: formStore.name,
                url: formStore.url,
                description: formStore.description,
            }
        })
            .then((response) => {
                getStores()
            })

        setFormStore(({
            /** reset form inputs to empty after submit */
            name: "",
            url: "",
            description: "",
        }))
        setExpanded(false)
        event.preventDefault()
    }
    function DeleteStore(id) {
        axios({
            method: "DELETE",
            url:`/cracken/stores/${id}/`,
        })
            .then((response) => {
                getStores()
            });
    }

    function handleChange(event) {
        /**
         * The function monitors every single change in the form inputs and updates/delete where necessary.
         * Without this function, you won't see what you are typing in the form input fields and the values of your
         * input elements won't change as well
         */
        const {value, name} = event.target
        setFormStore(prevStore => ({
            ...prevStore, [name]: value})
        )}

    function BackgroundShow(){
    setExpanded(true)
    setRows(3)
   }


    return (
<div className=''>

      <form className="create-store">
          <input onChange={handleChange} text={formStore.name} name="name" placeholder="Enter the store name" value={formStore.name} />
          <textarea onClick={BackgroundShow} onChange={handleChange} name="description" placeholder="Enter the store description" value={formStore.description} />
          <textarea onClick={BackgroundShow} onChange={handleChange} name="url" placeholder="Enter the store url address" value={formStore.url} />
          {isExpanded && <button onClick={createStore}><AddIcon /></button>}
      </form>
          { stores && stores.map(store => <List
          key={store.id}
          id={store.id}
          name={store.title}
          url={store.url}
          description={store.description}
          deletion ={DeleteStore}
          />
          )}

    </div>
  );
}

export default Store;


