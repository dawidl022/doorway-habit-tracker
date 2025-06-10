import type { FC } from "react";
import type { Habit } from "../../models/habit";
import "./HabitTile.css";

interface Props {
  habit: Habit;
  markHabit: (completed: boolean) => void;
}

const HabitTile: FC<Props> = ({ habit, markHabit }) => {
  return (
    <div>
      <form onSubmit={(e) => e.preventDefault()}>
        <label htmlFor={`habit-${habit.id}`} className="habit-checkbox-label">
          Completed today
        </label>
        <input
          type="checkbox"
          id={`habit-${habit.id}`}
          checked={habit.completedToday}
          onChange={(e) => markHabit(e.target.checked)}
        />
      </form>
      <h2>{habit.description}</h2>
    </div>
  );
};

export default HabitTile;
