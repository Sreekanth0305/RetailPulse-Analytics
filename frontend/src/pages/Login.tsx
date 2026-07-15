import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  Box,
  Button,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import { login } from "../services/authService";
import "../styles/login.css";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await login(email, password);

      console.log(response.data);

      localStorage.setItem(
      "access_token",
      response.data.access_token
    );
    
    localStorage.setItem(
      "refresh_token",
      response.data.refresh_token
    );
    
    navigate("/dashboard");
    } catch (error: any) {
      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );
    }
  };

  return (
    <Box className="login-container">
      <Paper
        className="login-card"
        elevation={5}
      >
        <Typography
          className="login-title"
          variant="h4"
        >
          RetailPulse
        </Typography>

        <Typography
          className="login-subtitle"
          variant="body1"
        >
          Analytics Platform
        </Typography>

        <TextField
          label="Email"
          variant="outlined"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <TextField
          label="Password"
          type="password"
          variant="outlined"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <Button
          variant="contained"
          fullWidth
          className="login-button"
          onClick={handleLogin}
        >
          Login
        </Button>

        <Typography className="register-text">

          Don't have an account?
        
          <Link
            to="/register"
            className="register-link"
          >
            Register Now
          </Link>
        
        </Typography>
      </Paper>
    </Box>
  );
}

export default Login;