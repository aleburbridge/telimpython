import { useTheme } from '@mui/material/styles';
import Button from '@mui/material/Button';

function RedButton({ label, onClick }) {
    const theme = useTheme();

    return (
        <Button
            onClick={onClick}
            size="large"
            variant="contained"
            style={{
            backgroundColor: theme.palette.button.buttonRed,
            color: 'white',
            minWidth: '12em'
            }}
            sx={{ mt: 2 }}
        >
            {label}
        </Button>
    );
}

export default RedButton;