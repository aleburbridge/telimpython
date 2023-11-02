import { React, useState, useEffect } from 'react';
import { useTheme } from '@mui/material/styles';
import Link from '@mui/material/Link';
import useMediaQuery from '@mui/material/useMediaQuery';
import AnimatedHeader from './AnimatedHeader';
import Join from './Join';
import Footer from './Footer';
import RedButton from '../Components/RedButton';

//TODO: friendly error messaging
function HomePage() {
    const url = "http://localhost:5000";
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
    
    const [showDescription, setShowDescription] = useState(false);
    const [pageState, setPageState] = useState('default');

    const handleDescriptionClick = () => {
        setShowDescription(!showDescription);
    }

    const handleCreateGame = () => {
        fetch(`${url}/api/generate_room_code`)
        .then((res) => res.json()
        .then((data) => {
                localStorage.setItem("room_code", data.room_code);
                setPageState('create');
            })
        ).catch(error => {
            console.log(error);
        });
    }

    return (
        <div style={{ textAlign: 'center' }}>

            <div style={{ display: 'flex', justifyContent: 'center', marginTop: isMobile ? theme.spacing(4) : theme.spacing(8) }}>
                <AnimatedHeader />
            </div>

            {pageState === 'default' && (
                <div>
                    <RedButton label={'Join Game'} onClick={() => setPageState('join')}/><br/>
                    <RedButton label={'Create Game'} onClick={handleCreateGame}/>
                </div>
            )}
            {pageState === 'join' && (
                <Join goBack={ () => setPageState('default') }/>
            )}
            {pageState === 'create' && (
                <Join isCreating={true} goBack={ () => setPageState('default') }/>
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