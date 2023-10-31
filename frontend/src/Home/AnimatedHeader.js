import { React, useEffect, useRef, useState } from 'react';
import { useTheme } from '@mui/material/styles';

function AnimatedHeader() {
    const theme = useTheme();

    const h1Ref = useRef(null);
    const [imgHeight, setImgHeight] = useState(null);

    const [leftImage, setLeftImage] = useState('/left_cool_lines_1.png');
    const [rightImage, setRightImage] = useState('/right_cool_lines_1.png');
  
    useEffect(() => {
        if (h1Ref.current) {
          const lineHeight = parseFloat(getComputedStyle(h1Ref.current).lineHeight);
          setImgHeight(lineHeight);
        }
      }, []);

    useEffect(() => {
      const timer = setInterval(() => {
        setLeftImage(prev => (prev === '/left_cool_lines_1.png' ? '/left_cool_lines_2.png' : '/left_cool_lines_1.png'));
        setRightImage(prev => (prev === '/right_cool_lines_1.png' ? '/right_cool_lines_2.png' : '/right_cool_lines_1.png'));
      }, 500);
  
      return () => clearInterval(timer);
    }, []);
  
    return (
        <div style={{ display: 'flex', alignItems: 'center' }}>
            <img src={leftImage} alt="Left Cool Lines" style={{ height: imgHeight }} />
            <h1 ref={h1Ref}  style={{ marginLeft: theme.spacing(2), marginRight: theme.spacing(2)}}>Telimpromptu</h1>
            <img src={rightImage} alt="Right Cool Lines" style={{ height: imgHeight }} />
        </div>
    )
}

export default AnimatedHeader;