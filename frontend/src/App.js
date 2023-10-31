import HomePage from './Home/HomePage';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { red } from '@mui/material/colors';


const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#050239',
    },
    button: {
      buttonRed: red[900],
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline>
        <div className="App">
          <HomePage/>
        </div>
      </CssBaseline>
    </ThemeProvider>
  );
}

export default App;
