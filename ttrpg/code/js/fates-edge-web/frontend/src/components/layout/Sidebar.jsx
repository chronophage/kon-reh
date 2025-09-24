// frontend/src/components/layout/Sidebar.jsx (updated)
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  HomeIcon, 
  UserGroupIcon, 
  UserCircleIcon, 
  DiceIcon, 
  CommandLineIcon,
  Cog6ToothIcon
} from '@heroicons/react/24/outline';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
  { name: 'Campaigns', href: '/campaigns', icon: UserGroupIcon },
  { name: 'Characters', href: '/characters', icon: UserCircleIcon },
  { name: 'Dice Roller', href: '/roll', icon: DiceIcon },
  { name: 'Macros', href: '/macros', icon: CommandLineIcon },
  { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
];

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="flex flex-col h-full bg-fate-dark border-r border-fate-darker">
      <div className="flex items-center justify-center h-16 border-b border-fate-darker">
        <h1 className="text-xl font-bold text-fate-accent">Fate's Edge</h1>
      </div>
      
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href || 
                          (item.href !== '/' && location.pathname.startsWith(item.href));
          
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                isActive
                  ? 'bg-fate-accent text-fate-darker'
                  : 'text-gray-300 hover:bg-fate-darker hover:text-white'
              }`}
            >
              <item.icon className="mr-3 h-5 w-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default Sidebar;

