import { React, useState } from 'react';
import Link from '@mui/material/Link';
import { useTheme } from '@mui/material/styles';
import AnimatedHeader from './AnimatedHeader';
import Button from '@mui/material/Button';
import Join from './Join';
import Create from './Create';
import Footer from './Footer';

function HomePage() {
    const theme = useTheme();
    const [showDescription, setShowDescription] = useState(false);
    const [pageState, setPageState] = useState('default');

    const handleDescriptionClick = () => {
        setShowDescription(!showDescription);
    }
  
    return (
        <div style={{ textAlign: 'center' }}>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: theme.spacing(8) }}>
                <AnimatedHeader />
            </div>

            {pageState === 'default' && (
                <div>
                    <Button onClick={() => setPageState('join')}size="large" variant="contained" style={{ backgroundColor: theme.palette.button.buttonRed, color: 'white' }} sx={{ mt: 2 }}>Join Game</Button><br/>
                    <Button onClick={() => setPageState('create')} size="large" variant="contained" style={{ backgroundColor: theme.palette.button.buttonRed, color: 'white' }} sx={{ mt: 2 }}>Create Game</Button><br/>
                </div>
            )}
            {pageState === 'join' && (
                <Join/>
            )}
            {pageState === 'create' && (
                <Create/>
            )}

            <Link style={{ display: 'block', marginTop: theme.spacing(2) }} onClick={handleDescriptionClick}>What is Telimpromptu?</Link>
            {showDescription && (
                <p>
                I'M GLAD YOU ASKED<br/>Telimpromptu is a party game for 2-8 people that has all players<br/>respond to prompts
                ad-libs style and then read off of a teleprompter<br/> at the end like they are giving a fake news report.<br/>
                But that's not all! Lorem ipsum dolor sit amet
                </p>
            )}

            <Footer/>
        </div>
    );
}

export default HomePage;