import { useState } from "react";
import { Link } from "react-router-dom";

import {
  Box,
  Button,
  Paper,
  TextField,
  MenuItem,
  Typography,
  Grid
} from "@mui/material";

import { registerCompany } from "../services/companyService";
import { useNavigate } from "react-router-dom";

import "../styles/registerCompany.css";

function RegisterCompany() {

  const navigate = useNavigate();
  const [companyName, setCompanyName] = useState("");
  const [industry, setIndustry] = useState("");
  const [companyEmail, setCompanyEmail] = useState("");
  const [companyPhone, setCompanyPhone] = useState("");
  const [role, setRole] = useState("");
  const [address, setAddress] = useState("");

  const [adminName, setAdminName] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleRegister = async () => {

    if (password !== confirmPassword) {
  
      alert("Passwords do not match.");
  
      return;
  
    }
  
    try {
  
      const data = {
  
         name: companyName,
         industry: industry,
         email: companyEmail,
         phone: companyPhone,
         address: address,
       
         admin_name: adminName,
         admin_email: adminEmail,
         admin_password: password
  
      };
  
        await registerCompany(data);

        alert("Company Registered Successfully");
    
        navigate("/");
    
  
    }
  
    catch (error: any) {
  
      alert(
        error.response?.data?.detail ||
        "Registration Failed"
      );
  
    }
  
  };
  return (

    <Box className="register-container">

      <Paper
        elevation={5}
        className="register-card"
      >

        <Typography
          variant="h4"
          className="register-title"
        >
          Register Company
        </Typography>

        <Typography
          className="register-subtitle"
        >
          Create your RetailPulse account
        </Typography>

        <Grid container spacing={2}>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Company Name"
              value={companyName}
              onChange={(e)=>setCompanyName(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Industry"
              value={industry}
              onChange={(e)=>setIndustry(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Company Email"
              value={companyEmail}
              onChange={(e)=>setCompanyEmail(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Company Phone"
              value={companyPhone}
              onChange={(e)=>setCompanyPhone(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              select
              fullWidth
              label="Role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
          
              <MenuItem value="Company Admin">
                Company Admin
              </MenuItem>
          
              <MenuItem value="Analyst">
                Analyst
              </MenuItem>
          
              <MenuItem value="Viewer">
                Viewer
              </MenuItem>
          
              <MenuItem value="Super Admin">
                Super Admin
              </MenuItem>
          
            </TextField>
          
          </Grid>

          <Grid size={12}>

            <TextField
              fullWidth
              multiline
              rows={2}
              label="Address"
              value={address}
              onChange={(e)=>setAddress(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Admin Name"
              value={adminName}
              onChange={(e)=>setAdminName(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              label="Admin Email"
              value={adminEmail}
              onChange={(e)=>setAdminEmail(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              type="password"
              label="Password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
            />

          </Grid>

          <Grid size={{ xs: 12, md: 6 }}>

            <TextField
              fullWidth
              type="password"
              label="Confirm Password"
              value={confirmPassword}
              onChange={(e)=>setConfirmPassword(e.target.value)}
            />

          </Grid>

        </Grid>

        <Button
          fullWidth
          variant="contained"
          className="register-button"
          onClick={handleRegister}
        >
          Register Company
        </Button>

        <Typography className="login-link">

          Already have an account?

          <Link
            to="/"
            className="back-login"
          >
            Login
          </Link>

        </Typography>

      </Paper>

    </Box>

  );

}

export default RegisterCompany;