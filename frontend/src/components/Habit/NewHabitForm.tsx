import { useState, type FC } from "react";
import "./NewHabitForm.css";

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
    <form onSubmit={createHabit} className="habit-form">
      <label htmlFor="new-habit-field">Add a Habit</label>
      <input
        type="text"
        id="new-habit-field"
        value={habitText}
        onChange={(e) => setHabitText(e.target.value)}
      />
    </form>
  );
};

export default NewHabitForm;
