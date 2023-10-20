import ReactDOM from 'react-dom/client';
import App from './App';

import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { green, lime } from '@mui/material/colors';

const theme = createTheme({
  palette: {
    primary: green,
    secondary: lime,
  },
});


ReactDOM.createRoot(document.getElementById('root')).render(
    <ThemeProvider theme={theme}>
        <App />
    </ThemeProvider>
);
