import { useEffect, useState, type FC } from "react";
import NewHabitForm from "./Habit/NewHabitForm";
import HabitList from "./Habit/HabitList";
import type { Habit } from "../models/habit";
import { useApi } from "../api/api";
import "./HabitTracker.css";

const HabitTacker: FC = () => {
  const [habits, setHabits] = useState<Habit[] | null>(null);
  const api = useApi();

  const fetchHabits = () => {
    api.fetchHabits().then((habits) => {
      setHabits(habits);
    });
  };

  const createHabit = (habitText: string) => {
    api.addHabit(habitText).then(({ id: habitId }) => {
      setHabits((prevHabits) => {
        const newHabit: Habit = {
          id: habitId,
          description: habitText,
          completedToday: false,
        };
        return prevHabits ? [...prevHabits, newHabit] : [newHabit];
      });
    });
  };

  const markHabit = (id: string, completed: boolean) => {
    const today = new Date().toISOString().split("T")[0];
    if (completed) {
      // TODO handle error
      api.checkIn(id, today);
    } else {
      api.deleteCheckIn(id, today);
    }

    setHabits((prevHabits) => {
      return prevHabits!.map((habit) =>
        habit.id === id ? { ...habit, completedToday: completed } : habit
      );
    });
  };

  useEffect(fetchHabits, []);

  return (
    <main className="habit-tracker">
      <NewHabitForm onCreate={createHabit} />
      {habits ? (
        <HabitList habits={habits} markHabit={markHabit} />
      ) : (
        <p>Loading...</p>
      )}
    </main>
  );
};

export default HabitTacker;
