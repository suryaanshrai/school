function Result(props) {
    return (
        <div className={props.class}>
            <p className="heading">{props.topic}</p>
            <p>{props.date}</p>
            <p> You scored {props.marks} out of {props.max_marks}</p>
        </div>
    )
}

function Schedule(props) {
    return(
        <div className={props.class}>
            <p>{props.activity}</p>
            <p>Due date: {props.due_date}</p>
        </div>
    )
}

function Notice(props) {
    return(
        <div className={props.class}>
            <h4>{props.title}</h4>
            <p>Dated:{props.issue_date}</p>
            <p>{props.content}</p>
        </div>
    )
}

function App() {
    const [resultsData,setResultsData] = React.useState([]);
    React.useEffect(() => {
        fetch("/student/results")
        .then(response => response.json()) 
        .then(data => {
            console.log(data);
            setResultsData(data["result"]);
        });
    }, []);
    
    const [scheduleData,setSchdeduleData] = React.useState([]);
    React.useEffect(() => {
        fetch("/student/schedule")
        .then(response => response.json()) 
        .then(data => {
            console.log(data);
            setSchdeduleData(data["schedule"]);
        });
    }, []);

    const [noticeData,setNoticeData] = React.useState([]);
    React.useEffect(() => {
        fetch("/student/notices")
        .then(response => response.json()) 
        .then(data => {
            console.log(data);
            setNoticeData(data["notices"]);
        });
    }, []);

    function showResults() {
        document.querySelector("#results").classList.remove("hide");
        document.querySelector("#schedule").classList.add("hide");
        document.querySelector("#notices").classList.add("hide");
    }
    function showNotices() {
        document.querySelector("#results").classList.add("hide");
        document.querySelector("#schedule").classList.add("hide");
        document.querySelector("#notices").classList.remove("hide");
    }
    function showSchedule() {
        document.querySelector("#results").classList.add("hide");
        document.querySelector("#schedule").classList.remove("hide");
        document.querySelector("#notices").classList.add("hide");        
    }
    return(
        <>
            <div>
                <button onClick={showResults}>All Results</button>
                <button onClick={showSchedule}>Entire Schedule</button>
                <button onClick={showNotices}>All Notices</button>
            </div>
            <div id="results" className="hide">
                <h3>All Results</h3>
            {resultsData.map((data,id)=> (
                <Result key={data.id} 
                    class="boxComponent"
                    topic={data.topic} 
                    date={data.date} 
                    max_marks={data.max_marks} 
                    marks={data.marks} 
                />
            ))}
            </div>
            <div id="schedule" className="hide">
                <h3>Entire Schedule</h3>
                {scheduleData.map((data,id)=> (
                <Schedule key={data.id} 
                    class="boxComponent"
                    activity={data.activity} 
                    due_date={data.due_date} 
                />
            ))}
            </div>
            <div id="notices" className="hide">
                <h3>All Notices</h3>
                {noticeData.map((data,id)=> (
                <Notice key={data.id} 
                    class="boxComponent"
                    title={data.title} 
                    issue_date={data.issue_date} 
                    content={data.content}
                />
            ))}
            </div>
        </>
    )
}

ReactDOM.render(<App />, document.querySelector("#App"));