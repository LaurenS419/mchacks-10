import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';

export default function NavBar({ navbar }) {
    return (
        <>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar position="static">
                    <Toolbar>
                        <Button color="inherit" component="div">
                            Analytics
                        </Button>
                        <Button color="inherit" component="div">
                            Download
                        </Button>
                        <Button color="inherit">Login</Button>
                    </Toolbar>
                </AppBar>
            </Box>
        </>
    );
}

//export default NavBar;


/*
class FileUpload extends Component {
    state = {
      selectedFile: null
    };
    onFileChange = event => {
      this.setState({ selectedFile: event.target.files[0] });
    };
    onFileUpload = () => {
      const formData = new FormData();
      formData.append(
        "myFile",
        this.state.selectedFile,
        this.state.selectedFile.name
      );

      console.log(this.state.selectedFile);
      axios.post("api/uploadfile", formData);
    };

    fileData = () => {
      if (this.state.selectedFile) {
        return (
          <div>
            <h4>Uploaded!</h4>
          </div>
          //
          <div>
            <h2>File Details:</h2>
            <p>File Name: {this.state.selectedFile.name}</p>
            <p>File Type: {this.state.selectedFile.type}</p>
            <p>
              Last Modified:{" "}
              {this.state.selectedFile.lastModifiedDate.toDateString()}
            </p>
          </div>
        //
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
  
      render() {
        return (
          <div>
            <h1>
              PDF Analyzer
            </h1>
            <div>
              <input type="file" onChange={this.onFileChange} />
              <button onClick={this.onFileUpload}>
                Upload
              </button>
  
            </div>
            {this.fileData()}
          </div>
        );
      }
    }
*/
