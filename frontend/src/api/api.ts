import type { Habit } from "../models/habit";

interface CreatedHabit {
  id: string;
}

const useApi = () => {
  const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8080";

  const fetchHabits = async (): Promise<Habit[]> => {
    const response = await fetch(`${apiUrl}/habits`);
    if (!response.ok) {
      throw new Error("Failed to fetch habits");
    }
    return response.json();
  };

  const addHabit = async (habitText: string): Promise<CreatedHabit> => {
    const response = await fetch(`${apiUrl}/habits`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description: habitText }),
    });
    if (!response.ok) {
      throw new Error("Failed to add habit");
    }
    return response.json();
  };

  const checkIn = async (habitId: string, date: string): Promise<void> => {
    const response = await fetch(`${apiUrl}/habits/${habitId}/check-ins`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date }),
    });
    if (!response.ok) {
      throw new Error("Failed to check in");
    }
  };

  const deleteCheckIn = async (
    habitId: string,
    date: string
  ): Promise<void> => {
    const response = await fetch(`${apiUrl}/habits/${habitId}/check-ins`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date }),
    });
    if (!response.ok) {
      throw new Error("Failed to delete check-in");
    }
  };

  return { fetchHabits, addHabit, checkIn, deleteCheckIn };
};

export { useApi };
export type { CreatedHabit };
