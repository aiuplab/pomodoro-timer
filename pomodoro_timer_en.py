import tkinter as tk
from tkinter import ttk, messagebox

class PomodoroTimer:
    """
    A simple Pomodoro Timer GUI application built with Python and Tkinter.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("380x400") # Window size
        self.root.resizable(False, False) # Prevent window resizing

        # Style configuration
        s = ttk.Style()
        s.configure("TFrame", background="#f0f0f0")
        s.configure("TButton", padding=6, relief="flat", background="#c0c0c0")
        s.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        s.configure("Header.TLabel", font=("Helvetica", 18, "bold"))
        s.configure("Timer.TLabel", font=("Helvetica", 48, "bold"))
        s.configure("TCheckbutton", background="#f0f0f0")

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="20 20 20 20", style="TFrame")
        self.main_frame.pack(fill="both", expand=True)

        # --- State and timer variables ---
        self._timer_id = None
        self.running = False
        self.is_work_time = True
        
        # Default times in seconds
        self.work_sec = 30 * 60
        self.break_sec = 5 * 60
        
        self.time_left = self.work_sec

        # --- Create UI widgets ---
        self.create_widgets()

    def create_widgets(self):
        """Create all the GUI widgets."""
        # Status Label
        self.status_label = ttk.Label(self.main_frame, text="Work", style="Header.TLabel")
        self.status_label.pack(pady=(0, 10))

        # Countdown Timer Label
        self.timer_label = ttk.Label(self.main_frame, text=self.format_time(self.time_left), style="Timer.TLabel")
        self.timer_label.pack(pady=(10, 20))

        # Controls Frame
        controls_frame = ttk.Frame(self.main_frame, style="TFrame")
        controls_frame.pack(pady=10)

        # Control Buttons
        self.start_button = ttk.Button(controls_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = ttk.Button(controls_frame, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.stop_button = ttk.Button(controls_frame, text="Stop", command=self.stop_timer)
        self.stop_button.grid(row=0, column=2, padx=5)

        # Custom Time Entry Fields
        settings_frame = ttk.Frame(self.main_frame, style="TFrame")
        settings_frame.pack(pady=20)

        ttk.Label(settings_frame, text="Work (min):").grid(row=0, column=0, padx=5, sticky="w")
        self.work_entry = ttk.Entry(settings_frame, width=5)
        self.work_entry.insert(0, "30")
        self.work_entry.grid(row=0, column=1, padx=5)

        ttk.Label(settings_frame, text="Rest (min):").grid(row=0, column=2, padx=5, sticky="w")
        self.break_entry = ttk.Entry(settings_frame, width=5)
        self.break_entry.insert(0, "5")
        self.break_entry.grid(row=0, column=3, padx=5)
        
        # Loop Option
        self.loop_var = tk.BooleanVar(value=True)
        self.loop_checkbutton = ttk.Checkbutton(
            self.main_frame,
            text="Auto-restart cycles",
            variable=self.loop_var,
            style="TCheckbutton"
        )
        self.loop_checkbutton.pack(pady=10)

    def format_time(self, seconds):
        """Formats seconds into MM:SS string."""
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02d}:{sec:02d}"

    def update_timer(self):
        """Updates the timer every second."""
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=self.format_time(self.time_left))
            self._timer_id = self.root.after(1000, self.update_timer)
        elif self.running and self.time_left == 0:
            # Play a sound notification (optional, works on Windows)
            try:
                import winsound
                winsound.Beep(1000, 500) # frequency=1000Hz, duration=500ms
            except ImportError:
                # On non-Windows systems, just print a message
                print("Time's up!")
            self.switch_mode()

    def start_timer(self):
        """Starts or resumes the timer."""
        if self.running:
            return

        try:
            # Get and set custom times from entry fields
            self.work_sec = int(self.work_entry.get()) * 60
            self.break_sec = int(self.break_entry.get()) * 60
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for minutes.")
            return

        # If the timer was stopped or it's the first run, set time based on the current mode
        if self._timer_id is None:
            self.time_left = self.work_sec if self.is_work_time else self.break_sec
            self.status_label.config(text="Work" if self.is_work_time else "Break")

        self.running = True
        self.update_timer()

    def pause_timer(self):
        """Pauses the timer."""
        if self.running:
            self.running = False
            if self._timer_id:
                self.root.after_cancel(self._timer_id)
            self.status_label.config(text=f"{self.status_label.cget('text')} (Paused)")

    def stop_timer(self):
        """Stops and resets the timer."""
        if self._timer_id:
            self.root.after_cancel(self.timer_id)
            self._timer_id = None
        
        self.running = False
        self.is_work_time = True
        self.status_label.config(text="Work")
        try:
            self.work_sec = int(self.work_entry.get()) * 60
            self.time_left = self.work_sec
            self.timer_label.config(text=self.format_time(self.time_left))
        except ValueError:
            self.time_left = 30 * 60 # Reset to default if entry is invalid
            self.timer_label.config(text=self.format_time(self.time_left))

    def switch_mode(self):
        """Switches between Work and Break modes."""
        self.is_work_time = not self.is_work_time
        
        if self.loop_var.get():
            self.time_left = self.work_sec if self.is_work_time else self.break_sec
            self.status_label.config(text="Work" if self.is_work_time else "Break")
            self.timer_label.config(text=self.format_time(self.time_left))
            # Automatically start the next cycle
            self.update_timer()
        else:
            # If not looping, stop the timer
            self.stop_timer()
            messagebox.showinfo("Finished", "Pomodoro cycle complete!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()