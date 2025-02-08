import { Link } from 'react-router-dom';
import Breadcrumb from '../../components/Breadcrumbs/Breadcrumb';
import { ChangeEvent, FormEvent, useState } from 'react';

interface CropDetails {
  state: string;
  cropGrown: string;
  landArea: number | '';
  plantingDate: string;
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
}

const LoginForm = () => {
  const [formData, setFormData] = useState<CropDetails>({
    state: '',
    cropGrown: '',
    landArea: '',
    plantingDate: '',
    notifications: {
      email: false,
      push: false,
      sms: false,
    },
  });

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    if (type === 'checkbox') {
      setFormData((prev) => ({
        ...prev,
        notifications: { ...prev.notifications, [name]: checked },
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: type === 'number' ? Number(value) || '' : value,
      }));
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <>
      <Breadcrumb pageName="Login Form" />
      <div className="grid grid-cols-1 gap-9 sm:grid-cols-2">
        <div className="flex flex-col gap-9">
          <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
            <div className="border-b border-stroke py-4 px-6.5 dark:border-strokedark">
              <h3 className="font-medium text-black dark:text-white">
                Crop Details Form
              </h3>
            </div>
            <form onSubmit={handleSubmit} className="p-6.5">
              <div className="mb-4.5">
                <label className="mb-2.5 block text-black dark:text-white">
                  State
                </label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  placeholder="Enter your state"
                  className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none focus:border-primary dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-2.5 block text-black dark:text-white">
                  Crop Grown
                </label>
                <input
                  type="text"
                  name="cropGrown"
                  value={formData.cropGrown}
                  onChange={handleChange}
                  placeholder="Enter crop grown"
                  className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none focus:border-primary dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-2.5 block text-black dark:text-white">
                  Land Area (in acres)
                </label>
                <input
                  type="number"
                  name="landArea"
                  value={formData.landArea}
                  onChange={handleChange}
                  placeholder="Enter land area"
                  className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none focus:border-primary dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                />
              </div>

              <div className="mb-4.5">
                <label className="mb-2.5 block text-black dark:text-white">
                  Planting Date
                </label>
                <input
                  type="date"
                  name="plantingDate"
                  value={formData.plantingDate}
                  onChange={handleChange}
                  className="w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 text-black outline-none focus:border-primary dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                />
              </div>

              <div className="mb-4.5">
                <h4 className="mb-2.5 block text-black dark:text-white">
                  Notification Preferences
                </h4>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="emailNotifications"
                    name="email"
                    checked={formData.notifications.email}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <label htmlFor="emailNotifications">
                    Email Notifications
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="pushNotifications"
                    name="push"
                    checked={formData.notifications.push}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <label htmlFor="pushNotifications">Push Notifications</label>
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="smsNotifications"
                    name="sms"
                    checked={formData.notifications.sms}
                    onChange={handleChange}
                    className="mr-2"
                  />
                  <label htmlFor="smsNotifications">SMS Notifications</label>
                </div>
              </div>

              <button
                type="submit"
                className="flex w-full justify-center rounded bg-primary p-3 font-medium text-gray hover:bg-opacity-90"
              >
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginForm;
