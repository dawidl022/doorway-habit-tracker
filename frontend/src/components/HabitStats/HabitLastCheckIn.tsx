import type { FC } from "react";

interface Props {
  numberOfDays: number;
}

const HabitLastCheckIn: FC<Props> = ({ numberOfDays }) => {
  return (
    <>
      Days since last check-in: {numberOfDays} day
      {numberOfDays !== 1 ? "s" : ""}
    </>
  );
};

export default HabitLastCheckIn;
