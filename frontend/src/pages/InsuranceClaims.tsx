import React, { useState } from 'react';
import { 
  CreditCardIcon, 
  DocumentTextIcon, 
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  PlusIcon
} from '@heroicons/react/24/outline';

interface InsuranceClaim {
  id: string;
  claimNumber: string;
  serviceDate: string;
  provider: string;
  serviceDescription: string;
  amount: number;
  status: 'submitted' | 'processing' | 'approved' | 'denied' | 'appealed';
  submittedDate: string;
  lastUpdated: string;
  insuranceProvider: string;
  copay?: number;
  deductible?: number;
  coinsurance?: number;
  notes?: string;
}

const InsuranceClaims: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'claims' | 'eligibility' | 'appeals'>('claims');
  
  const [claims] = useState<InsuranceClaim[]>([
    {
      id: '1',
      claimNumber: 'CLM-2024-001234',
      serviceDate: '2024-01-15',
      provider: 'Dr. Sarah Johnson - Cardiology',
      serviceDescription: 'Echocardiogram and consultation',
      amount: 850.00,
      status: 'approved',
      submittedDate: '2024-01-16',
      lastUpdated: '2024-01-20',
      insuranceProvider: 'Blue Cross Blue Shield',
      copay: 25.00,
      deductible: 0,
      coinsurance: 170.00
    },
    {
      id: '2',
      claimNumber: 'CLM-2024-001235',
      serviceDate: '2024-01-22',
      provider: 'City Medical Lab',
      serviceDescription: 'Blood work - Comprehensive metabolic panel',
      amount: 180.00,
      status: 'processing',
      submittedDate: '2024-01-23',
      lastUpdated: '2024-01-25',
      insuranceProvider: 'Blue Cross Blue Shield',
      copay: 0,
      deductible: 50.00,
      coinsurance: 26.00
    },
    {
      id: '3',
      claimNumber: 'CLM-2024-001236',
      serviceDate: '2024-01-28',
      provider: 'Dr. Michael Chen - Endocrinology',
      serviceDescription: 'Diabetes management consultation',
      amount: 320.00,
      status: 'denied',
      submittedDate: '2024-01-29',
      lastUpdated: '2024-02-02',
      insuranceProvider: 'Blue Cross Blue Shield',
      notes: 'Prior authorization required for specialist consultation'
    }
  ]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'denied':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      case 'processing':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      case 'appealed':
        return <ExclamationTriangleIcon className="h-5 w-5 text-orange-500" />;
      default:
        return <DocumentTextIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'denied':
        return 'bg-red-100 text-red-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'appealed':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const tabs = [
    { id: 'claims', name: 'Claims', icon: DocumentTextIcon },
    { id: 'eligibility', name: 'Eligibility', icon: CheckCircleIcon },
    { id: 'appeals', name: 'Appeals', icon: ExclamationTriangleIcon }
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Insurance Management</h1>
        <p className="mt-2 text-gray-600">
          Track claims, verify eligibility, and manage insurance appeals
        </p>
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="h-5 w-5 inline mr-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'claims' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-lg font-medium text-gray-900">
                  Insurance Claims ({claims.length})
                </h2>
                <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  <PlusIcon className="h-4 w-4 mr-2" />
                  Submit New Claim
                </button>
              </div>

              <div className="space-y-4">
                {claims.map((claim) => (
                  <div key={claim.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(claim.status)}
                        <div>
                          <h3 className="text-sm font-medium text-gray-900">
                            {claim.claimNumber}
                          </h3>
                          <p className="text-sm text-gray-500">
                            {claim.provider}
                          </p>
                        </div>
                      </div>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(claim.status)}`}>
                        {claim.status.charAt(0).toUpperCase() + claim.status.slice(1)}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-3">
                      <div>
                        <p className="text-xs text-gray-500">Service Date</p>
                        <p className="text-sm font-medium text-gray-900">
                          {formatDate(claim.serviceDate)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Amount</p>
                        <p className="text-sm font-medium text-gray-900">
                          {formatCurrency(claim.amount)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Submitted</p>
                        <p className="text-sm font-medium text-gray-900">
                          {formatDate(claim.submittedDate)}
                        </p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-500">Last Updated</p>
                        <p className="text-sm font-medium text-gray-900">
                          {formatDate(claim.lastUpdated)}
                        </p>
                      </div>
                    </div>

                    <div className="mb-3">
                      <p className="text-sm text-gray-900 font-medium mb-1">Service Description</p>
                      <p className="text-sm text-gray-600">{claim.serviceDescription}</p>
                    </div>

                    {(claim.copay || claim.deductible || claim.coinsurance) && (
                      <div className="grid grid-cols-3 gap-4 mb-3 p-3 bg-gray-50 rounded-md">
                        {claim.copay !== undefined && (
                          <div>
                            <p className="text-xs text-gray-500">Copay</p>
                            <p className="text-sm font-medium text-gray-900">
                              {formatCurrency(claim.copay)}
                            </p>
                          </div>
                        )}
                        {claim.deductible !== undefined && (
                          <div>
                            <p className="text-xs text-gray-500">Deductible</p>
                            <p className="text-sm font-medium text-gray-900">
                              {formatCurrency(claim.deductible)}
                            </p>
                          </div>
                        )}
                        {claim.coinsurance !== undefined && (
                          <div>
                            <p className="text-xs text-gray-500">Coinsurance</p>
                            <p className="text-sm font-medium text-gray-900">
                              {formatCurrency(claim.coinsurance)}
                            </p>
                          </div>
                        )}
                      </div>
                    )}

                    {claim.notes && (
                      <div className="mb-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                        <p className="text-sm text-yellow-800">
                          <strong>Note:</strong> {claim.notes}
                        </p>
                      </div>
                    )}

                    <div className="flex space-x-3">
                      <button className="text-sm text-primary-600 hover:text-primary-500 font-medium">
                        View Details
                      </button>
                      {claim.status === 'denied' && (
                        <button className="text-sm text-orange-600 hover:text-orange-500 font-medium">
                          File Appeal
                        </button>
                      )}
                      <button className="text-sm text-gray-600 hover:text-gray-500 font-medium">
                        Download Documents
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'eligibility' && (
            <div className="text-center py-12">
              <CheckCircleIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Insurance Eligibility</h3>
              <p className="mt-1 text-sm text-gray-500">
                Verify your insurance coverage and benefits
              </p>
              <div className="mt-6">
                <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  Check Eligibility
                </button>
              </div>
            </div>
          )}

          {activeTab === 'appeals' && (
            <div className="text-center py-12">
              <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Insurance Appeals</h3>
              <p className="mt-1 text-sm text-gray-500">
                Manage and track your insurance claim appeals
              </p>
              <div className="mt-6">
                <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
                  File New Appeal
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default InsuranceClaims;
