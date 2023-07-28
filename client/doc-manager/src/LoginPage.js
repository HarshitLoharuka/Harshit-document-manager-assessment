import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import axios from 'axios'; // 


const LoginPage = () => {

  const navigate = useNavigate(); 
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginStatus, setLoginStatus] = useState(null);
  const API_URL = 'http://localhost:8001';
 

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    if (name === 'email') {
      setEmail(value);
    } else if (name === 'password') {
      setPassword(value);
    }
  };


  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      console.log('inside useEffect')
     
      

      const response = await axios.post(`${API_URL}/auth-token/`, {
        username: email,
        password: password,
      });
      
      const token = response.data.token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      
      if (response.status === 200) {

        navigate('/dashboard', { state: { token } });
       
      } else {
        setLoginStatus('error');
   }
     
    } catch (error) {
      setLoginStatus('error');
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={handleInputChange}
            required
          />
        </div>
        <button type="submit">Submit</button>
        {loginStatus === 'error' && <p style={{ color: 'red' }}>User does not exist!</p>}
      </form>
    </div>
  );
};

export default LoginPage;