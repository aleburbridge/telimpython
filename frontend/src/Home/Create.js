import RedButton from "../Components/RedButton";

function Create({ goBack }) {
    return(
        <div>
            Create :D<br/>
            <RedButton label="Go Back" onClick={goBack}/>
        </div>
    )
}

export default Create;