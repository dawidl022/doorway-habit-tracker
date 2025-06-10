import type { FC } from "react";
import type { Habit } from "../../models/habit";
import HabitTile from "./HabitTile";
import "./HabitList.css";

interface Props {
  habits: Habit[];
  markHabit: (id: string, completed: boolean) => void;
}

const HabitList: FC<Props> = ({ habits, markHabit }) => {
  return (
    <ul className="habit-list">
      {habits.map((h) => (
        <li key={h.id}>
          <HabitTile
            habit={h}
            markHabit={(completed) => markHabit(h.id, completed)}
          />
        </li>
      ))}
    </ul>
  );
};

export default HabitList;
