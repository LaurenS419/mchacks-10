import { SystemSecurityUpdate } from '@mui/icons-material';
import axios from 'axios';
import React, { Component } from 'react';
import './index.css';
import { useEffect, useState } from 'react'

function FileUpload(props) {
    const [selectedFile, setSelectedFile] = useState('');

    const onFileChange = event => {
        setSelectedFile(event.target.files[0]);
    };

    const fetchData = () => {

        var input = document.querySelector('input[type="file"]')

        let formData = new FormData()
        formData.append('files', selectedFile);

        let payload = {
            method: 'POST',
            body: formData
        }

        let pdfText;

        console.log(formData.get('files'));

        // Pass this file to the backend
        // Backend will receive data, then return pdf
        // Receive pdf from backend then console log and see what it returns

        fetch('http://127.0.0.1:8000/pdf-analysis', payload)
            .then(data => data.text())
            .then(text => { props.setData(text) })


    }

    const fileData = () => {
        if (selectedFile) {
            return (
                <div>
                    <br />
                    <h4>Uploaded!</h4>
                </div>
                /*
                <div>
                  <h2>File Details:</h2>
                  <p>File Name: {this.state.selectedFile.name}</p>
                  <p>File Type: {this.state.selectedFile.type}</p>
                  <p>
                    Last Modified:{" "}
                    {this.state.selectedFile.lastModifiedDate.toDateString()}
                  </p>
                </div>
                */
            );
        } else {
            return (
                <div>
                    <br />
                    <h4>Nothing uploaded</h4>
                </div >
            );
        }
    };


    return (
        <div>
            <div>
                <input type="file" onChange={onFileChange} />
                <button onClick={() => fetchData()}>
                    Upload
                </button>

            </div>
            {fileData()}
        </div>
    );

}

export default FileUpload;