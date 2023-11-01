import { useTheme } from '@mui/material/styles';
import RedButton from '../Components/RedButton';
import TextField from '@mui/material/TextField';

function Join( {goBack} ) {
    const theme = useTheme();

    return(
        <div>
            <TextField id="outlined-basic" label="Name" variant="outlined" /><br/>
            <TextField id="outlined-basic" label="Room Code" variant="outlined" /><br/>
            <RedButton label={'Join Game'} onClick={console.log("")}/><br/>
            <RedButton label={'Go Back'} onClick={goBack}/>
        </div>
    )
};
  
 export default Join;