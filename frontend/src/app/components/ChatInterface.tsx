// frontend/src/components/ChatInterface.tsx
'use client'; // This is a client component in Next.js 13+

import React, { useState } from 'react';
import { queryOccupancy, DeskRecommendation } from '../api/occupancy';

export const ChatInterface: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<DeskRecommendation[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const recommendations = await queryOccupancy(query);
      setResults(recommendations);
    } catch (err) {
      setError(`Failed to get recommendations: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-gray-100 rounded-lg shadow-md">
      <h1 className="text-2xl font-bold text-gray-800 mb-4 text-center">Occupancy Planner AI</h1>
      <p className="text-gray-600 mb-6 text-center">
        Ask me: "Find me an available standing desk near the marketing team on the 3rd floor for tomorrow afternoon."
      </p>

      <form onSubmit={handleSubmit} className="flex gap-4 mb-8">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query..."
          className="flex-grow p-3 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Searching...' : 'Find Desk'}
        </button>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <strong className="font-bold">Error!</strong>
          <span className="block sm:inline"> {error}</span>
        </div>
      )}

      {results && (
        <div className="bg-white p-4 rounded-md shadow">
          <h2 className="text-xl font-semibold mb-3 text-gray-700">Recommendations:</h2>
          {results.length > 0 ? (
            <ul className="space-y-3">
              {results.map((desk) => (
                <li key={desk.id} className="p-3 border border-gray-200 rounded-md bg-gray-50">
                  <p className="font-medium text-lg text-blue-700">{desk.id} - {desk.type.charAt(0).toUpperCase() + desk.type.slice(1)} Desk</p>
                  <p className="text-sm text-gray-600">
                    Floor {desk.floor}, Zone: {desk.zone} ({desk.area_id})
                  </p>
                  <p className="text-sm text-gray-600">Location: {desk.location_description}</p>
                  <p className="text-sm text-gray-600">Features: {desk.features.join(', ')}</p>
                  <p className="text-sm text-gray-600">Status: <span className={`font-semibold ${desk.status === 'available' ? 'text-green-600' : 'text-yellow-600'}`}>{desk.status.charAt(0).toUpperCase() + desk.status.slice(1)}</span></p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No available desks found matching your criteria.</p>
          )}
        </div>
      )}
    </div>
  );
};