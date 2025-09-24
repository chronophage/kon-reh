import React, { useState } from 'react';
import { CalendarIcon, PlusIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

const SessionList = ({ campaign, isGM }) => {
  const [sessions] = useState([
    { 
      id: 1, 
      date: '2024-01-15', 
      title: 'The Shattered Gate', 
      notes: 'Party investigates the mysterious gate...', 
      attendance: 4 
    },
    { 
      id: 2, 
      date: '2024-01-08', 
      title: 'Character Introductions', 
      notes: 'Players create characters and meet...', 
      attendance: 3 
    },
    { 
      id: 3, 
      date: '2024-01-01', 
      title: 'Campaign Start', 
      notes: 'Opening session, setting introduction...', 
      attendance: 4 
    }
  ]);

  const [showNewSession, setShowNewSession] = useState(false);
  const [newSession, setNewSession] = useState({
    date: new Date().toISOString().split('T')[0],
    title: '',
    notes: ''
  });

  const handleCreateSession = (e) => {
    e.preventDefault();
    // In a real app, this would create a session
    console.log('Creating session:', newSession);
    setShowNewSession(false);
    setNewSession({
      date: new Date().toISOString().split('T')[0],
      title: '',
      notes: ''
    });
  };

  return (
    <div className="bg-gray-800 rounded-lg shadow">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-medium text-white">Sessions</h2>
          {isGM && (
            <button
              onClick={() => setShowNewSession(!showNewSession)}
              className="btn-secondary flex items-center text-sm"
            >
              <PlusIcon className="h-4 w-4 mr-1" />
              New Session
            </button>
          )}
        </div>
      </div>
      
      <div className="p-6">
        {/* New Session Form */}
        {showNewSession && isGM && (
          <div className="mb-6 bg-gray-700 rounded-lg p-4">
            <h3 className="text-lg font-medium text-white mb-3">Create New Session</h3>
            <form onSubmit={handleCreateSession} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Session Date
                </label>
                <input
                  type="date"
                  value={newSession.date}
                  onChange={(e) => setNewSession(prev => ({ ...prev, date: e.target.value }))}
                  className="input-field w-full"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Session Title
                </label>
                <input
                  type="text"
                  value={newSession.title}
                  onChange={(e) => setNewSession(prev => ({ ...prev, title: e.target.value }))}
                  className="input-field w-full"
                  placeholder="e.g., The Shattered Gate"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Session Notes
                </label>
                <textarea
                  value={newSession.notes}
                  onChange={(e) => setNewSession(prev => ({ ...prev, notes: e.target.value }))}
                  className="input-field w-full"
                  rows="3"
                  placeholder="Brief summary of what happened in this session..."
                />
              </div>
              <div className="flex space-x-2">
                <button
                  type="submit"
                  className="btn-primary flex-1"
                >
                  Create Session
                </button>
                <button
                  type="button"
                  onClick={() => setShowNewSession(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Sessions List */}
        {sessions.length > 0 ? (
          <div className="space-y-4">
            {sessions.map(session => (
              <div key={session.id} className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors duration-200">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center">
                      <CalendarIcon className="h-5 w-5 text-purple-400 mr-2" />
                      <h3 className="text-lg font-medium text-white">{session.title}</h3>
                    </div>
                    <p className="text-sm text-gray-400 mt-1">
                      {new Date(session.date).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-300 mt-2 line-clamp-2">
                      {session.notes}
                    </p>
                  </div>
                  <div className="flex items-center">
                    <div className="flex items-center text-sm text-gray-400 mr-4">
                      <UserIcon className="h-4 w-4 mr-1" />
                      {session.attendance}
                    </div>
                    <button className="p-2 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500">
                      <DocumentTextIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <DocumentTextIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-200">No sessions</h3>
            <p className="mt-1 text-sm text-gray-400">
              {isGM 
                ? 'Create your first session to get started.' 
                : 'No sessions have been recorded yet.'}
            </p>
            {isGM && (
              <div className="mt-6">
                <button
                  onClick={() => setShowNewSession(true)}
                  className="btn-primary inline-flex items-center"
                >
                  <PlusIcon className="h-4 w-4 mr-1" />
                  New Session
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

// Add this helper component for the user icon
const UserIcon = ({ className }) => (
  <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

export default SessionList;

