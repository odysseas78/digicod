'use client';

import { useEffect } from 'react';

const ViewportSetter = () => {
  useEffect(() => {
    const setViewport = () => {
      const width = screen.width;
      const meta = document.querySelector('meta[name="viewport"]');

      if (meta) {
        if (width && width <= 450) {
          meta.setAttribute('content', 'width=device-width, initial-scale=0.9');
        } else if (width && (width > 449)) {
          meta.setAttribute('content', 'width=device-width, initial-scale=1.0');
        } 
      }
    };

    setViewport();

    window.addEventListener('resize', setViewport);
    return () => {
      window.removeEventListener('resize', setViewport);
    };
  }, []);

  return null;
};

export default ViewportSetter;
