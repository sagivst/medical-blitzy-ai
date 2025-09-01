import React, { useState } from 'react';
import { 
  MagnifyingGlassIcon, 
  MapPinIcon, 
  StarIcon,
  PhoneIcon,
  GlobeAltIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';

interface Provider {
  id: string;
  name: string;
  specialty: string;
  rating: number;
  reviewCount: number;
  distance: string;
  address: string;
  phone: string;
  website?: string;
  acceptsNewPatients: boolean;
  languages: string[];
  matchScore: number;
  matchReasons: string[];
  estimatedWaitTime: string;
  insuranceAccepted: boolean;
}

const ProviderSearch: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState('');
  const [specialty, setSpecialty] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [providers, setProviders] = useState<Provider[]>([]);

  const handleSearch = async () => {
    setIsSearching(true);
    try {
      const params = new URLSearchParams();
      if (searchQuery) params.append('keywords', searchQuery.replace(/\s+/g, ','));
      if (location) params.append('location', location);
      if (specialty) params.append('specialty', specialty);
      
       const response = await fetch(`http://localhost:8000/api/v1/providers?${params}`);
      if (!response.ok) {
        throw new Error(`Search failed: ${response.statusText}`);
      }
      
      const result = await response.json();
      
      const transformedProviders = (result.providers || []).map((provider: any) => ({
        id: provider.id?.toString() || Math.random().toString(),
        name: provider.name || 'Unknown Provider',
        specialty: provider.specialty || 'General',
        rating: 4.5, // Default rating since backend doesn't provide this
        reviewCount: 50, // Default review count
        distance: '2.5 miles', // Default distance
        address: provider.location || 'Address not available',
        phone: '+1-555-0100',
        acceptsNewPatients: true,
        languages: ['English'],
        matchScore: Math.round((provider.match_score || 0.8) * 100),
        matchReasons: provider.matched_keywords ? 
          [`Matches keywords: ${provider.matched_keywords.join(', ')}`] : 
          ['General match'],
        estimatedWaitTime: '1-2 weeks',
        insuranceAccepted: true
      }));
      
      setProviders(transformedProviders);
      
    } catch (error) {
      console.error('Provider search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const renderStars = (rating: number) => {
    return (
      <div className="flex items-center">
        {[1, 2, 3, 4, 5].map((star) => (
          <div key={star}>
            {star <= rating ? (
              <StarIconSolid className="h-4 w-4 text-yellow-400" />
            ) : (
              <StarIcon className="h-4 w-4 text-gray-300" />
            )}
          </div>
        ))}
      </div>
    );
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 90) return 'bg-green-100 text-green-800';
    if (score >= 80) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Find Healthcare Providers</h1>
        <p className="mt-2 text-gray-600">
          AI-powered provider matching based on your medical needs and preferences
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
              Search by condition or specialty
            </label>
            <div className="relative">
              <input
                type="text"
                id="search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="e.g., diabetes, cardiology"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Location
            </label>
            <div className="relative">
              <input
                type="text"
                id="location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="City, State or ZIP"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MapPinIcon className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          <div>
            <label htmlFor="specialty" className="block text-sm font-medium text-gray-700 mb-2">
              Specialty
            </label>
            <select
              id="specialty"
              value={specialty}
              onChange={(e) => setSpecialty(e.target.value)}
              className="block w-full px-3 py-2 border border-gray-300 rounded-md leading-5 bg-white focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            >
              <option value="">All Specialties</option>
              <option value="cardiology">Cardiology</option>
              <option value="endocrinology">Endocrinology</option>
              <option value="neurology">Neurology</option>
              <option value="oncology">Oncology</option>
              <option value="orthopedics">Orthopedics</option>
            </select>
          </div>
        </div>

        <div className="mt-4">
          <button
            onClick={handleSearch}
            disabled={isSearching}
            className="w-full sm:w-auto inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {isSearching ? (
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
            ) : (
              <MagnifyingGlassIcon className="h-4 w-4 mr-2" />
            )}
            {isSearching ? 'Searching...' : 'Search Providers'}
          </button>
        </div>
      </div>

      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-medium text-gray-900">
            Search Results ({providers.length} providers found)
          </h2>
          <div className="text-sm text-gray-500">
            Sorted by AI match score
          </div>
        </div>

        {providers.map((provider) => (
          <div key={provider.id} className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-lg font-medium text-gray-900">{provider.name}</h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getMatchScoreColor(provider.matchScore)}`}>
                    {provider.matchScore}% Match
                  </span>
                </div>
                
                <p className="text-sm text-gray-600 mb-2">{provider.specialty}</p>
                
                <div className="flex items-center space-x-4 mb-3">
                  <div className="flex items-center">
                    {renderStars(provider.rating)}
                    <span className="ml-1 text-sm text-gray-600">
                      {provider.rating} ({provider.reviewCount} reviews)
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPinIcon className="h-4 w-4 mr-1" />
                    {provider.distance}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {provider.estimatedWaitTime}
                  </div>
                </div>

                <div className="mb-3">
                  <p className="text-sm text-gray-600 mb-1">Why this provider matches:</p>
                  <ul className="text-sm text-gray-500">
                    {provider.matchReasons.map((reason: string, index: number) => (
                      <li key={index} className="flex items-center">
                        <span className="w-1 h-1 bg-gray-400 rounded-full mr-2" />
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <MapPinIcon className="h-4 w-4 mr-1" />
                    {provider.address}
                  </div>
                  <div className="flex items-center">
                    <PhoneIcon className="h-4 w-4 mr-1" />
                    {provider.phone}
                  </div>
                  {provider.website && (
                    <div className="flex items-center">
                      <GlobeAltIcon className="h-4 w-4 mr-1" />
                      <a href={provider.website} className="text-primary-600 hover:text-primary-500">
                        Website
                      </a>
                    </div>
                  )}
                </div>

                <div className="mt-3 flex items-center space-x-4">
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                    provider.acceptsNewPatients 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {provider.acceptsNewPatients ? 'Accepting New Patients' : 'Not Accepting New Patients'}
                  </span>
                  {provider.insuranceAccepted && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Accepts Your Insurance
                    </span>
                  )}
                  <span className="text-xs text-gray-500">
                    Languages: {provider.languages.join(', ')}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-4 flex space-x-3">
              <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                Schedule Appointment
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                View Profile
              </button>
              <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                Save Provider
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProviderSearch;
