import { React, useState } from 'react';
import { useTheme } from '@mui/material/styles';
import Link from '@mui/material/Link';
import useMediaQuery from '@mui/material/useMediaQuery';
import AnimatedHeader from './AnimatedHeader';
import Join from './Join';
import Create from './Create';
import Footer from './Footer';
import RedButton from '../Components/RedButton';

function HomePage() {
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    
    const [showDescription, setShowDescription] = useState(false);
    const [pageState, setPageState] = useState('default');

    const handleDescriptionClick = () => {
        setShowDescription(!showDescription);
    }
  
    return (
        <div style={{ textAlign: 'center' }}>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: isMobile ? theme.spacing(4) : theme.spacing(8) }}>
                <AnimatedHeader />
            </div>

            {pageState === 'default' && (
                <div>
                    <RedButton label={'Join Game'} onClick={() => setPageState('join')}/><br/>
                    <RedButton label={'Create Game'} onClick={() => setPageState('create')}/>
                </div>
            )}
            {pageState === 'join' && (
                <Join goBack={ () => setPageState('default') }/>
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