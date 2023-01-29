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
import { useEffect, useState } from 'react'


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
          Raw Text
        </Button>
      </Toolbar>
    </AppBar>
  </Box>

);

function Home(props) {


  return (
    <>
      <div className='home'>
        <h1>PDF Analyzer</h1>
        <p> Upload a pdf below!</p>
      </div>

      <FileUpload data={props.data} setData={props.setData} />
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
    <h3>Download the MP3 Recording of your PDF: <a href="https://drive.google.com/file/d/1iN4qkzQWBE9f1qeTBnODTFLYU8KCeZOE/view?usp=sharing">HERE</a> </h3>
    <h3>Analytics downloaded!</h3>
    <p></p>
  </div>


);



const About = (props) => (
  <div className='about'>
    <h1>Text</h1>
    <p>{props.data}</p>
  </div>
);

const Main = () => {
  const [data, setData] = useState('');
  return (
    <Routes>
      <Route exact path='/home' element={<Home data={data} setData={setData} />}></Route>
      <Route exact path='/analytics' element={<Analytics />} />
      <Route exact path='/about' element={<About data={data} setData={setData} />} />
    </Routes>
  )
};


export default App;


