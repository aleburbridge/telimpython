import { useTheme } from '@mui/material/styles';
import RedButton from '../Components/RedButton';
import TextField from '@mui/material/TextField';

function Join( {isCreating, goBack} ) {
    const theme = useTheme();

    return(
        <div>
            <TextField id="outlined-basic" label="Name"/><br/>
            <TextField disabled={isCreating} id={isCreating ? "outlined-disabled" : "outlined-basic"} label="Room Code" defaultValue={isCreating ? localStorage.getItem("room_code") : ""} sx={{ mt: 2 }}/><br/>
            <RedButton label={isCreating ? "Create Game" : "Join Game"} onClick={console.log("")}/><br/>
            <RedButton label={"Go Back"} onClick={goBack}/>
        </div>
    )
};
  
 export default Join;