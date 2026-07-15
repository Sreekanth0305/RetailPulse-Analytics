import { useEffect, useState } from "react";

import { getProfile } from "../services/profileService";

import "../styles/profile.css";

function Profile() {

  const [profile, setProfile] = useState({

    name: "",
    email: "",
    role: "",
    company: "",
    last_login: "",
    status: ""

  });

  const loadProfile = async () => {

    try {

      const response = await getProfile();

      setProfile(response.data);

    }

    catch (error) {

      console.log(error);

    }

  };

  useEffect(() => {

    loadProfile();

  }, []);

  return (

    <div className="profile-container">

      <div className="profile-card">

        <h1>User Profile</h1>

        <hr />

        <div className="profile-row">

          <span>Name</span>

          <p>{profile.name}</p>

        </div>

        <div className="profile-row">

          <span>Email</span>

          <p>{profile.email}</p>

        </div>

        <div className="profile-row">

          <span>Role</span>

          <p>{profile.role}</p>

        </div>

        <div className="profile-row">

          <span>Company</span>

          <p>{profile.company}</p>

        </div>

        <div className="profile-row">

          <span>Last Login</span>

          <p>{profile.last_login}</p>

        </div>

        <div className="profile-row">

          <span>Status</span>

          <p>{profile.status}</p>

        </div>

      </div>

    </div>

  );

}

export default Profile;