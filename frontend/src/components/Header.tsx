import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  UserIcon, 
  DocumentTextIcon, 
  MagnifyingGlassIcon,
  CreditCardIcon 
} from '@heroicons/react/24/outline';

const Header: React.FC = () => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon },
    { name: 'Profile', href: '/profile', icon: UserIcon },
    { name: 'Documents', href: '/documents', icon: DocumentTextIcon },
    { name: 'Find Providers', href: '/providers', icon: MagnifyingGlassIcon },
    { name: 'Insurance', href: '/insurance', icon: CreditCardIcon },
  ];

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-primary-600">
                Medical Blitzy AI
              </h1>
              <p className="text-xs text-gray-500">Integrated Health Navigator</p>
            </div>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => {
              const isActive = location.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`inline-flex items-center px-1 pt-1 text-sm font-medium ${
                    isActive
                      ? 'text-primary-600 border-b-2 border-primary-600'
                      : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <item.icon className="w-4 h-4 mr-2" />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center">
            <div className="text-sm text-gray-700">
              <span className="font-medium">Patient Portal</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
