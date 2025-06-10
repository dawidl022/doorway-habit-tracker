import type { FC } from "react";

interface Props {
  streakDays: number;
}

const HabitStreak: FC<Props> = ({ streakDays }) => {
  return (
    <>
      Streak: {streakDays} day{streakDays !== 1 ? "s" : ""}
    </>
  );
};

export default HabitStreak;
