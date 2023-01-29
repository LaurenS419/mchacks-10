import { SystemSecurityUpdate } from '@mui/icons-material';
import axios from 'axios';
import React, { Component } from 'react';
import './index.css';
import { useEffect, useState } from 'react'

function FileUpload() {
    const [selectedFile, setSelectedFile] = useState('');
    const [data, setData] = useState('');

    const onFileChange = event => {
        setSelectedFile(event.target.files[0]);
    };

    // Calls when page is loaded
    useEffect(() => {
        fetchData()
    }, []);

    const fetchData = () => {
        const fileToUpload = selectedFile;

        var input = document.querySelector('input[type="file"]')

        var data = new FormData()
        data.append('file', fileToUpload)

        // Pass this file to the backend
        // Backend will receive data, then return pdf
        // Receive pdf from backend then console log and see what it returns

        fetch('http://127.0.0.1:5000/pdf-analysis', {
            method: 'POST',
            body: data
        })

        // Test enpoint (remove eventually)
        fetch("http://127.0.0.1:5000/test")
            .then((response) => response.text())
            .then((data) => console.log(data));
    }
    const onFileUpload = () => {





        /*
        const formData = new FormData();
        formData.append(
            "myFile",
            this.state.selectedFile,
            this.state.selectedFile.name
        );

        console.log(this.state.selectedFile);
        axios.post("api/uploadfile", formData).then(data => {
            console.log();
        });
        */
    };

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
                <button onClick={fetchData}>
                    Upload
                </button>

            </div>
            {fileData()}
        </div>
    );

}

export default FileUpload;