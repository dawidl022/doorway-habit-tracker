import type { FC } from "react";
import type { Habit } from "../../models/habit";
import HabitStreak from "./HabitStreak";
import HabitLastCheckIn from "./HabitLastCheckIn";

interface Props {
  habit: Habit;
}

const HabitStats: FC<Props> = ({ habit }) => {
  if (habit.lastCheckIn == null || habit.currentStreak == null) {
    // backend API does not support these fields yet, so we don't render them
    // for now
    return <></>;
  }

  if (globalThis.Temporal == null) {
    // Temporal API is not yet available in the browser, could include a
    // polyfill later
    return;
  }

  const today = Temporal.Now.plainDateISO();
  const habitLastCheckIn = Temporal.PlainDate.from(habit.lastCheckIn);
  const daysSinceLastCheckIn = habitLastCheckIn
    .until(today)
    .total({ unit: "days" });

  return (
    <div>
      {daysSinceLastCheckIn <= 1 ? (
        <HabitStreak streakDays={habit.currentStreak} />
      ) : (
        <HabitLastCheckIn numberOfDays={daysSinceLastCheckIn} />
      )}
    </div>
  );
};

export default HabitStats;
