// frontend/src/api/occupancy.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface DeskRecommendation {
  id: string;
  type: 'standing' | 'regular';
  area_id: string;
  vergesense_area_id: string;
  floor: number;
  zone: string;
  location_description: string;
  features: string[];
  status: 'available' | 'occupied' | 'maintenance';
  last_used: string; // ISO string
}


export async function queryOccupancy(queryText: string): Promise<DeskRecommendation[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/query-occupancy`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // THIS IS THE KEY CHANGE: Send a JSON object
      body: JSON.stringify({ query_text: queryText }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Failed to query occupancy');
    }

    return await response.json();
  } catch (error) {
    console.error('Error in queryOccupancy:', error);
    throw error;
  }
}