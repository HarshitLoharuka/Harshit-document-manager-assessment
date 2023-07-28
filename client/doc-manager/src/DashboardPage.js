
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import './DashboardPage.css'; // Import the SCSS file

const DashboardPage = () => {
  const styles = {
    textAlign: 'center',
    marginTop: '3rem',
  };

  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');
  const [fileVersions, setFileVersions] = useState([]);
  const [selectedVersion, setSelectedVersion] = useState('');
  const [fetchData, setFetchData] = useState(false);
  const [fileData, setFileData] = useState(null); // Define the fileData state variable
  const [successMessage, setSuccessMessage] = useState('');


  const API_URL = 'http://localhost:8001/api';

  const location = useLocation();
  const token = location.state?.token || '';

  

  const handleFileSelect = (event) => {
    const selectedFile = event.target.value;
    console.log('Selected File:', selectedFile);

    setSelectedFile(selectedFile); // Save the selected file in the state

    // Fetch file versions for the selected file
    fetchFileVersions(selectedFile);

    // You may also consider resetting selected version and success message when a new file is selected
    setSelectedVersion('');
    setSuccessMessage('');
  };

   
  
  const fetchFiles = async () => {
    try {
      const response = await axios.get(`${API_URL}/get-unique-files/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });
      setFiles(response.data.unique_files); // Assuming the API returns data in JSON format
      console.log('files value ', response.data.unique_files);
      fetchFileVersions(selectedFile);
    } catch (error) {
      console.error('Error fetching unique files:', error);
      setFiles([]); // Set files as an empty array to handle the error scenario
    }
  };

  useEffect(() => {
    fetchFiles();
  }, [token]);


  const fetchFileVersions = async (selectedFile) => {
    try {
      if (selectedFile) {
        const response = await axios.get(
          `${API_URL}/get-file-versions/?file_name=${selectedFile}`,
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        setFileVersions(response.data.versions);
        console.log('File versions:', response.data.versions);
       
      } else {
        setFileVersions([]);
      }
    } catch (error) {
      console.error('Error fetching file versions:', error);
      setFileVersions([]);
    }
  };


   


  const handleFileChange = async (event) => {
    const selectedFilePath = event.target.value;
    console.log('selectedFilePath ', selectedFilePath);
    const filename = selectedFilePath.split('\\').pop();
    console.log('filename ',filename);
    // Your file upload logic here...

    try {
      // Assuming you have the necessary information to construct the fileData object here
      const fileData = {
        file_name: filename,
        file_url: selectedFilePath,
      };

      const response = await axios.post(`${API_URL}/upload-file/`, fileData, {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      console.log('File upload success:', response.data);
      // Add any further processing of the response data if needed
      fetchFiles();
    } catch (error) {
      console.error('Error uploading file:', error);
      // Handle the error scenario
    }
  };



  const handleVersionChange = (event) => {
    const selectedVersion = event.target.value;
    setSelectedVersion(selectedVersion);
    
  };

  const handleRetrieve = () => {
    console.log('Retrieve file:', selectedFile, 'Version:', selectedVersion);
    setFetchData(true); // Set fetchData to true when the "Retrieve" button is clicked
 
  }
  useEffect(() => {
    // This useEffect will be triggered when fetchData changes to true
    if (fetchData) {
      const fetchFileData = async () => {
        try {
          let url = `${API_URL}/get-file-version/?file_name=${selectedFile}`;
          if (selectedVersion !== '') {
            url += `&revision=${selectedVersion}`;
          }
          const response = await axios.get(url, {
            headers: {
              Authorization: `Token ${token}`,
            },
          });
          setFileData(response.data); 
          console.log('retrieve file ',response.data)
          setSuccessMessage(`File retrieved successfully at the location :`+response.data.file_url);
        } catch (error) {
          console.error('Error fetching file data:', error);
          setFileData(null); // Set fileData to null to handle the error scenario
        } finally {
          // Reset the fetchData state variable to false to prevent useEffect from being triggered on subsequent renders
          setFetchData(false);
        }
      };

      fetchFileData();
    }
  }, [fetchData, selectedFile, selectedVersion]);

 
  return (
    <React.Fragment>
      <div style={styles}><h1>Welcome to Harshit Document Manager Dashboard</h1></div>
      <div className="dashboard-container">
        <div className="dashboard-upload">
          <h2>Upload</h2>
          {/* Add the upload logic and interface here */}
          <input type="file" onChange={handleFileChange} />
        </div>

        <div className="dashboard-retrieve">
          <h2>Retrieve</h2>
          {/* <select value={selectedFile} onChange={handleFileChange}> */}
          <select onChange={handleFileSelect} value={selectedFile}>
          <option value="">Select a file</option>
          {files.map((file) => (
          <option key={file} value={file}>
          {file}
          </option>
       ))}
       </select>

       {selectedFile && (
            <select value={selectedVersion} onChange={handleVersionChange}>
              <option value="">Select a version</option>
              {fileVersions.map((version) => (
                <option key={version} value={version}>
                  {version}
                </option>
              ))}
            </select>
          )}

          <button onClick={handleRetrieve} disabled={!selectedFile }>
            Retrieve
          </button>
          {successMessage && <div className="success-message">{successMessage}</div>}
        </div>
      </div>
    </React.Fragment>
  );
};

export default DashboardPage;
