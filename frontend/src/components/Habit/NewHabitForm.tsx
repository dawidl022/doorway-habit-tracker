import { useState, type FC } from "react";

interface Props {
  onCreate: (habitTest: string) => void;
}

const NewHabitForm: FC<Props> = ({ onCreate }) => {
  const [habitText, setHabitText] = useState("");

  const createHabit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const trimmedText = habitText.trim();
    if (trimmedText === "") {
      return;
    }

    onCreate(trimmedText);
    setHabitText("");
  };

  return (
    <form onSubmit={createHabit}>
      <label htmlFor="new-habit-field">Add a Habit</label>
      <input
        type="text"
        value={habitText}
        onChange={(e) => setHabitText(e.target.value)}
      />
    </form>
  );
};

export default NewHabitForm;
