import axios from 'axios';
import React, { Component } from 'react';
import './index.css';
import { NavLink, Routes, Route } from 'react-router-dom';
//import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { Link } from 'react-router-dom';
import FileUpload from './fileUpload';
import analyze from './analyze.py'


const App = () => (
  <div className='app'>
    <Navigation />
    <Main />

  </div>

);


const Navigation = () => (
  <Box sx={{ flexGrow: 1 }}>
    <AppBar position="fixed">
      <Toolbar>
        <Button color="inherit" component={Link} to="/home">
          Home
        </Button>
        <Button color="inherit" component={Link} to="/analytics">
          Analytics
        </Button>
        <Button color="inherit" component={Link} to="/about">
          About
        </Button>
      </Toolbar>
    </AppBar>
  </Box>

);


function Home() {
  return (
    <>
      <div className='home'>
        <h1>PDF Analyzer</h1>
        <p> Upload a pdf below!</p>
      </div>

      <FileUpload />
    </>
  )
}

/*
function doAnalyze() {
  result = 

  //const fobj = axios.get("api/uploadfile", formData)
  return result
}
*/


const Analytics = () => (
  <div className='analytics'>
    <h1>Analytics</h1>
    <p>text</p>
    <p></p>
  </div>


);



const About = () => (
  <div className='about'>
    <h1>About Us</h1>
    <p>McHacks 10 Team from McGill</p>
  </div>
);

const Main = () => (
  <Routes>
    <Route exact path='/home' element={<Home />}></Route>
    <Route exact path='/analytics' element={<Analytics />} />
    <Route exact path='/about' element={<About />} />
  </Routes>
);


export default App;


