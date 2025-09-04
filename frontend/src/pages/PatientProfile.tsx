import React, { useState } from 'react';
import { UserIcon, PencilIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface PatientInfo {
  firstName: string;
  lastName: string;
  dateOfBirth: string;
  gender: string;
  phone: string;
  email: string;
  address: string;
  emergencyContact: string;
  emergencyPhone: string;
  allergies: string;
  medications: string;
  medicalHistory: string;
}

const PatientProfile: React.FC = () => {
  const [isEditing, setIsEditing] = useState(false);
  const [patientInfo, setPatientInfo] = useState<PatientInfo>({
    firstName: 'John',
    lastName: 'Doe',
    dateOfBirth: '1985-06-15',
    gender: 'Male',
    phone: '+1-555-0123',
    email: 'john.doe@email.com',
    address: '123 Main St, Jerusalem, Israel',
    emergencyContact: 'Jane Doe',
    emergencyPhone: '+1-555-0124',
    allergies: 'Penicillin, Shellfish',
    medications: 'Lisinopril 10mg daily',
    medicalHistory: 'Hypertension, Type 2 Diabetes'
  });

  const handleSave = () => {
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  const handleInputChange = (field: keyof PatientInfo, value: string) => {
    setPatientInfo(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Patient Profile</h1>
          <p className="mt-2 text-gray-600">
            Manage your personal health information
          </p>
        </div>
        <div className="flex space-x-3">
          {!isEditing ? (
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PencilIcon className="h-4 w-4 mr-2" />
              Edit Profile
            </button>
          ) : (
            <>
              <button
                onClick={handleCancel}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <XMarkIcon className="h-4 w-4 mr-2" />
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <CheckIcon className="h-4 w-4 mr-2" />
                Save Changes
              </button>
            </>
          )}
        </div>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex items-center mb-6">
            <div className="h-20 w-20 rounded-full bg-gray-200 flex items-center justify-center">
              <UserIcon className="h-12 w-12 text-gray-400" />
            </div>
            <div className="ml-6">
              <h2 className="text-2xl font-bold text-gray-900">
                {patientInfo.firstName} {patientInfo.lastName}
              </h2>
              <p className="text-gray-600">Patient ID: PAT-2024-001</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-gray-700">First Name</label>
              {isEditing ? (
                <input
                  type="text"
                  value={patientInfo.firstName}
                  onChange={(e) => handleInputChange('firstName', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.firstName}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Last Name</label>
              {isEditing ? (
                <input
                  type="text"
                  value={patientInfo.lastName}
                  onChange={(e) => handleInputChange('lastName', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.lastName}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Date of Birth</label>
              {isEditing ? (
                <input
                  type="date"
                  value={patientInfo.dateOfBirth}
                  onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.dateOfBirth}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Gender</label>
              {isEditing ? (
                <select
                  value={patientInfo.gender}
                  onChange={(e) => handleInputChange('gender', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.gender}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Phone</label>
              {isEditing ? (
                <input
                  type="tel"
                  value={patientInfo.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.phone}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              {isEditing ? (
                <input
                  type="email"
                  value={patientInfo.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.email}</p>
              )}
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Address</label>
              {isEditing ? (
                <textarea
                  value={patientInfo.address}
                  onChange={(e) => handleInputChange('address', e.target.value)}
                  rows={2}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.address}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Emergency Contact</label>
              {isEditing ? (
                <input
                  type="text"
                  value={patientInfo.emergencyContact}
                  onChange={(e) => handleInputChange('emergencyContact', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.emergencyContact}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Emergency Phone</label>
              {isEditing ? (
                <input
                  type="tel"
                  value={patientInfo.emergencyPhone}
                  onChange={(e) => handleInputChange('emergencyPhone', e.target.value)}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.emergencyPhone}</p>
              )}
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Allergies</label>
              {isEditing ? (
                <textarea
                  value={patientInfo.allergies}
                  onChange={(e) => handleInputChange('allergies', e.target.value)}
                  rows={2}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.allergies}</p>
              )}
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Current Medications</label>
              {isEditing ? (
                <textarea
                  value={patientInfo.medications}
                  onChange={(e) => handleInputChange('medications', e.target.value)}
                  rows={3}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.medications}</p>
              )}
            </div>

            <div className="sm:col-span-2">
              <label className="block text-sm font-medium text-gray-700">Medical History</label>
              {isEditing ? (
                <textarea
                  value={patientInfo.medicalHistory}
                  onChange={(e) => handleInputChange('medicalHistory', e.target.value)}
                  rows={4}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              ) : (
                <p className="mt-1 text-sm text-gray-900">{patientInfo.medicalHistory}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PatientProfile;
