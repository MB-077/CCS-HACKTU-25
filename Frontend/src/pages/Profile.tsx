import React, { useEffect, useState } from 'react';
import Breadcrumb from '../components/Breadcrumbs/Breadcrumb';
import CoverOne from '../images/cover/cover-01.png';
import userSix from '../images/user/user-06.png';
import { Link } from 'react-router-dom';

const Profile = () => {
  const [userData, setUserData] = useState({
    first_name: 'John',
    last_name: 'Doe',
    phone_number: '123-456-7890',
    email: 'john.doe@example.com',
    address: '123 Main St, Springfield',
    land_area: '500 sq ft',
    latitude: '12.9716', // Dummy value
    longitude: '77.5946', // Dummy value
    profileImage: userSix,
    coverImage: CoverOne,
  });

  const handleProfileImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUserData((prevData) => ({
          ...prevData,
          profileImage: reader.result,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCoverImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUserData((prevData) => ({
          ...prevData,
          coverImage: reader.result,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch('/api/user/profile'); // Adjust the API endpoint as needed
        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        } else {
          console.error('Failed to fetch user data');
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, []);

  return (
    <>
      <Breadcrumb pageName="Profile" />

      <div className="overflow-hidden rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="relative z-20 h-35 md:h-65">
        <img
            src={CoverOne}
            alt="profile cover"
            className="h-full w-full rounded-tl-sm rounded-tr-sm object-cover object-center"
          />
          <div className="absolute bottom-1 right-1 z-10 xsm:bottom-4 xsm:right-4">
            <label
              htmlFor="cover"
              className="flex cursor-pointer items-center justify-center gap-2 rounded bg-primary py-1 px-2 text-sm font-medium text-white hover:bg-opacity-90 xsm:px-4"
            >
              <input type="file" name="cover" id="cover" className="sr-only" onChange={handleCoverImageChange} />
              <span>Edit</span>
            </label>
          </div>
        </div>
        <div className="px-4 pb-6 text-center lg:pb-8 xl:pb-11.5">
          <div className="relative z-30 mx-auto -mt-22 h-30 w-full max-w-30 rounded-full bg-white/20 p-1 backdrop-blur sm:h-44 sm:max-w-44 sm:p-3">
            <div className="relative drop-shadow-2">
              <img src={userData.profileImage} alt="profile" className="rounded-full" />
              <label
                htmlFor="profile"
                className="absolute bottom-0 right-0 flex h-8.5 w-8.5 cursor-pointer items-center justify-center rounded-full bg-primary text-white hover:bg-opacity-90 sm:bottom-2 sm:right-2"
              >
                <input
                  type="file"
                  name="profile"
                  id="profile"
                  className="sr-only"
                  onChange={handleProfileImageChange}
                />
                <span>Edit</span>
              </label>
            </div>
          </div>
          <div className="mt-4">
            <h3 className="mb-1.5 text-2xl font-semibold text-black dark:text-white">
              {userData.first_name} {userData.last_name}
            </h3>
            <p className="font-medium">{userData.email}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <div>
              <h4 className="mb-3.5 font-medium text-black dark:text-white">Address</h4>
              <p>{userData.address}</p>
            </div>
            <div>
              <h4 className="mb-3.5 font-medium text-black dark:text-white">Land Area</h4>
              <p>{userData.land_area}</p>
            </div>
            <div>
              <h4 className="mb-3.5 font-medium text-black dark:text-white">Location</h4>
              <p>{userData.latitude}</p>
            </div>
            <div>
              <h4 className="mb-3.5 font-medium text-black dark:text-white">Longitude</h4>
              <p>{userData.longitude}</p>
            </div>
          </div>

          <div className="mt-6">
            <h4 className="mb-3.5 font-medium text-black dark:text-white">Notification Preferences</h4>
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center">
                <input type="checkbox" id="emailNotifications" className="mr-2" />
                <label htmlFor="emailNotifications">Email Notifications</label>
              </div>
              <div className="flex items-center">
                <input type="checkbox" id="pushNotifications" className="mr-2" />
                <label htmlFor="pushNotifications">Push Notifications</label>
              </div>
              <div className="flex items-center">
                <input type="checkbox" id="smsNotifications" className="mr-2" disabled />
                <label htmlFor="smsNotifications" className="text-gray-500">SMS (available soon)</label>
              </div>
            </div>
          </div>

          <div className="mt-6">
            <h4 className="mb-3.5 font-medium text-black dark:text-white">Additional General Settings</h4>
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center">
                <label className="mr-2">Language:</label>
                <select className="rounded border border-stroke bg-gray py-2 px-3">
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                </select>
              </div>
              <div className="flex items-center">
                <label className="mr-2">Theme:</label>
                <select className="rounded border border-stroke bg-gray py-2 px-3">
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Profile;