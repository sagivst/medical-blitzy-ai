import React from 'react';
import { Link } from 'react-router-dom';
import { 
  DocumentTextIcon, 
  MagnifyingGlassIcon,
  CreditCardIcon,
  ChartBarIcon,
  ClockIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const quickActions = [
    {
      name: 'Upload Documents',
      description: 'Upload medical records for OCR processing',
      href: '/documents',
      icon: DocumentTextIcon,
      color: 'bg-blue-500'
    },
    {
      name: 'Find Providers',
      description: 'AI-powered provider matching',
      href: '/providers',
      icon: MagnifyingGlassIcon,
      color: 'bg-green-500'
    },
    {
      name: 'Insurance Claims',
      description: 'Track and manage insurance claims',
      href: '/insurance',
      icon: CreditCardIcon,
      color: 'bg-purple-500'
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'document',
      title: 'Lab Results Processed',
      description: 'Blood work from Dr. Smith converted to FHIR',
      time: '2 hours ago',
      status: 'completed'
    },
    {
      id: 2,
      type: 'provider',
      title: 'New Provider Match',
      description: 'Found 3 specialists matching your condition',
      time: '1 day ago',
      status: 'pending'
    },
    {
      id: 3,
      type: 'insurance',
      title: 'Claim Submitted',
      description: 'MRI scan claim submitted to insurance',
      time: '3 days ago',
      status: 'processing'
    }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Welcome to your Integrated Health Navigator
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {quickActions.map((action) => (
          <Link
            key={action.name}
            to={action.href}
            className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg shadow hover:shadow-md transition-shadow"
          >
            <div>
              <span className={`rounded-lg inline-flex p-3 ${action.color} text-white`}>
                <action.icon className="h-6 w-6" aria-hidden="true" />
              </span>
            </div>
            <div className="mt-4">
              <h3 className="text-lg font-medium text-gray-900">
                {action.name}
              </h3>
              <p className="mt-2 text-sm text-gray-500">
                {action.description}
              </p>
            </div>
          </Link>
        ))}
      </div>

      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Recent Activity
          </h3>
          <div className="flow-root">
            <ul className="-mb-8">
              {recentActivity.map((item, itemIdx) => (
                <li key={item.id}>
                  <div className="relative pb-8">
                    {itemIdx !== recentActivity.length - 1 ? (
                      <span
                        className="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"
                        aria-hidden="true"
                      />
                    ) : null}
                    <div className="relative flex space-x-3">
                      <div>
                        <span className={`h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white ${
                          item.status === 'completed' ? 'bg-green-500' :
                          item.status === 'pending' ? 'bg-yellow-500' : 'bg-blue-500'
                        }`}>
                          {item.type === 'document' && <DocumentTextIcon className="h-4 w-4 text-white" />}
                          {item.type === 'provider' && <MagnifyingGlassIcon className="h-4 w-4 text-white" />}
                          {item.type === 'insurance' && <CreditCardIcon className="h-4 w-4 text-white" />}
                        </span>
                      </div>
                      <div className="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {item.title}
                          </p>
                          <p className="text-sm text-gray-500">
                            {item.description}
                          </p>
                        </div>
                        <div className="text-right text-sm whitespace-nowrap text-gray-500">
                          <time>{item.time}</time>
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
