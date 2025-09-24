import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCharacterStore } from '../../store/characterStore';
import CharacterHeader from './sheet/CharacterHeader';
import AttributesTab from './sheet/tabs/AttributesTab';
import SkillsTab from './sheet/tabs/SkillsTab';
import TalentsTab from './sheet/tabs/TalentsTab';
import AssetsTab from './sheet/tabs/AssetsTab';
import FollowersTab from './sheet/tabs/FollowersTab';
import ComplicationsTab from './sheet/tabs/ComplicationsTab';

const CharacterSheet = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { getCharacter, currentCharacter, isLoading, error, clearError } = useCharacterStore();
  const [activeTab, setActiveTab] = useState('attributes');

  useEffect(() => {
    const fetchCharacter = async () => {
      try {
        await getCharacter(id);
      } catch (err) {
        console.error('Failed to fetch character:', err);
      }
    };

    if (id) {
      fetchCharacter();
    }
  }, [id, getCharacter]);

  const tabs = [
    { id: 'attributes', name: 'Attributes', component: AttributesTab },
    { id: 'skills', name: 'Skills', component: SkillsTab },
    { id: 'talents', name: 'Talents', component: TalentsTab },
    { id: 'assets', name: 'Assets', component: AssetsTab },
    { id: 'followers', name: 'Followers', component: FollowersTab },
    { id: 'complications', name: 'Complications', component: ComplicationsTab },
  ];

  const ActiveTabComponent = tabs.find(tab => tab.id === activeTab)?.component || AttributesTab;

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <svg className="animate-spin h-12 w-12 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-900 p-4">
        <div className="flex justify-between">
          <div className="text-sm text-red-200">
            {error}
          </div>
          <button
            onClick={() => {
              clearError();
              navigate('/characters');
            }}
            className="text-sm text-red-200 hover:text-white"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  if (!currentCharacter) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-medium text-gray-200">Character not found</h3>
        <button
          onClick={() => navigate('/characters')}
          className="mt-4 btn-primary"
        >
          Back to Characters
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <CharacterHeader character={currentCharacter} />
      
      <div className="border-b border-gray-700">
        <nav className="-mb-px flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`${
                activeTab === tab.id
                  ? 'border-purple-500 text-purple-400'
                  : 'border-transparent text-gray-400 hover:text-gray-300 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      <div className="bg-gray-800 rounded-lg shadow p-6">
        <ActiveTabComponent character={currentCharacter} />
      </div>
    </div>
  );
};

export default CharacterSheet;

