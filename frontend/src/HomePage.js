import Button from '@mui/material/Button';
import { useTheme } from '@mui/material/styles';

function HomePage() {
    const theme = useTheme();

    return (
        <div className="App">
            <h1>Telimpromptu 📺</h1>
            <Button size="large" variant="contained" style={{ backgroundColor: theme.palette.button.buttonRed, color: 'white' }} sx={{ mt: 2 }}>Join Game</Button><br/>
            <Button size="large" variant="contained" style={{ backgroundColor: theme.palette.button.buttonRed, color: 'white' }} sx={{ mt: 2 }}>Create Game</Button>
        </div>
    );
}

export default HomePage;