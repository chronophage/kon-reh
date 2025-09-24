import React, { useState } from 'react';
import { XMarkIcon, ArrowPathIcon } from '@heroicons/react/24/outline';
import { useDiceStore } from '../../store/diceStore';

const ComplicationDrawer = ({ onClose, onDraw }) => {
  const { drawComplications, isRolling } = useDiceStore();
  const [points, setPoints] = useState(1);
  const [complications, setComplications] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);

  const sampleComplications = [
    "Unexpected arrival of an enemy or rival",
    "A trusted ally acts against you",
    "Something you possess is stolen or damaged",
    "A secret is revealed at the worst possible moment",
    "The environment turns against you",
    "A crucial piece of equipment fails",
    "An innocent person is endangered",
    "Your reputation suffers",
    "A past mistake comes back to haunt you",
    "Resources become scarce or unavailable",
    "Time pressure intensifies",
    "A key ally becomes unavailable",
    "Misinformation spreads",
    "A hidden threat is revealed",
    "Personal relationships become strained"
  ];

  const handleDraw = async () => {
    setIsDrawing(true);
    try {
      // In a real implementation, this would call the API
      // For demo purposes, we'll generate sample complications
      const drawn = [];
      for (let i = 0; i < points; i++) {
        const randomIndex = Math.floor(Math.random() * sampleComplications.length);
        drawn.push(sampleComplications[randomIndex]);
      }
      setComplications(drawn);
    } catch (error) {
      console.error('Failed to draw complications:', error);
    } finally {
      setIsDrawing(false);
    }
  };

  const handleRedraw = (index) => {
    const newComplications = [...complications];
    const randomIndex = Math.floor(Math.random() * sampleComplications.length);
    newComplications[index] = sampleComplications[randomIndex];
    setComplications(newComplications);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div className="absolute inset-0 bg-black bg-opacity-50" onClick={onClose}></div>
      
      <div className="absolute inset-y-0 right-0 max-w-full flex">
        <div className="relative w-screen max-w-md">
          <div className="h-full flex flex-col bg-gray-800 shadow-xl">
            <div className="flex-1 overflow-y-auto">
              <div className="px-4 py-6 sm:px-6">
                <div className="flex items-start justify-between">
                  <h2 className="text-lg font-medium text-white">
                    Complication Drawer
                  </h2>
                  <button
                    onClick={onClose}
                    className="ml-3 h-7 flex items-center justify-center rounded-full bg-gray-700 text-gray-400 hover:text-white focus:outline-none"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </button>
                </div>
                
                <div className="mt-6">
                  <div className="bg-gray-700 rounded-lg p-4 mb-6">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Number of Complications
                    </label>
                    <div className="flex items-center space-x-3">
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={points}
                        onChange={(e) => setPoints(parseInt(e.target.value))}
                        className="flex-1 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer"
                        disabled={isDrawing}
                      />
                      <span className="text-lg font-bold text-white w-8 text-center">
                        {points}
                      </span>
                    </div>
                    <div className="flex justify-between text-xs text-gray-400 mt-1">
                      <span>1</span>
                      <span>3</span>
                      <span>5</span>
                    </div>
                    
                    <button
                      onClick={handleDraw}
                      disabled={isDrawing}
                      className="w-full mt-4 btn-primary flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isDrawing ? (
                        <>
                          <ArrowPathIcon className="h-4 w-4 mr-2 animate-spin" />
                          Drawing...
                        </>
                      ) : (
                        `Draw ${points} Complication${points !== 1 ? 's' : ''}`
                      )}
                    </button>
                  </div>

                  {complications.length > 0 && (
                    <div className="space-y-4">
                      <h3 className="text-md font-medium text-gray-300">
                        Drawn Complications
                      </h3>
                      <div className="space-y-3">
                        {complications.map((complication, index) => (
                          <div
                            key={index}
                            className="bg-gray-700 rounded-lg p-4 border-l-4 border-red-500"
                          >
                            <div className="flex items-start justify-between">
                              <p className="text-white flex-1">{complication}</p>
                              <button
                                onClick={() => handleRedraw(index)}
                                className="ml-2 p-1 rounded-full bg-gray-600 text-gray-300 hover:bg-gray-500"
                                title="Redraw this complication"
                              >
                                <ArrowPathIcon className="h-4 w-4" />
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                      
                      <div className="pt-4 border-t border-gray-700">
                        <h4 className="text-sm font-medium text-gray-300 mb-2">
                          How to Use Complications
                        </h4>
                        <ul className="text-xs text-gray-400 space-y-1">
                          <li>• Introduce these elements into your story</li>
                          <li>• Award boons to players who embrace complications</li>
                          <li>• Use them to create tension and drive narrative</li>
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComplicationDrawer;

