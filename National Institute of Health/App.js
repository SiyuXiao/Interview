import React, {useState} from 'react';

const App = () => {

    const [todoList, setTodoList] = useState([
        {
            id: 1,
            content: 'Total anosmia'
        },
        {
            id: 2,
            content: 'Specific anosmia'
        },
        {
            id: 3,
            content: 'Partial anosmia'
        }
    ])
    let uuid = 3;
    //let isShown = true;

    const inputRef = React.useRef();

    function addItem() {
        const inputRefResult = inputRef.current.value;
        const newList = [...todoList]
        uuid = uuid + 1
        newList.unshift({id: uuid, content: inputRefResult})
        setTodoList(newList)
        //isShown = true
        inputRef.current.value = ''
    }

    return (
        <div >

            <ul>

                <li> Anosmia


                    <ul ><input ref={inputRef} onBlur={addItem} placeholder="click to add element"/></ul>
                    <ul>
                        {todoList.map(item => (
                            <Item key={item.id} item={item} />
                        ))}
                    </ul>

                </li>
            </ul>

        </div>
    );

};

const Item = ({item}) => (
    <div>
        <li>{item.content}</li>
    </div>
)



export default App;

