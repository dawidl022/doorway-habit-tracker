type date = string;

interface Habit {
  id: string;
  description: string;
  completedToday: boolean;
  currentStreak?: number;
  lastCheckIn?: date;
}

export type { Habit };
