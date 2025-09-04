import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  MagnifyingGlassIcon, 
  MapPinIcon, 
  PhoneIcon,
  StarIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface Provider {
  id: number;
  name: string;
  specialty: string;
  location: string;
  keywords: string[];
  rating?: number;
  reviews?: number;
  phone?: string;
  availability?: string;
}

const ProviderSearch: React.FC = () => {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('');
  const [selectedLocation, setSelectedLocation] = useState('');
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const specialties = [
    'All Specialties',
    'Cardiology',
    'Neurology', 
    'Endocrinology',
    'Orthopedics',
    'Dermatology',
    'Psychiatry',
    'Pediatrics',
    'Internal Medicine',
    'Surgery'
  ];

  const locations = [
    'All Locations',
    'Jerusalem',
    'Tel Aviv',
    'Haifa',
    'Beer Sheva',
    'Netanya',
    'Ashdod',
    'Petah Tikva',
    'Rishon LeZion'
  ];

  useEffect(() => {
    searchProviders();
  }, []);

  const searchProviders = async () => {
    setLoading(true);
    setError(null);

    try {
      const params: any = {};
      
      if (selectedSpecialty && selectedSpecialty !== 'All Specialties') {
        params.specialty = selectedSpecialty.toLowerCase();
      }
      
      if (selectedLocation && selectedLocation !== 'All Locations') {
        params.location = selectedLocation;
      }

      const response = await axios.get(`${API_URL}/api/v1/providers`, { params });
      
      let results = response.data.providers || [];
      
      if (searchTerm) {
        results = results.filter((provider: Provider) =>
          provider.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          provider.specialty.toLowerCase().includes(searchTerm.toLowerCase()) ||
          provider.keywords.some(keyword => 
            keyword.toLowerCase().includes(searchTerm.toLowerCase())
          )
        );
      }

      const providersWithDetails = results.map((provider: Provider) => ({
        ...provider,
        rating: provider.id === 1 ? 4.8 : provider.id === 2 ? 4.5 : provider.id === 3 ? 4.7 : 4.6,
        reviews: provider.id === 1 ? 75 : provider.id === 2 ? 50 : provider.id === 3 ? 60 : 45,
        phone: provider.id === 1 ? '+1-555-0101' : provider.id === 2 ? '+1-555-0100' : provider.id === 3 ? '+1-555-0102' : '+1-555-0103',
        availability: provider.id === 1 ? '2-3 weeks' : provider.id === 2 ? '1-2 weeks' : provider.id === 3 ? '1 week' : '3-4 weeks'
      }));

      setProviders(providersWithDetails);
    } catch (error) {
      console.error('Search error:', error);
      setError('Failed to search providers. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    searchProviders();
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, index) => (
      <StarIcon
        key={index}
        className={`h-4 w-4 ${
          index < Math.floor(rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'
        }`}
      />
    ));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Provider Search</h1>
        <p className="mt-2 text-gray-600">
          Find healthcare providers using AI-powered matching
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700">
                Search Term
              </label>
              <div className="mt-1 relative">
                <input
                  type="text"
                  id="search"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Provider name, condition, or keyword..."
                  className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm pl-10"
                />
                <MagnifyingGlassIcon className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              </div>
            </div>

            <div>
              <label htmlFor="specialty" className="block text-sm font-medium text-gray-700">
                Specialty
              </label>
              <select
                id="specialty"
                value={selectedSpecialty}
                onChange={(e) => setSelectedSpecialty(e.target.value)}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                {specialties.map((specialty) => (
                  <option key={specialty} value={specialty}>
                    {specialty}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Location
              </label>
              <select
                id="location"
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              >
                {locations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              <MagnifyingGlassIcon className="h-4 w-4 mr-2" />
              {loading ? 'Searching...' : 'Search Providers'}
            </button>
          </div>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Search Results ({providers.length} providers found)
            </h3>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <p className="mt-2 text-sm text-gray-500">Searching providers...</p>
            </div>
          ) : providers.length === 0 ? (
            <div className="text-center py-8">
              <MagnifyingGlassIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No providers found</h3>
              <p className="mt-1 text-sm text-gray-500">
                Try adjusting your search criteria or browse all providers.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {providers.map((provider) => (
                <div key={provider.id} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h4 className="text-lg font-medium text-gray-900">{provider.name}</h4>
                      <p className="text-sm text-primary-600 font-medium">{provider.specialty}</p>
                      
                      <div className="mt-2 flex items-center text-sm text-gray-500">
                        <MapPinIcon className="h-4 w-4 mr-1" />
                        {provider.location}
                      </div>

                      {provider.phone && (
                        <div className="mt-1 flex items-center text-sm text-gray-500">
                          <PhoneIcon className="h-4 w-4 mr-1" />
                          {provider.phone}
                        </div>
                      )}

                      {provider.availability && (
                        <div className="mt-1 flex items-center text-sm text-gray-500">
                          <ClockIcon className="h-4 w-4 mr-1" />
                          Next available: {provider.availability}
                        </div>
                      )}

                      {provider.keywords.length > 0 && (
                        <div className="mt-3">
                          <p className="text-xs text-gray-500 mb-2">Specializes in:</p>
                          <div className="flex flex-wrap gap-1">
                            {provider.keywords.slice(0, 5).map((keyword, idx) => (
                              <span
                                key={idx}
                                className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                              >
                                {keyword}
                              </span>
                            ))}
                            {provider.keywords.length > 5 && (
                              <span className="text-xs text-gray-500">
                                +{provider.keywords.length - 5} more
                              </span>
                            )}
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="ml-6 text-right">
                      {provider.rating && (
                        <div className="flex items-center mb-2">
                          <div className="flex items-center">
                            {renderStars(provider.rating)}
                          </div>
                          <span className="ml-2 text-sm text-gray-600">
                            {provider.rating} ({provider.reviews} reviews)
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="mt-4 flex space-x-3">
                    <button className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                      Book Appointment
                    </button>
                    <button className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                      View Profile
                    </button>
                    <button className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                      Contact
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProviderSearch;
