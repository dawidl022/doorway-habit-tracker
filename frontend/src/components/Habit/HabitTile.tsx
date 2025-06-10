import type { FC } from "react";
import type { Habit } from "../../models/habit";
import HabitStats from "../HabitStats/HabitStats";
import "./HabitTile.css";

interface Props {
  habit: Habit;
  markHabit: (completed: boolean) => void;
}

const HabitTile: FC<Props> = ({ habit, markHabit }) => {
  return (
    <div
      className={habit.completedToday ? "habit-tile completed" : "habit-tile"}
    >
      <form onSubmit={(e) => e.preventDefault()}>
        <label htmlFor={`habit-${habit.id}`} className="habit-checkbox-label">
          Completed today
        </label>
        <input
          className="habit-checkbox"
          type="checkbox"
          id={`habit-${habit.id}`}
          checked={habit.completedToday}
          onChange={(e) => markHabit(e.target.checked)}
        />
      </form>
      <h2>{habit.description}</h2>
      <div className="stats">
        <HabitStats habit={habit} />
      </div>
    </div>
  );
};

export default HabitTile;
