import type { FC } from "react";
import Header from "./components/Header";
import HabitTacker from "./components/HabitTracker";
import "./App.css";

const App: FC = () => {
  return (
    <>
      <Header />
      <HabitTacker />
    </>
  );
};

export default App;
