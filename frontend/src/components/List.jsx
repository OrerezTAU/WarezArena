function List(props){
      function handleClick(){
    props.deletion(props.id)
  }
    return (
        <div className="store">
          <h1 >  Name: {props.name} </h1>
            {props.url!=null && <p > URL: {props.url}</p>}
            {props.year_founded!=null && <p > Year Founded: {props.year_founded}</p>}
            <p > Description: {props.description}</p>
          <button onClick={handleClick}>Delete</button>
        </div>
    )
  }

export default List;